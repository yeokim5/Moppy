#!/usr/bin/env python3

import os
import sys
import argparse
import datetime
import threading
import time
import numpy as np
import cv2
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from nav_msgs.msg import Odometry
import json
import csv

class CameraCapture(Node):
    """
    CameraCapture subscribes to camera data from the robot and saves images,
    along with metadata about robot position and orientation.
    """
    
    def __init__(self, output_dir, prefix, capture_rate, image_format='jpg'):
        super().__init__('camera_capture')
        
        # Setup parameters
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, 'images')
        os.makedirs(self.images_dir, exist_ok=True)
        
        self.prefix = prefix
        self.capture_rate = capture_rate
        self.image_format = image_format.lower()
        
        # Initialize data containers
        self.latest_image = None
        self.latest_camera_info = None
        self.latest_odom = None
        self.image_lock = threading.Lock()
        self.camera_info_lock = threading.Lock()
        self.odom_lock = threading.Lock()
        
        # Set up timestamp for run ID
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_id = f"{self.prefix}_{self.timestamp}"
        
        # Set up metadata CSV file
        self.metadata_file = os.path.join(output_dir, f"{self.run_id}_camera_metadata.csv")
        self.csv_file = open(self.metadata_file, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write metadata header
        self.csv_writer.writerow([
            'timestamp', 'image_filename', 'x_position', 'y_position', 'theta',
            'width', 'height', 'encoding'
        ])
        
        # Initialize cv_bridge
        self.bridge = CvBridge()
        
        # Set up subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/andino_camera/image_color',  # Adjust topic name based on your robot's camera
            self.image_callback,
            10)
        
        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            '/andino_camera/camera_info',  # Adjust topic name based on your robot
            self.camera_info_callback,
            10)
        
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        
        # Set up timer for data capture
        self.capture_count = 0
        self.timer = self.create_timer(1.0 / capture_rate, self.capture_data)
        
        self.get_logger().info(
            f"Camera capture initialized. Saving data to {output_dir} at {capture_rate} Hz"
        )
    
    def image_callback(self, msg):
        """Callback function for when new camera image arrives."""
        with self.image_lock:
            self.latest_image = msg
    
    def camera_info_callback(self, msg):
        """Callback function for when new camera info arrives."""
        with self.camera_info_lock:
            self.latest_camera_info = msg
    
    def odom_callback(self, msg):
        """Callback function for when new odometry data arrives."""
        with self.odom_lock:
            self.latest_odom = msg
    
    def capture_data(self):
        """Timer callback to capture and save data at the specified rate."""
        with self.image_lock, self.odom_lock:
            if self.latest_image is None or self.latest_odom is None:
                return  # Not enough data yet
            
            # Get current timestamp
            timestamp = self.get_clock().now().to_msg().sec + self.get_clock().now().to_msg().nanosec / 1e9
            
            # Extract position and orientation
            x = self.latest_odom.pose.pose.position.x
            y = self.latest_odom.pose.pose.position.y
            
            # Convert quaternion to yaw (theta)
            q = self.latest_odom.pose.pose.orientation
            theta = np.arctan2(2.0 * (q.w * q.z + q.x * q.y), 
                              1.0 - 2.0 * (q.y * q.y + q.z * q.z))
            
            # Convert ROS Image to OpenCV format
            try:
                cv_image = self.bridge.imgmsg_to_cv2(self.latest_image, desired_encoding='bgr8')
                
                # Generate filename
                self.capture_count += 1
                filename = f"{self.run_id}_{self.capture_count:06d}.{self.image_format}"
                filepath = os.path.join(self.images_dir, filename)
                
                # Save image
                if self.image_format == 'jpg' or self.image_format == 'jpeg':
                    cv2.imwrite(filepath, cv_image, [cv2.IMWRITE_JPEG_QUALITY, 95])
                elif self.image_format == 'png':
                    cv2.imwrite(filepath, cv_image)
                else:
                    cv2.imwrite(filepath, cv_image)  # Default format
                
                # Write metadata
                self.csv_writer.writerow([
                    timestamp,
                    filename,
                    x,
                    y,
                    theta,
                    self.latest_image.width,
                    self.latest_image.height,
                    self.latest_image.encoding
                ])
                
                # Log periodically
                if self.capture_count % 100 == 0:
                    self.get_logger().info(f"Captured {self.capture_count} images")
                    
            except Exception as e:
                self.get_logger().error(f"Error processing image: {e}")
    
    def __del__(self):
        """Destructor to ensure file is closed properly."""
        if hasattr(self, 'csv_file') and self.csv_file is not None:
            self.csv_file.close()
            self.get_logger().info(f"Closed metadata file: {self.metadata_file}")

def main():
    parser = argparse.ArgumentParser(description='Capture camera data from the robot')
    parser.add_argument('--output-dir', type=str, default='./data',
                        help='Directory to save captured data')
    parser.add_argument('--prefix', type=str, default='camera_data',
                        help='Prefix for output files')
    parser.add_argument('--rate', type=float, default=5.0,
                        help='Capture rate in Hz')
    parser.add_argument('--format', type=str, default='jpg',
                        choices=['jpg', 'jpeg', 'png'],
                        help='Image format to save (jpg, png)')
    parser.add_argument('--duration', type=int, default=0,
                        help='Capture duration in seconds (0 = run until terminated)')
    
    args, unknown = parser.parse_known_args()
    
    # Initialize ROS
    rclpy.init()
    node = CameraCapture(args.output_dir, args.prefix, args.rate, args.format)
    
    try:
        # Run for specified duration or until Ctrl+C
        if args.duration > 0:
            end_time = time.time() + args.duration
            while rclpy.ok() and (time.time() < end_time):
                rclpy.spin_once(node, timeout_sec=0.1)
        else:
            rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Camera capture stopped by user")
    finally:
        # Cleanup
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main() 