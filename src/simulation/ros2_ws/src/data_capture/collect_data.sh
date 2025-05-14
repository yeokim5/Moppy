#!/bin/bash

# Integrated script to collect, label, and organize data for ML training
# This script should be run after setting up the ROS environment and starting the simulation

# Configuration
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATA_DIR="./data/${TIMESTAMP}"
DURATION=300  # Data collection duration in seconds
LIDAR_RATE=10 # Hz
CAMERA_RATE=5 # Hz
IMAGE_FORMAT="jpg"
ROBOT_SPEED=0.15 # Lower speed for better coverage
USE_COVERAGE_PLANNER=false
DATASET_VERSION="v1.${TIMESTAMP}"
RUN_UUID=$(cat /proc/sys/kernel/random/uuid | cut -c-8)
VALIDATE_DATA=true
MLFLOW_READY=true
SHUTDOWN_DELAY=1 # Delay in seconds between stopping processes

# Process command line arguments
for arg in "$@"; do
    case $arg in
        --use-coverage-planner)
            USE_COVERAGE_PLANNER=true
            ;;
        --duration=*)
            DURATION="${arg#*=}"
            ;;
        --lidar-rate=*)
            LIDAR_RATE="${arg#*=}"
            ;;
        --camera-rate=*)
            CAMERA_RATE="${arg#*=}"
            ;;
        --no-validation)
            VALIDATE_DATA=false
            ;;
        --dataset-version=*)
            DATASET_VERSION="${arg#*=}"
            ;;
    esac
done

# Create data directory and subdirectories
mkdir -p "$DATA_DIR"
mkdir -p "$DATA_DIR/images"
mkdir -p "$DATA_DIR/raw"
mkdir -p "$DATA_DIR/metadata"

# Create dataset info file for versioning and ML tracking
echo "Creating dataset metadata..."
cat > "$DATA_DIR/metadata/dataset_info.json" << EOL
{
  "dataset_id": "sim_data_${RUN_UUID}",
  "version": "${DATASET_VERSION}",
  "timestamp": "$(date -Iseconds)",
  "description": "Simulated LIDAR and camera data for obstacle detection and floor classification",
  "collection_parameters": {
    "duration": ${DURATION},
    "lidar_rate": ${LIDAR_RATE},
    "camera_rate": ${CAMERA_RATE},
    "robot_speed": ${ROBOT_SPEED},
    "coverage_planner": ${USE_COVERAGE_PLANNER}
  },
  "formats": {
    "lidar": "CSV with timestamp, position, orientation, and range readings",
    "images": "${IMAGE_FORMAT} files with position metadata CSV"
  }
}
EOL

# Set up ROS environment if not already done
if [ -z "$ROS_DISTRO" ]; then
    echo "Setting up ROS environment..."
    source /opt/ros/humble/setup.bash
    source ../../install/local_setup.bash
fi

# Environment check function
check_environment() {
    echo "Checking environment for data collection..."
    
    # Check if ROS topics are available
    if ! ros2 topic list 2>/dev/null | grep -q "/andino_camera\|/andino_scan"; then
        echo "Warning: Webots topics are not detected."
        echo "If Webots is already running, please ensure the robot is properly spawned."
        return 1
    fi
    
    # Check disk space (at least 1GB free)
    FREE_SPACE=$(df -h . | awk 'NR==2 {print $4}' | sed 's/G//')
    if (( $(echo "$FREE_SPACE < 1" | bc -l) )); then
        echo "Warning: Low disk space. Less than 1GB available."
        return 1
    fi
    
    return 0
}

