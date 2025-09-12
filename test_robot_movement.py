#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class RobotTester(Node):
    def __init__(self):
        super().__init__('robot_tester')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Robot movement tester started')
        
    def test_straight_movement(self):
        """Test if robot moves straight when given forward command"""
        msg = Twist()
        msg.linear.x = 0.2  # Move forward slowly
        msg.angular.z = 0.0  # No rotation
        
        self.get_logger().info('Testing straight movement for 3 seconds...')
        self.get_logger().info('Watch your robot - it should move STRAIGHT forward!')
        
        # Publish for 3 seconds
        for i in range(30):  # 3 seconds at 10Hz
            self.publisher.publish(msg)
            time.sleep(0.1)
            
        # Stop the robot
        stop_msg = Twist()
        self.publisher.publish(stop_msg)
        self.get_logger().info('Movement test complete. Did the robot move straight?')

def main(args=None):
    rclpy.init(args=args)
    tester = RobotTester()
    
    try:
        # Wait a moment for connections
        time.sleep(1)
        tester.test_straight_movement()
        
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the robot
        stop_msg = Twist()
        tester.publisher.publish(stop_msg)
        tester.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
