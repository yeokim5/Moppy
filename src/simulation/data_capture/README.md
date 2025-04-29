# Data Capture Pipeline for Andino Robot

This module contains the necessary tools to collect sensor data from the Andino robot in the Webots simulation environment.

## Prerequisites

Before using these scripts, make sure you have successfully:

1. Set up the Webots simulation environment
2. Created 3D room models
3. Implemented the Andino robot model
4. Configured LIDAR and camera sensors
5. Successfully run and saved maps using SLAM

## Available Scripts

### 1. Room Simulator (`room_simulator.py`)

Automates robot movement to collect data from various room layouts.

```bash
# Run in a small apartment layout for 5 minutes (300 seconds)
./room_simulator.py --room small_apartment --exploration-time 300

# Run in office layout with higher data capture rate
./room_simulator.py --room office --capture-rate 15.0
```

### 2. LIDAR Data Capture (`lidar_capture.py`)

Captures LIDAR data and saves it to CSV files.

```bash
# Basic usage
./lidar_capture.py --output-dir ./data

# Capture at 20Hz for 5 minutes
./lidar_capture.py --output-dir ./data --rate 20.0 --duration 300

# Custom file prefix
./lidar_capture.py --output-dir ./data --prefix my_experiment
```

### 3. Camera Capture (`camera_capture.py`)

Captures camera images and saves them with associated metadata.

```bash
# Basic usage
./camera_capture.py --output-dir ./data

# Capture at lower rate and use PNG format
./camera_capture.py --output-dir ./data --rate 2.0 --format png

# Capture for a specific duration
./camera_capture.py --output-dir ./data --duration 180
```

### 4. Data Validation (`data_validation.py`)

Validates the quality and format of captured data.

```bash
# Validate data in the data directory
./data_validation.py --data-dir ./data

# Save validation results to a custom location
./data_validation.py --data-dir ./data --output-dir ./validation_results

# Run in quiet mode (less output)
./data_validation.py --data-dir ./data --quiet
```

## Workflow Example

Here's a complete workflow example to capture both LIDAR and camera data while the robot explores a room:

1. Launch the Andino robot in Webots:

```bash
source /opt/ros/humble/setup.bash
source install/local_setup.bash
export WEBOTS_HOME=/mnt/c/Program\ Files/Webots
ros2 launch andino_webots andino_webots_windows.launch.py
```

2. Start the data collection in separate terminals:

```bash
# Terminal 1: Run SLAM
ros2 launch andino_slam slam_toolbox_online_async.launch.py

# Terminal 2: Start LIDAR data capture
mkdir -p data
./src/data_capture/lidar_capture.py --output-dir ./data --rate 10.0

# Terminal 3: Start camera data capture
./src/data_capture/camera_capture.py --output-dir ./data --rate 5.0

# Terminal 4: Run the room simulator for automated exploration
./src/data_capture/room_simulator.py --room small_apartment --exploration-time 300
```

3. After data collection, validate the data:

```bash
./src/data_capture/data_validation.py --data-dir ./data
```

## Output Data Format

### LIDAR Data

- CSV files with timestamp, robot position, and range readings for each angle
- Each file represents a complete data collection session

### Camera Data

- Images saved in the specified format (JPG/PNG) in the `images` subdirectory
- Metadata CSV file with timestamps, positions, and filenames

## Requirements

These scripts require the following Python packages:
- rclpy (ROS 2 Python client)
- numpy
- pandas
- cv2 (OpenCV)
- matplotlib (for visualization)
- PIL (Python Imaging Library)

You can install non-ROS dependencies using:

```bash
pip install numpy pandas opencv-python matplotlib pillow
``` 