# Data validation function
validate_data() {
    echo "Validating collected data..."
    
    # Check if LIDAR data was collected
    LIDAR_FILES=$(find "$DATA_DIR" -name "*lidar*.csv" | wc -l)
    if [ "$LIDAR_FILES" -eq 0 ]; then
        echo "Error: No LIDAR data was collected!"
        return 1
    fi
    
    # Check if camera images were collected
    IMAGE_COUNT=$(find "$DATA_DIR/images" -type f | wc -l)
    if [ "$IMAGE_COUNT" -eq 0 ]; then
        echo "Error: No camera images were collected!"
        return 1
    fi
    
    # Check if we collected a reasonable amount of data based on duration and rates
    EXPECTED_LIDAR_COUNT=$((DURATION * LIDAR_RATE / 10))  # Approximate expectation
    EXPECTED_CAMERA_COUNT=$((DURATION * CAMERA_RATE / 10))
    
    if [ "$LIDAR_FILES" -lt "$EXPECTED_LIDAR_COUNT" ]; then
        echo "Warning: Collected fewer LIDAR samples than expected."
    fi
    
    if [ "$IMAGE_COUNT" -lt "$EXPECTED_CAMERA_COUNT" ]; then
        echo "Warning: Collected fewer camera images than expected."
    fi
    
    # Create validation report
    cat > "$DATA_DIR/metadata/validation_report.json" << EOL
{
  "validation_timestamp": "$(date -Iseconds)",
  "dataset_id": "sim_data_${RUN_UUID}",
  "validation_status": "passed",
  "metrics": {
    "lidar_files": ${LIDAR_FILES},
    "image_count": ${IMAGE_COUNT},
    "expected_lidar_min": ${EXPECTED_LIDAR_COUNT},
    "expected_camera_min": ${EXPECTED_CAMERA_COUNT}
  },
  "warnings": [
    $([ "$LIDAR_FILES" -lt "$EXPECTED_LIDAR_COUNT" ] && echo "\"Fewer LIDAR samples than expected\"," || echo "")
    $([ "$IMAGE_COUNT" -lt "$EXPECTED_CAMERA_COUNT" ] && echo "\"Fewer camera images than expected\"," || echo "")
    ""
  ]
}
EOL
    sed -i '$ s/,$//' "$DATA_DIR/metadata/validation_report.json"
    
    echo "Data validation complete."
    return 0
}

# Prepare MLflow tracking metadata
prepare_mlflow_metadata() {
    echo "Preparing MLflow metadata..."
    
    # Calculate sizes
    TOTAL_SIZE=$(du -sk "$DATA_DIR" | cut -f1)
    IMAGES_SIZE=$(du -sk "$DATA_DIR/images" | cut -f1)
    TOTAL_SIZE_MB=$(echo "scale=2; $TOTAL_SIZE/1024" | bc)
    IMAGES_SIZE_MB=$(echo "scale=2; $IMAGES_SIZE/1024" | bc)
    
    # Create MLflow metadata file
    cat > "$DATA_DIR/metadata/mlflow_metadata.json" << EOL
{
  "dataset": {
    "name": "simulation_dataset_${RUN_UUID}",
    "version": "${DATASET_VERSION}",
    "description": "Simulated LIDAR and camera data for obstacle detection and floor classification",
    "size_mb": ${TOTAL_SIZE_MB},
    "metrics": {
      "total_images": ${IMAGE_COUNT},
      "total_duration_sec": ${DURATION}
    },
    "tags": {
      "source": "webots_simulation",
      "environment": "indoor",
      "sensors": "lidar,camera"
    },
    "parameters": {
      "lidar_rate": ${LIDAR_RATE},
      "camera_rate": ${CAMERA_RATE},
      "robot_speed": ${ROBOT_SPEED},
      "coverage_planner": ${USE_COVERAGE_PLANNER}
    }
  }
}
EOL
    
    echo "MLflow metadata prepared."
}

# Graceful shutdown function for ROS nodes
graceful_shutdown() {
    echo "Gracefully shutting down ROS nodes..."
    
    # Stop the movement node first to ensure robot stops
    if [ "$USE_COVERAGE_PLANNER" = true ]; then
        if ps -p $EXPLORER_PID > /dev/null; then
            echo "Stopping coverage planner..."
            kill -SIGINT $EXPLORER_PID 2>/dev/null
            sleep $SHUTDOWN_DELAY
        fi
    else
        if ps -p $SIMULATOR_PID > /dev/null; then
            echo "Stopping room simulator..."
            kill -SIGINT $SIMULATOR_PID 2>/dev/null
            sleep $SHUTDOWN_DELAY
        fi
    fi
    
    # Stop camera node
    if ps -p $CAMERA_PID > /dev/null; then
        echo "Stopping camera capture..."
        kill -SIGINT $CAMERA_PID 2>/dev/null
        sleep $SHUTDOWN_DELAY
    fi
    
    # Stop lidar node
    if ps -p $LIDAR_PID > /dev/null; then
        echo "Stopping LIDAR capture..."
        kill -SIGINT $LIDAR_PID 2>/dev/null
        sleep $SHUTDOWN_DELAY
    fi
    
    # Wait for all processes to terminate
    wait
    
    echo "All ROS nodes have been shut down."
}

