#!/usr/bin/env python3

import os
import sys
import argparse
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String
import math
import random
import time

class RoomSimulator(Node):
    """
    RoomSimulator provides automated control of the Andino robot in the Webots simulation
    for collecting sensor data in various room layouts.
    """
    
    def __init__(self, config):
        super().__init__('room_simulator')
        
        # Store configuration
        self.config = config
        self.get_logger().info(f"Using room configuration: {self.config['room_name']}")
        
        # Set up publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        
        # Robot state
        self.position = None
        self.orientation = None
        self.linear_velocity = None
        self.angular_velocity = None
        
        # Setup timers for robot control and data capture
        self.control_timer = self.create_timer(0.1, self.control_loop)  # 10Hz control loop
        self.data_capture_timer = self.create_timer(1.0 / self.config['capture_rate'], 
                                                   self.trigger_data_capture)
        
        # Exploration parameters
        self.exploration_mode = 'random'  # 'random', 'grid', 'wall_follow'
        self.obstacle_detected = False
        self.turn_direction = 1  # 1 for right, -1 for left
        self.random_turn_time = 0.0
        
        self.get_logger().info('Room simulator initialized and ready to collect data')
        
    def odom_callback(self, msg):
        """Process odometry data to track robot position and velocity."""
        self.position = msg.pose.pose.position
        self.orientation = msg.pose.pose.orientation
        self.linear_velocity = msg.twist.twist.linear
        self.angular_velocity = msg.twist.twist.angular
        
    def trigger_data_capture(self):
        """Signal to capture data from sensors at the specified rate."""
        # This will be enhanced later to trigger actual data capture
        self.get_logger().debug('Triggering data capture')
        
    def control_loop(self):
        """Main control loop for moving the robot around the environment."""
        if self.position is None:
            return  # Wait until we have received odometry data
        
        cmd = Twist()
        
        # Simple obstacle avoidance (will be enhanced with actual sensor data)
        if self.obstacle_detected:
            # Turn to avoid obstacle
            cmd.angular.z = 0.5 * self.turn_direction
            cmd.linear.x = 0.0
        else:
            # Standard exploration behavior
            if self.exploration_mode == 'random':
                # Random exploration
                if self.random_turn_time > 0:
                    self.random_turn_time -= 0.1  # Decrement timer
                    cmd.angular.z = 0.5 * self.turn_direction
                    cmd.linear.x = 0.05
                else:
                    cmd.linear.x = 0.2  # Go forward
                    
                    # Occasionally make random turns
                    if random.random() < 0.05:  # 5% chance per control cycle
                        self.random_turn_time = random.uniform(1.0, 3.0)
                        self.turn_direction = random.choice([-1, 1])
        
        # Publish velocity command
        self.cmd_vel_pub.publish(cmd)

def get_default_map_path():
    """Find a suitable map from installed packages."""
    possible_maps = [
        '/install/webots_ros2_tiago/share/webots_ros2_tiago/resource/map.yaml',
        '/install/webots_ros2_epuck/share/webots_ros2_epuck/resource/epuck_world_map.yaml',
        '/install/webots_ros2_turtlebot/share/webots_ros2_turtlebot/resource/turtlebot3_burger_example_map.yaml'
    ]
    
    # Get workspace root directory
    ros_ws = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    for rel_path in possible_maps:
        full_path = os.path.join(ros_ws, rel_path.lstrip('/'))
        if os.path.exists(full_path):
            return full_path
            
    # If no map is found, return None
    return None

def load_room_config(room_name):
    """Load room configuration based on room name."""
    # Try to find a default map
    default_map = get_default_map_path()
    
    # In a real implementation, this would load from a config file
    # For now, we'll just return some default configurations
    configs = {
        'small_apartment': {
            'room_name': 'small_apartment',
            'size': 'small',
            'capture_rate': 5.0,  # Hz
            'exploration_time': 30,  # seconds
            'map_path': default_map,
        },
        'office': {
            'room_name': 'office',
            'size': 'medium',
            'capture_rate': 10.0,  # Hz
            'exploration_time': 600,  # seconds
            'map_path': default_map,
        },
        'warehouse': {
            'room_name': 'warehouse',
            'size': 'large',
            'capture_rate': 20.0,  # Hz
            'exploration_time': 1200,  # seconds
            'map_path': default_map,
        }
    }
    
    # Return the requested configuration or a default
    return configs.get(room_name, configs['small_apartment'])

def main():
    parser = argparse.ArgumentParser(description='Room simulator for data collection')
    parser.add_argument('--room', type=str, default='small_apartment',
                        help='Room configuration to use (small_apartment, office, warehouse)')
    parser.add_argument('--capture-rate', type=float, default=None,
                        help='Data capture rate in Hz (overrides config)')
    parser.add_argument('--exploration-time', type=int, default=None,
                        help='Total exploration time in seconds (overrides config)')
    
    args, unknown = parser.parse_known_args()
    
    # Load room configuration
    config = load_room_config(args.room)
    
    # Override with command line arguments if provided
    if args.capture_rate is not None:
        config['capture_rate'] = args.capture_rate
    if args.exploration_time is not None:
        config['exploration_time'] = args.exploration_time
    
    # Initialize ROS node
    rclpy.init()
    node = RoomSimulator(config)
    
    try:
        # Spin the node for the requested exploration time
        timeout = config['exploration_time']
        start_time = time.time()
        while rclpy.ok() and (time.time() - start_time < timeout):
            rclpy.spin_once(node, timeout_sec=0.1)
        
        print(f"Completed {timeout} seconds of exploration in {config['room_name']}")
    except KeyboardInterrupt:
        print("Exploration stopped by user")
    finally:
        # Stop the robot
        stop_cmd = Twist()
        node.cmd_vel_pub.publish(stop_cmd)
        
        # Clean up
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main() 