#!/usr/bin/env python3

import os
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose, FollowWaypoints
from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Header
from builtin_interfaces.msg import Time
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import datetime
import json
import math
import time
import tf2_ros
import uuid
from tf2_ros import Buffer, TransformListener

class CoveragePlanner(Node):
    """
    Implementation of the Coverage Path Planning (CPP) algorithm for robot exploration.
    This module generates a path that covers the entire accessible area of a map.
    """
    
    def __init__(self):
        super().__init__('coverage_planner')
        
        # Parameters
        self.declare_parameter('cell_size', 0.1)  # Cell size in meters
        self.declare_parameter('robot_radius', 0.2)  # Robot radius in meters
        self.declare_parameter('inflation_radius', 0.3)  # Inflation radius in meters
        self.declare_parameter('visualization_enabled', True)  # Enable visualization
        self.declare_parameter('map_topic', '/map')  # Map topic
        
        # Get parameters
        self.cell_size = self.get_parameter('cell_size').value
        self.robot_radius = self.get_parameter('robot_radius').value
        self.inflation_radius = self.get_parameter('inflation_radius').value
        self.visualization_enabled = self.get_parameter('visualization_enabled').value
        self.map_topic = self.get_parameter('map_topic').value
        
        # Initialize map data
        self.map = None
        self.map_frame = None
        self.map_origin = None
        self.map_resolution = None
        self.map_width = None
        self.map_height = None
        
        # Initialize coverage path
        self.coverage_path = []
        self.waypoints = []
        self.current_waypoint_index = 0
        self.exploration_completed = False
        
        # Initialize coverage grid
        self.coverage_grid = None
        
        # Run ID for experiment tracking
        self.run_id = f"coverage_run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.run_uuid = str(uuid.uuid4())[:8]
        
        # Create data directory
        self.data_dir = os.path.expanduser(f"~/coverage_data/{self.run_id}")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Set up action clients using a callback group to avoid deadlocks
        self.callback_group = ReentrantCallbackGroup()
        
        # Action client for navigation
        self.nav_to_pose_client = ActionClient(
            self, NavigateToPose, 'navigate_to_pose', callback_group=self.callback_group)
        
        # Action client for waypoint following
        self.follow_waypoints_client = ActionClient(
            self, FollowWaypoints, 'follow_waypoints', callback_group=self.callback_group)
            
        # Wait for action servers
        self.get_logger().info('Waiting for navigation action servers...')
        self.nav_to_pose_client.wait_for_server()
        self.follow_waypoints_client.wait_for_server()
        self.get_logger().info('Navigation action servers connected!')
        
        # Map subscription
        self.map_sub = self.create_subscription(
            OccupancyGrid,
            self.map_topic,
            self.map_callback,
            10)
            
        # Set up TF listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Timer for periodic tasks
        self.timer = self.create_timer(5.0, self.timer_callback)
        
        # Set up visualization timer (if enabled)
        if self.visualization_enabled:
            self.viz_timer = self.create_timer(10.0, self.visualization_callback)
        
        self.get_logger().info('Coverage planner initialized')
        
    def map_callback(self, msg):
        """Process incoming map messages"""
        self.get_logger().info('Received map update')
        
        # Store map data
        self.map = msg
        self.map_frame = msg.header.frame_id
        self.map_origin = (msg.info.origin.position.x, msg.info.origin.position.y)
        self.map_resolution = msg.info.resolution
        self.map_width = msg.info.width
        self.map_height = msg.info.height
        
        # Convert to numpy array for processing
        self.map_data = np.array(msg.data).reshape(self.map_height, self.map_width)
        
        # Initialize coverage grid if not already done
        if self.coverage_grid is None:
            self.coverage_grid = np.zeros((self.map_height, self.map_width), dtype=np.int8)
        
        # If we haven't planned a path yet, do so now
        if not self.coverage_path and not self.exploration_completed:
            self.plan_coverage_path()
    
    def plan_coverage_path(self):
        """
        Plan a complete coverage path based on the current map.
        Uses a simple sweeping pattern algorithm.
        """
        self.get_logger().info('Planning coverage path...')
        
        # Make a copy of the map for planning
        planning_map = self.map_data.copy()
        
        # Mark unknown cells (-1) as obstacles for planning
        planning_map[planning_map == -1] = 100
        
        # Inflate obstacles
        inflated_map = self.inflate_obstacles(planning_map)
        
        # Identify free cells for exploration
        free_cells = np.where(inflated_map == 0)
        free_positions = list(zip(free_cells[0], free_cells[1]))
        
        if not free_positions:
            self.get_logger().warn('No free cells found for exploration')
            return
        
        # Group cells into rows for sweeping pattern
        rows = {}
        for y, x in free_positions:
            if y not in rows:
                rows[y] = []
            rows[y].append(x)
        
        # Sort rows
        sorted_rows = sorted(rows.keys())
        
        # Generate waypoints using a sweeping pattern
        direction = 1  # Start moving right
        path = []
        
        for y in sorted_rows:
            row_cells = sorted(rows[y])
            
            # Skip rows with too few cells (likely noise)
            if len(row_cells) < 5:
                continue
                
            if direction == 1:
                # Left to right
                waypoints = [(y, x) for x in row_cells]
            else:
                # Right to left
                waypoints = [(y, x) for x in reversed(row_cells)]
                
            path.extend(waypoints)
            direction *= -1  # Flip direction for next row
        
        # Convert cell coordinates to world coordinates
        self.coverage_path = [self.cell_to_world(y, x) for y, x in path]
        
        # Downsample the path to reduce the number of waypoints (take every nth point)
        n = max(1, len(self.coverage_path) // 50)  # Aim for ~50 waypoints
        self.waypoints = self.coverage_path[::n]
        
        self.get_logger().info(f'Coverage path planned with {len(self.waypoints)} waypoints')
        
        # Save the planned path for analysis
        self.save_coverage_plan()
        
        # Start navigation
        self.navigate_to_waypoints()
    
    def inflate_obstacles(self, grid_map):
        """
        Inflate obstacles in the map by the specified inflation radius
        """
        # Convert inflation radius from meters to grid cells
        inflation_cells = int(self.inflation_radius / self.map_resolution)
        
        # Make a copy of the map
        inflated_map = grid_map.copy()
        
        # Find obstacle cells
        obstacle_indices = np.where(grid_map >= 50)
        
        # Create a kernel for dilation
        y_indices, x_indices = np.ogrid[-inflation_cells:inflation_cells+1, 
                                        -inflation_cells:inflation_cells+1]
        kernel = x_indices**2 + y_indices**2 <= inflation_cells**2
        
        # For each obstacle, mark the surrounding cells
        for i in range(len(obstacle_indices[0])):
            y, x = obstacle_indices[0][i], obstacle_indices[1][i]
            
            # Calculate kernel bounds
            y_min = max(0, y - inflation_cells)
            y_max = min(self.map_height, y + inflation_cells + 1)
            x_min = max(0, x - inflation_cells)
            x_max = min(self.map_width, x + inflation_cells + 1)
            
            # Calculate kernel indices
            ky_min = inflation_cells - (y - y_min)
            ky_max = inflation_cells + (y_max - y)
            kx_min = inflation_cells - (x - x_min)
            kx_max = inflation_cells + (x_max - x)
            
            # Apply kernel
            inflated_map[y_min:y_max, x_min:x_max] = np.maximum(
                inflated_map[y_min:y_max, x_min:x_max],
                kernel[ky_min:ky_max, kx_min:kx_max] * 100)
        
        return inflated_map
    
    def cell_to_world(self, cell_y, cell_x):
        """
        Convert grid cell coordinates to world coordinates
        """
        world_x = self.map_origin[0] + cell_x * self.map_resolution
        world_y = self.map_origin[1] + cell_y * self.map_resolution
        return (world_x, world_y)
    
    def world_to_cell(self, world_x, world_y):
        """
        Convert world coordinates to grid cell coordinates
        """
        cell_x = int((world_x - self.map_origin[0]) / self.map_resolution)
        cell_y = int((world_y - self.map_origin[1]) / self.map_resolution)
        
        # Ensure coordinates are within bounds
        cell_x = max(0, min(cell_x, self.map_width - 1))
        cell_y = max(0, min(cell_y, self.map_height - 1))
        
        return (cell_y, cell_x)
    
    def navigate_to_waypoints(self):
        """
        Send the list of waypoints to Nav2 for navigation
        """
        if not self.waypoints:
            self.get_logger().warn('No waypoints to navigate to')
            return
            
        self.get_logger().info(f'Navigating to {len(self.waypoints)} waypoints')
        
        # Create a list of PoseStamped messages
        pose_list = []
        for i, (x, y) in enumerate(self.waypoints):
            pose = PoseStamped()
            pose.header.frame_id = self.map_frame
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0
            pose.pose.orientation.w = 1.0  # Identity quaternion
            pose_list.append(pose)
        
        # Create goal
        goal = FollowWaypoints.Goal()
        goal.poses = pose_list
        
        # Send goal
        self.get_logger().info('Sending waypoints to Nav2...')
        self.follow_waypoints_client.send_goal_async(
            goal, feedback_callback=self.feedback_callback)
    
    def feedback_callback(self, feedback_msg):
        """
        Process feedback from Nav2
        """
        feedback = feedback_msg.feedback
        self.current_waypoint_index = feedback.current_waypoint
        self.get_logger().info(f'Following waypoint {self.current_waypoint_index} of {len(self.waypoints)}')
        
        # Update coverage visualization if enabled
        if self.visualization_enabled:
            self.update_coverage_visualization()
    
    def timer_callback(self):
        """
        Periodic check of robot position to update coverage map
        """
        if self.map is None:
            return
            
        try:
            # Get current robot position
            trans = self.tf_buffer.lookup_transform(
                self.map_frame,
                'base_link',
                rclpy.time.Time())
                
            # Convert to map coordinates
            robot_x = trans.transform.translation.x
            robot_y = trans.transform.translation.y
            
            # Convert to grid cell
            cell_y, cell_x = self.world_to_cell(robot_x, robot_y)
            
            # Update coverage grid
            coverage_radius = int(self.robot_radius / self.map_resolution)
            y_min = max(0, cell_y - coverage_radius)
            y_max = min(self.map_height, cell_y + coverage_radius + 1)
            x_min = max(0, cell_x - coverage_radius)
            x_max = min(self.map_width, cell_x + coverage_radius + 1)
            
            # Mark covered cells
            self.coverage_grid[y_min:y_max, x_min:x_max] = 1
            
            # Calculate coverage percentage
            free_cells = np.sum(self.map_data == 0)
            covered_cells = np.sum(self.coverage_grid)
            coverage_pct = (covered_cells / free_cells) * 100 if free_cells > 0 else 0
            
            # Log progress
            self.get_logger().info(f'Coverage: {coverage_pct:.2f}% ({covered_cells}/{free_cells} cells)')
            
            # Check if exploration is complete (reached high coverage)
            if coverage_pct > 90 and not self.exploration_completed:
                self.exploration_completed = True
                self.get_logger().info('Exploration completed! (>90% coverage)')
                self.save_coverage_results()
            
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().warn(f'TF lookup failed: {e}')
    
    def visualization_callback(self):
        """
        Generate and save visualization of the coverage map
        """
        if self.map is None or self.coverage_grid is None:
            return
            
        self.update_coverage_visualization()
    
    def update_coverage_visualization(self):
        """
        Update and save the coverage visualization
        """
        # Create a visualization image
        viz_img = np.zeros((self.map_height, self.map_width, 3), dtype=np.uint8)
        
        # Color coding:
        # White: free space
        # Black: obstacles
        # Gray: unknown
        # Green: covered areas
        # Red: current position
        
        # Mark free space as white
        viz_img[self.map_data == 0] = [255, 255, 255]
        
        # Mark obstacles as black
        viz_img[self.map_data == 100] = [0, 0, 0]
        
        # Mark unknown as gray
        viz_img[self.map_data == -1] = [128, 128, 128]
        
        # Mark covered areas as green
        covered_indices = np.where(self.coverage_grid == 1)
        viz_img[covered_indices] = [0, 200, 0]
        
        # Draw waypoints as blue circles
        for i, (wx, wy) in enumerate(self.waypoints):
            cell_y, cell_x = self.world_to_cell(wx, wy)
            if 0 <= cell_x < self.map_width and 0 <= cell_y < self.map_height:
                # Draw different colors for visited vs. remaining waypoints
                if i < self.current_waypoint_index:
                    color = [0, 0, 200]  # Dark blue for visited
                else:
                    color = [0, 200, 200]  # Cyan for remaining
                
                radius = 3
                y_min = max(0, cell_y - radius)
                y_max = min(self.map_height, cell_y + radius + 1)
                x_min = max(0, cell_x - radius)
                x_max = min(self.map_width, cell_x + radius + 1)
                
                for y in range(y_min, y_max):
                    for x in range(x_min, x_max):
                        if (y - cell_y)**2 + (x - cell_x)**2 <= radius**2:
                            viz_img[y, x] = color
        
        # Try to mark current robot position as red
        try:
            trans = self.tf_buffer.lookup_transform(
                self.map_frame,
                'base_link',
                rclpy.time.Time())
                
            robot_x = trans.transform.translation.x
            robot_y = trans.transform.translation.y
            cell_y, cell_x = self.world_to_cell(robot_x, robot_y)
            
            # Draw robot position
            radius = 5
            y_min = max(0, cell_y - radius)
            y_max = min(self.map_height, cell_y + radius + 1)
            x_min = max(0, cell_x - radius)
            x_max = min(self.map_width, cell_x + radius + 1)
            
            for y in range(y_min, y_max):
                for x in range(x_min, x_max):
                    if (y - cell_y)**2 + (x - cell_x)**2 <= radius**2:
                        viz_img[y, x] = [200, 0, 0]  # Red
                        
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            pass  # Ignore errors
        
        # Save the visualization
        img = Image.fromarray(viz_img)
        img.save('coverage.png')
        
        # Also save a larger version for easier viewing
        img_large = img.resize((self.map_width * 4, self.map_height * 4), Image.NEAREST)
        img_large.save('coverage_large.png')
        
    def save_coverage_plan(self):
        """
        Save the coverage plan to a file for analysis
        """
        plan_data = {
            'run_id': self.run_id,
            'uuid': self.run_uuid,
            'timestamp': datetime.datetime.now().isoformat(),
            'map_resolution': self.map_resolution,
            'map_origin': self.map_origin,
            'map_size': (self.map_width, self.map_height),
            'robot_radius': self.robot_radius,
            'inflation_radius': self.inflation_radius,
            'waypoints': [(x, y) for x, y in self.waypoints],
            'total_waypoints': len(self.waypoints)
        }
        
        with open(os.path.join(self.data_dir, 'coverage_plan.json'), 'w') as f:
            json.dump(plan_data, f, indent=2)
            
        # Save plan image
        self.update_coverage_visualization()
        shutil.copy('coverage.png', os.path.join(self.data_dir, 'initial_plan.png'))
    
    def save_coverage_results(self):
        """
        Save the final coverage results for analysis and ML integration
        """
        # Calculate coverage statistics
        free_cells = np.sum(self.map_data == 0)
        covered_cells = np.sum(self.coverage_grid)
        coverage_pct = (covered_cells / free_cells) * 100 if free_cells > 0 else 0
        
        # Save results
        results = {
            'run_id': self.run_id,
            'uuid': self.run_uuid,
            'timestamp': datetime.datetime.now().isoformat(),
            'total_free_cells': int(free_cells),
            'covered_cells': int(covered_cells),
            'coverage_percentage': float(coverage_pct),
            'exploration_completed': self.exploration_completed,
            'total_waypoints': len(self.waypoints),
            'visited_waypoints': self.current_waypoint_index
        }
        
        with open(os.path.join(self.data_dir, 'coverage_results.json'), 'w') as f:
            json.dump(results, f, indent=2)
            
        # Save ML metadata for later integration
        ml_metadata = {
            'coverage_run': {
                'run_id': self.run_id,
                'dataset_version': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                'coverage_percentage': float(coverage_pct),
                'total_area_m2': float(free_cells * self.map_resolution * self.map_resolution),
                'robot_radius_m': float(self.robot_radius),
                'algorithm': 'boustrophedon_decomposition',
                'tags': {
                    'source': 'webots_simulation',
                    'environment': 'indoor',
                    'completion': 'success' if coverage_pct > 90 else 'partial'
                }
            }
        }
        
        with open(os.path.join(self.data_dir, 'ml_metadata.json'), 'w') as f:
            json.dump(ml_metadata, f, indent=2)
            
        # Save final coverage image
        self.update_coverage_visualization()
        shutil.copy('coverage.png', os.path.join(self.data_dir, 'final_coverage.png'))
        shutil.copy('coverage_large.png', os.path.join(self.data_dir, 'final_coverage_large.png'))

def main():
    rclpy.init()
    node = CoveragePlanner()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Coverage planner stopped by user")
    finally:
        # Save final results if not already done
        if hasattr(node, 'map') and node.map is not None:
            node.save_coverage_results()
            
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
