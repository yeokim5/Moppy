#!/usr/bin/env python3
import rclpy, os, time, cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver_node')

        # ── parameters ──────────────────────────
        self.declare_parameter('image_topic', '/image_raw')
        self.declare_parameter('output_dir',
                               '~/Downloads/Moppy/ml_pipeline/artifacts/raw_images')
        self.declare_parameter('period_sec', 1.0)        # ▶ save interval

        topic      = self.get_parameter('image_topic').value
        self.period= self.get_parameter('period_sec').value   # ▶
        self.out   = os.path.expanduser(self.get_parameter('output_dir').value)
        os.makedirs(self.out, exist_ok=True)

        # ── ROS entities ────────────────────────
        self.bridge = CvBridge()
        self.current_frame = None
        self.create_subscription(Image, topic, self.image_cb, 10)
        self.create_timer(self.period, self.autosave_cb)      # ▶

        self.get_logger().info(
            f'Listening to {topic}; auto‑saving every {self.period}s → {self.out}')

    # topic callback
    def image_cb(self, msg):
        try:
            self.current_frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge conversion failed: {e}')

    # timer callback  (fires once per second)  ▶
    def autosave_cb(self):
        if self.current_frame is None:
            return
        fname = os.path.join(self.out, f'image_{int(time.time())}.png')
        cv2.imwrite(fname, self.current_frame)
        self.get_logger().debug(f'Saved {fname}')

def main(args=None):
    rclpy.init(args=args)
    node = ImageSaver()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