# Function to handle cleanup
cleanup() {
    echo "Stopping data collection..."
    
    # Perform graceful shutdown of ROS nodes
    graceful_shutdown
    
    # Copy coverage visualization if it exists
    if [ -f "coverage.png" ]; then
        cp coverage.png "$DATA_DIR/coverage_map.png"
    fi
    if [ -f "coverage_large.png" ]; then
        cp coverage_large.png "$DATA_DIR/coverage_map_large.png"
    fi
    
    # Save map for reference if available
    echo "Saving current map for reference..."
    ros2 run nav2_map_server map_saver_cli -f "$DATA_DIR/reference_map" || echo "Could not save map, continuing anyway..."
    
    # Label and organize the collected data
    echo "Labeling and organizing data..."
    python3 $(dirname "$0")/data_labeler.py --data-dir "$DATA_DIR" --organize
    
    # Validate the collected data if enabled
    if [ "$VALIDATE_DATA" = true ]; then
        validate_data
    fi
    
    # Prepare MLflow metadata if enabled
    if [ "$MLFLOW_READY" = true ]; then
        prepare_mlflow_metadata
    fi
    
    # Create a symlink to the latest data collection
    ln -sf "$DATA_DIR" ./data/latest
    
    echo "Data collection complete."
    echo "Dataset ID: sim_data_${RUN_UUID}"
    echo "Dataset Version: ${DATASET_VERSION}"
    echo "Data saved to $DATA_DIR"
    exit 0
}

# Set up trap for clean exit
trap cleanup SIGINT SIGTERM

# Check environment before proceeding
check_environment
ENV_CHECK=$?
if [ $ENV_CHECK -ne 0 ]; then
    echo "Environment check warnings detected."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Start LIDAR data collection
echo "Starting LIDAR data collection..."
python3 $(dirname "$0")/lidar_capture.py --output-dir "$DATA_DIR/raw" --prefix "lidar_data" --rate $LIDAR_RATE --duration $DURATION &
LIDAR_PID=$!

# Start camera data collection
echo "Starting camera data collection..."
python3 $(dirname "$0")/camera_capture.py --output-dir "$DATA_DIR" --prefix "camera_data" --rate $CAMERA_RATE --format $IMAGE_FORMAT --duration $DURATION &
CAMERA_PID=$!

# Start surface coverage exploration if requested
if [ "$USE_COVERAGE_PLANNER" = true ]; then
    echo "Starting coverage planner for exploration..."
    
    # Check if the Nav2 stack is running
    if ! ros2 service list 2>/dev/null | grep -q "/follow_waypoints/_action/get_result"; then
        echo "Warning: Nav2 follow_waypoints service not found. Coverage planner may not work properly."
    fi
    
    # Check if the map is available
    if ! ros2 topic list 2>/dev/null | grep -q "/map"; then
        echo "Warning: Map topic not found. Coverage planner requires a map to function."
    fi
    
    # Run the coverage planner
    python3 $(dirname "$0")/coverage_planner.py &
    EXPLORER_PID=$!
else
    echo "Coverage planner not enabled. Use --use-coverage-planner flag to enable."
    echo "Using basic room_simulator for robot movement instead..."
    python3 $(dirname "$0")/room_simulator.py --speed $ROBOT_SPEED --duration $DURATION &
    SIMULATOR_PID=$!
fi

# Create README file with collection info
cat > "$DATA_DIR/README.md" << EOL
# Simulation Data Collection

**Dataset ID:** sim_data_${RUN_UUID}
**Version:** ${DATASET_VERSION}
**Date:** $(date -Iseconds)

## Collection Parameters
- Duration: ${DURATION} seconds
- LIDAR rate: ${LIDAR_RATE} Hz
- Camera rate: ${CAMERA_RATE} Hz
- Robot speed: ${ROBOT_SPEED} m/s
- Coverage planner: ${USE_COVERAGE_PLANNER}

## Directory Structure
- \`images/\`: Camera image files
- \`raw/\`: Raw sensor data files
- \`metadata/\`: Dataset metadata and validation info
- \`labeled/\`: (Created after processing) Labeled and organized data

## Next Steps
1. The data in this collection is automatically labeled by the data_labeler.py script
2. For model training, use the files in \`labeled/\` directory
3. MLflow tracking metadata is available in \`metadata/mlflow_metadata.json\`
EOL

# Wait for data collection to complete
echo "Collecting data for $DURATION seconds. Press Ctrl+C to stop early."
sleep $DURATION

# Clean up
cleanup 