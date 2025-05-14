#!/usr/bin/env python3

# A simple subscriber that keeps the camera active
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class CameraActivator(Node):
    def __init__(self):
        super().__init__('camera_activator')
        # Create a subscription to the camera topic
        self.subscription = self.create_subscription(
            Image,
            '/andino_camera/image_color',
            self.callback,
            10)
        self.get_logger().info('Camera activator started. The camera should now be active in Webots.')
    
    def callback(self, msg):
        # We don't need to do anything with the message, just receive it
        pass

def main(args=None):
    rclpy.init(args=args)
    camera_activator = CameraActivator()
    rclpy.spin(camera_activator)
    camera_activator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 