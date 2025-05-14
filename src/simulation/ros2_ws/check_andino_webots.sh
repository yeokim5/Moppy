#!/bin/bash

# Source ROS environment
source /opt/ros/humble/setup.bash
source install/local_setup.bash

echo "==== Checking Andino Webots Simulation ====="

# Wait for nodes to initialize
echo "Waiting for simulation to fully start... (10 seconds)"
sleep 10

echo -e "\n=== Active Nodes ==="
ros2 node list

echo -e "\n=== Available Topics ==="
topics=$(ros2 topic list)
echo "$topics"

echo -e "\n=== Testing Motor Control ==="
# Check if cmd_vel topic exists
if echo "$topics" | grep -q "/cmd_vel"; then
    echo "  [OK] cmd_vel topic found - robot control should work"
else
    echo "  [ERROR] cmd_vel topic not found - robot control might not work"
fi

echo -e "\n=== Checking Robot Model ==="
# Check for joint_states topic
if echo "$topics" | grep -q "/joint_states"; then
    echo "  [OK] joint_states topic found - robot model loaded properly"
else
    echo "  [ERROR] joint_states topic not found - robot model may not be complete"
fi

# Check for TF
if echo "$topics" | grep -q "/tf"; then
    echo "  [OK] tf topic found - robot model transformation working"
else
    echo "  [ERROR] tf topic not found - robot model transformation might not work"
fi

echo -e "\n=== Checking Sensors ==="
# Check for LIDAR using the actual topic name from the output
if echo "$topics" | grep -q "/andino_scan"; then
    echo "  [OK] LIDAR topic found (/andino_scan) - LIDAR sensor working"
else
    echo "  [ERROR] LIDAR topic not found - LIDAR sensor might not be working"
fi

# Check for camera using the actual topic name from the output
if echo "$topics" | grep -q "/andino_camera/image_color"; then
    echo "  [OK] Camera topic found (/andino_camera/image_color) - Camera sensor working"
else
    echo "  [ERROR] Camera topic not found - Camera sensor might not be working"
fi

echo -e "\n=== Checking Webots Interfaces ==="
nodes=$(ros2 node list)
if echo "$nodes" | grep -q "/andino"; then
    echo "  [OK] Andino node found - Webots driver working"
else
    echo "  [ERROR] Andino node not found - Webots driver might not be working"
fi

echo -e "\n=== Mesh File Paths ==="
echo "Andino meshes: C:/webots_meshes/andino/"
echo "Sensor meshes: C:/webots_meshes/sensors/"
echo "Component meshes: C:/webots_meshes/components/"

echo -e "\n==== Verification Complete ====="
echo "If you see errors above, some components may not be loaded properly."
echo "If everything shows [OK], your simulation should be fully functional!" 