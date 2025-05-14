# Data Capture Pipeline for Andino Robot

This module contains tools to collect, label, and process sensor data from the Andino robot in the Webots simulation environment.

## Codebase Overview

### Key Components

- **`lidar_capture.py`**: Captures LIDAR sensor data and exports to CSV format with positional information
- **`camera_capture.py`**: Captures camera images with metadata about robot position and orientation
- **`room_simulator.py`**: Controls robot movement patterns for systematic data collection
- **`coverage_planner.py`**: Implements CCPP (Complete Coverage Path Planning) algorithm
- **`data_labeler.py`**: Labels collected data and organizes datasets for ML training
- **`prepare_for_ml.py`**: Prepares the labeled data for ML training with MLflow integration
- **`data_pipeline_config.yaml`**: Configuration file for the entire data processing pipeline
- **`collect_data.sh`**: Integrated script that orchestrates the complete data collection workflow

## Code File Descriptions

### 1. `lidar_capture.py`

LIDAR data collection node that:
- Subscribes to `/andino_scan` and `/odom` topics
- Records LIDAR range readings at configurable frequency
- Exports synchronized position and range data to CSV
- Handles data organization with timestamp and run ID
- Includes command-line interface for controlling capture parameters

```python
# Key classes:
class LidarCapture(Node):  # ROS2 node for LIDAR data collection
```

### 2. `camera_capture.py`

Camera data collection node that:
- Subscribes to camera topics for RGB image capture
- Saves images in specified format (JPG/PNG)
- Creates metadata CSV with image file references and position data
- Synchronizes with odometry data for precise position labeling
- Configurable capture rate and image quality

```python
# Key classes:
class CameraCapture(Node):  # ROS2 node for camera data collection
```

### 3. `room_simulator.py`

Robot movement controller that:
- Implements exploration strategies for thorough room coverage
- Handles obstacle avoidance during data collection
- Publishes velocity commands based on exploration algorithms
- Supports different room layouts and exploration patterns
- Configurable exploration time and movement parameters

```python
# Key classes:
class RoomSimulator(Node):  # Controls robot movement patterns
```

### 4. `coverage_planner.py`

Complete Coverage Path Planning implementation that:
- Processes occupancy grid maps from SLAM
- Implements modified Boustrophedon coverage algorithm
- Generates efficient paths for complete environment coverage
- Publishes path visualization for RViz
- Executes path following with real-time position feedback
- Handles dynamic replanning when needed
- Creates visualizations of coverage progress
- Generates ML-friendly metadata for experiment tracking

```python
# Key classes:
class CoveragePlanner(Node):  # Implements CCPP algorithm
```

### 5. `data_labeler.py`

Data labeling and organization system that:
- Processes raw LIDAR and camera data
- Applies labels for obstacle types and floor types (tile, carpet, wood, other)
- Organizes datasets into train/validation/test splits (70%/15%/15%)
- Creates dataset versioning and tracking information
- Generates statistics and summaries about labeled data
- Prepares MLflow-compatible metadata for ML pipeline integration

```python
# Key classes:
class DataLabeler:  # Handles data labeling and organization
```

### 6. `prepare_for_ml.py`

ML preparation utility that:
- Validates dataset structure and contents
- Generates additional metadata required for ML frameworks
- Creates samples of the data for quick experimentation
- Sets up the data for registration with MLflow
- Prepares detailed reports on dataset characteristics
- Organizes data into ML-friendly directory structure

```python
# Key classes:
class MLDataPreparer:  # Prepares data for ML training
```

### 7. `data_pipeline_config.yaml`

Configuration file that defines:
- Image preprocessing settings (resizing, normalization, augmentation)
- LIDAR data processing parameters
- Data split settings for ML training
- Threshold values for detection tasks
- MLflow tracking configuration
- Model architecture and training parameters
- Deployment settings for the Raspberry Pi
- Airflow DAG configuration for production pipelines

### 8. `collect_data.sh`

Integrated bash script that:
- Orchestrates the complete data collection workflow
- Coordinates parallel execution of data collection components
- Creates timestamped data directories with unique dataset IDs
- Validates environment before data collection starts
- Performs automatic data validation after collection
- Triggers data labeling and organization
- Prepares MLflow metadata for experiment tracking
- Creates detailed documentation with each dataset

## Usage Examples

### Integrated Workflow

For a streamlined data collection experience, use the integrated collection script:

```bash
./src/data_capture/collect_data.sh
```

