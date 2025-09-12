# 1 start the robot
cd /home/pi/Downloads/Moppy/andino_ws
source install/setup.bash
ros2 launch andino_bringup andino_robot.launch.py

# 2 start SLAM
cd /home/pi/Downloads/Moppy/andino_ws
source install/setup.bash
ros2 launch andino_slam slam_toolbox_online_async.launch.py

# 3 start keyboard
cd /home/pi/Downloads/Moppy/andino_ws
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r __node:=teleop_twist_keyboard_node

# save map 
ros2 run nav2_map_server map_saver_cli -f my_map

# Detecting object(wallet) : 
python yolo_detect_ncnn.py --model=/home/pi/Downloads/Moppy/ml_pipeline/src/model/best_ncnn_model --source=usb0 --headless --thresh=0.3 --resolution=640x480 --debug_confidence=true 
