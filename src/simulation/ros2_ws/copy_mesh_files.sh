#!/bin/bash

# Create destination directories in Windows filesystem
mkdir -p /mnt/c/webots_meshes/andino/
mkdir -p /mnt/c/webots_meshes/sensors/
mkdir -p /mnt/c/webots_meshes/components/

# Copy andino mesh files
cp -v /home/yeokim/ros2_ws/install/andino_description/share/andino_description/meshes/andino/* /mnt/c/webots_meshes/andino/

# Copy sensor mesh files
cp -v /home/yeokim/ros2_ws/install/andino_description/share/andino_description/meshes/sensors/* /mnt/c/webots_meshes/sensors/

# Copy component mesh files
cp -v /home/yeokim/ros2_ws/install/andino_description/share/andino_description/meshes/components/* /mnt/c/webots_meshes/components/

echo "All mesh files copied to Windows-accessible location." 