Advanced options:
```bash
# Collect data for 5 minutes with coverage planner
./src/data_capture/collect_data.sh --duration=300 --use-coverage-planner

# Collect data with custom sensor rates
./src/data_capture/collect_data.sh --lidar-rate=15 --camera-rate=8

# Specify custom dataset version
./src/data_capture/collect_data.sh --dataset-version="experiment_v2.1"
```

### Individual Component Usage

#### LIDAR Data Capture

```bash
# Basic usage
./lidar_capture.py --output-dir ./data

# Capture at 20Hz for 5 minutes
./lidar_capture.py --output-dir ./data --rate 20.0 --duration 300
```

#### Camera Capture

```bash
# Basic usage
./camera_capture.py --output-dir ./data

# Capture at lower rate and use PNG format
./camera_capture.py --output-dir ./data --rate 2.0 --format png
```

#### Coverage Planner

```bash
# Basic usage with path execution
./coverage_planner.py

# View the coverage visualization
# (Coverage visualization is saved to coverage.png and coverage_large.png)
```

#### Data Labeler

```bash
# Basic usage
./data_labeler.py --data-dir ./data

# Label and organize into train/val/test splits
./data_labeler.py --data-dir ./data --organize
```

#### ML Data Preparation

```bash
# Prepare data for ML training
./prepare_for_ml.py --data-dir ./data/latest

# Create only a sample for quick experimentation
./prepare_for_ml.py --data-dir ./data/latest --sample-only --sample-size 10

# Specify custom output directory and config file
./prepare_for_ml.py --data-dir ./data/latest --output-dir ./ml_data --config-file ./custom_config.yaml
```

## Testing the Pipeline

You can test the complete pipeline with these commands:

```bash
# 1. Test data collection with short duration (10 seconds)
./src/data_capture/collect_data.sh --duration=10 --no-validation

# 2. Test data labeling independently
./src/data_capture/data_labeler.py --data-dir ./data/latest --organize

# 3. Test ML preparation with sample creation
./src/data_capture/prepare_for_ml.py --data-dir ./data/latest --sample-only --sample-size 5

# 4. Run complete end-to-end test
./src/data_capture/collect_data.sh --duration=30 --lidar-rate=5 --camera-rate=2 && \
./src/data_capture/prepare_for_ml.py --data-dir ./data/latest

# 5. Test coverage planner visualization (requires ROS2 with map)
ros2 run nav2_map_server map_saver_cli -f test_map && python3 ./src/data_capture/coverage_planner.py
```

## Data Format Specifications

### LIDAR Data

- CSV files with timestamp, robot position, and range readings for each angle
- Each file represents a complete data collection session
- Labeled data includes obstacle presence flags

### Camera Data

- Images saved in the specified format (JPG/PNG) in the `images` subdirectory
- Metadata CSV file with timestamps, positions, and filenames
- Labeled data includes floor type classification (tile, carpet, wood, other)

### Dataset Organization

After data collection and labeling:

- Raw data is stored in the timestamped directory
- Images are stored in the `images` subdirectory
- LIDAR data is stored in the `raw` subdirectory
- Metadata is stored in the `metadata` subdirectory
- Labeled data is organized in the `labeled` subdirectory:
  - Split into train/val/test sets (70%/15%/15%)
  - Each split contains images and CSV files
- ML-ready data is organized in the `ml_ready` subdirectory:
  - Maintains train/val/test splits
  - Contains MLflow artifacts
  - Includes data samples for quick experimentation
  - Provides detailed dataset reports and statistics

### Dataset Versioning

Each dataset is assigned:
- A unique dataset ID
- A version number
- Timestamp information
- A validation report
- MLflow-compatible metadata

## Requirements

These scripts require the following Python packages:
- rclpy (ROS 2 Python client)
- numpy
- pandas
- cv2 (OpenCV)
- matplotlib (for visualization)
- PIL (Python Imaging Library)
- pyyaml (for configuration loading)
- uuid (for unique ID generation)

You can install non-ROS dependencies using:

```bash
pip install numpy pandas opencv-python matplotlib pillow pyyaml
```

## ML Pipeline Integration

The data collection pipeline is designed to integrate seamlessly with MLflow for experiment tracking:

1. Collected and labeled data includes all necessary metadata for ML experiments
2. Directory structure matches what's expected by the ML pipeline
3. `prepare_for_ml.py` creates artifacts that can be directly imported into MLflow
4. `data_pipeline_config.yaml` contains settings for the entire ML workflow
5. Dataset versioning enables reproducible experiments

For ML training, use the files in the `ml_ready` directory with your MLflow setup. 