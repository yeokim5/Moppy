#!/usr/bin/env python3
import rclpy, os, sys, time, threading, cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver_auto')

        # ── parameters ──────────────────────────
        self.declare_parameter('image_topic', '/image_raw')
        self.declare_parameter('output_dir',
                               '~/Downloads/Moppy/ml_pipeline/artifacts/raw_images')
        self.declare_parameter('period_sec', 3.0)

        topic       = self.get_parameter('image_topic').value
        self.period = self.get_parameter('period_sec').value
        self.outdir = os.path.expanduser(self.get_parameter('output_dir').value)
        os.makedirs(self.outdir, exist_ok=True)

        # ── ROS entities ────────────────────────
        self.bridge = CvBridge()
        self.frame  = None
        self.count  = 0
        self.create_subscription(Image, topic, self.image_cb, 10)
        self.create_timer(self.period, self.autosave_cb)

        self.get_logger().info(
            f'Listening to {topic}; auto‑saving every {self.period}s → {self.outdir}')

    # topic callback ---------------------------------------------------------
    def image_cb(self, msg):
        try:
            self.frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge conversion failed: {e}')

    # timer callback ---------------------------------------------------------
    def autosave_cb(self):
        if self.frame is None:
            return
        fname = os.path.join(self.outdir, f'image_{int(time.time())}.png')
        if cv2.imwrite(fname, self.frame):
            self.count += 1
            # Log every save; use .debug if you prefer it quieter
            self.get_logger().info(f'Saved #{self.count}  →  {fname}')
        else:
            self.get_logger().error(f'Failed to write {fname}')

# ── keyboard listener -------------------------------------------------------
def keyboard_listener(node):
    print("Press 'q' then ENTER to quit.")
    for ch in sys.stdin:                       # blocking read line by line
        if ch.strip().lower() == 'q':
            node.get_logger().info("Quit requested — shutting down.")
            rclpy.shutdown()
            break

# ── main --------------------------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = ImageSaver()

    # Start keyboard thread
    threading.Thread(target=keyboard_listener, args=(node,), daemon=True).start()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
