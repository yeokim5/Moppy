import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yeokim/Moppy/src/simulation/ros2_ws/install/webots_ros2_epuck'
