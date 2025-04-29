#!/usr/bin/env python3

import os
import sys
import numpy as np
import csv
import datetime
import argparse
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import tf2_ros
from tf2_ros import TransformException
import threading
import time
import math

class LidarCapture(Node):
    """
    LidarCapture subscribes to LIDAR data from the robot and saves it to CSV files,
    also capturing robot position for data correlation.
    """
    
    def __init__(self, output_dir, prefix, capture_rate):
        super().__init__('lidar_capture')
        
        # Setup parameters
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.prefix = prefix
        self.capture_rate = capture_rate
        
        # Initialize data containers
        self.latest_scan = None
        self.latest_odom = None
        self.scan_lock = threading.Lock()
        self.odom_lock = threading.Lock()
        
        # Set up timestamp for run ID
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_id = f"{self.prefix}_{self.timestamp}"
        
        # Set up CSV file
        self.csv_filename = os.path.join(self.output_dir, f"{self.run_id}_lidar.csv")
        self.csv_file = open(self.csv_filename, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write CSV header
        header = ['timestamp', 'x_position', 'y_position', 'theta']
        # Add columns for each LIDAR angle
        # We'll update this once we receive the first scan to know how many angles
        self.header_written = False
        
        # Set up subscribers
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/andino_scan',
            self.scan_callback,
            10)
        
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        
        # Set up timer for data capture
        self.timer = self.create_timer(1.0 / capture_rate, self.capture_data)
        
        self.get_logger().info(
            f"LIDAR capture initialized. Saving data to {self.csv_filename} at {capture_rate} Hz"
        )
    
    def scan_callback(self, msg):
        """Callback function for when new LIDAR scan data arrives."""
        with self.scan_lock:
            self.latest_scan = msg
            
            # If this is our first scan, complete the CSV header
            if not self.header_written and self.latest_scan is not None:
                header = ['timestamp', 'x_position', 'y_position', 'theta']
                # Add columns for each LIDAR angle
                num_readings = len(self.latest_scan.ranges)
                angle_min = self.latest_scan.angle_min
                angle_max = self.latest_scan.angle_max
                angle_increment = self.latest_scan.angle_increment
                
                for i in range(num_readings):
                    angle = angle_min + i * angle_increment
                    header.append(f"range_{i}_{angle:.4f}")
                
                self.csv_writer.writerow(header)
                self.header_written = True
    
    def odom_callback(self, msg):
        """Callback function for when new odometry data arrives."""
        with self.odom_lock:
            self.latest_odom = msg
    
    def capture_data(self):
        """Timer callback to capture and save data at the specified rate."""
        with self.scan_lock, self.odom_lock:
            if self.latest_scan is None or self.latest_odom is None:
                return  # Not enough data yet
            
            # Get current timestamp
            timestamp = self.get_clock().now().to_msg().sec + self.get_clock().now().to_msg().nanosec / 1e9
            
            # Extract position and orientation
            x = self.latest_odom.pose.pose.position.x
            y = self.latest_odom.pose.pose.position.y
            
            # Convert quaternion to yaw (theta)
            q = self.latest_odom.pose.pose.orientation
            theta = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 
                              1.0 - 2.0 * (q.y * q.y + q.z * q.z))
            
            # Start building row with position data
            row = [timestamp, x, y, theta]
            
            # Add all range readings
            row.extend(self.latest_scan.ranges)
            
            # Write to CSV
            self.csv_writer.writerow(row)
            
            # Log periodically
            if int(timestamp) % 10 == 0:  # Log every ~10 seconds
                self.get_logger().info(f"Captured data at position: ({x:.2f}, {y:.2f})")
    
    def __del__(self):
        """Destructor to ensure file is closed properly."""
        if hasattr(self, 'csv_file') and self.csv_file is not None:
            self.csv_file.close()
            self.get_logger().info(f"Closed output file: {self.csv_filename}")

def main():
    parser = argparse.ArgumentParser(description='Capture LIDAR data from the robot')
    parser.add_argument('--output-dir', type=str, default='./data',
                        help='Directory to save captured data')
    parser.add_argument('--prefix', type=str, default='lidar_data',
                        help='Prefix for output files')
    parser.add_argument('--rate', type=float, default=10.0,
                        help='Capture rate in Hz')
    parser.add_argument('--duration', type=int, default=0,
                        help='Capture duration in seconds (0 = run until terminated)')
    
    args, unknown = parser.parse_known_args()
    
    # Initialize ROS
    rclpy.init()
    node = LidarCapture(args.output_dir, args.prefix, args.rate)
    
    try:
        # Run for specified duration or until Ctrl+C
        if args.duration > 0:
            end_time = time.time() + args.duration
            while rclpy.ok() and (time.time() < end_time):
                rclpy.spin_once(node, timeout_sec=0.1)
        else:
            rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("LIDAR capture stopped by user")
    finally:
        # Cleanup
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main() 