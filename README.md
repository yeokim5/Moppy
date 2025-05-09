# Floor mopping robot Moppy.

General Flow

- Simulate a room in Webots → Capture LIDAR/camera data → Save as CSV/images.
- Run Apache Airflow DAG to clean data → Extract edges with OpenCV.
- Train a PyTorch CNN to detect obstacles → Save model.
- Automate training with GitHub Actions → Track with MLflow.
- Containerize inference service → Deploy with Kubernetes.
- Optimize model with TensorRT → Run on Jetson with OTA updates.
- Monitor accuracy with Prometheus/Grafana → Retrain if needed

# Raspberry Pi Project for Perception ML Ops - Simulation Testing

This document outlines how to test the simulation environment to ensure all components are working correctly before proceeding to the data processing stage.

## Prerequisites

- ROS 2 Humble
- Webots simulation environment
- Andino robot packages properly installed
- All simulation components built and sourced

## Testing the Simulation Environment

Follow these steps to verify that your simulation setup is complete and functioning properly:

### 1. Start the Webots Simulation

```bash
# Source ROS environment
source /opt/ros/humble/setup.bash
source install/local_setup.bash

# Launch the Andino robot in Webots simulation (use apartment.wbt for a more complex environment)
ros2 launch andino_webots andino_webots.launch.py world:=apartment.wbt
```

### 2. Verify the Simulation Setup

Run the check script to ensure all required topics and nodes are available:

```bash
./check_andino_webots.sh
```

This script will verify that:
- All sensor topics are active
- Robot model is loaded correctly
- Control interfaces are functioning

### 3. Test Basic Data Collection

In a new terminal, run the data collection script:

```bash
cd src/simulation/ros2_ws
source /opt/ros/humble/setup.bash
source ../../install/local_setup.bash

# Run the data collection script for a short duration (60 seconds)
./src/data_capture/collect_data.sh --duration=60
```

### 4. Test with Coverage Planner

For more advanced navigation and complete room coverage:

```bash
cd src/simulation/ros2_ws
source /opt/ros/humble/setup.bash
source ../../install/local_setup.bash

# Run with the coverage planner for better navigation
./src/data_capture/collect_data.sh --duration=120 --use-coverage-planner
```

### 5. Validate the Collected Data

After data collection completes, check the output directory (typically in `./data/[timestamp]`) for:
- LIDAR data CSV files
- Camera images 
- Validation reports
- Data labels

### 6. Test End-to-End Pipeline

Ensure the data preparation for machine learning works correctly:

```bash
# Using the most recent data collection
cd src/simulation/ros2_ws
source /opt/ros/humble/setup.bash
source ../../install/local_setup.bash

# Prepare data for ML
python3 src/data_capture/prepare_for_ml.py --data-dir ./data/latest
```

## Expected Results

### Webots Simulation
- The Andino robot should appear in the simulated environment
- You should be able to see the robot's camera view and LIDAR visualization

### Check Script
- All sensor topics should show `[OK]`
- Robot model and control should show `[OK]`

### Data Collection
- Terminal should show that LIDAR and camera data are being captured
- No error messages should appear
- At the end, you should see a summary of the data collected

### Data Validation
- In the data directory, you should find:
  - A `raw` folder with LIDAR data
  - An `images` folder with camera images
  - A `metadata` folder with validation reports
  - A `labeled` folder (created during processing)

### ML Data Preparation
- Should complete without errors
- Should create structured data ready for the next stage

## Troubleshooting

### Common Issues

1. **Missing mesh files**: Ensure mesh files are properly copied using the `copy_mesh_files.sh` script
2. **Robot not moving**: Check if the `/cmd_vel` topic is active and receiving commands
3. **Sensors not reporting data**: Verify the sensor topics are published correctly
4. **Data not being collected**: Check the file permissions in your data directory

If all tests complete successfully, your simulation environment is working correctly and you're ready to proceed to the data processing stage!
