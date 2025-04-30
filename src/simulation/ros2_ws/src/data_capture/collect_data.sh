#!/bin/bash

# collect_data.sh - Script to run all data collection tools for the Andino robot

# Default values
OUTPUT_DIR="./data"
DURATION=30  # 5 minutes
LIDAR_RATE=10.0
CAMERA_RATE=5.0
ROOM_TYPE="small_apartment"

# Print usage information
function print_usage {
    echo "Usage: $0 [OPTIONS]"
    echo "Collect sensor data from the Andino robot."
    echo ""
    echo "Options:"
    echo "  -o, --output-dir DIR    Output directory (default: ./data)"
    echo "  -d, --duration SEC      Collection duration in seconds (default: 300)"
    echo "  -l, --lidar-rate HZ     LIDAR capture rate in Hz (default: 10.0)"
    echo "  -c, --camera-rate HZ    Camera capture rate in Hz (default: 5.0)"
    echo "  -r, --room TYPE         Room type (small_apartment|office|warehouse) (default: small_apartment)"
    echo "  -h, --help              Display this help message"
    echo ""
    echo "Example:"
    echo "  $0 --output-dir ./my_data --duration 600 --room office"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -d|--duration)
            DURATION="$2"
            shift 2
            ;;
        -l|--lidar-rate)
            LIDAR_RATE="$2"
            shift 2
            ;;
        -c|--camera-rate)
            CAMERA_RATE="$2"
            shift 2
            ;;
        -r|--room)
            ROOM_TYPE="$2"
            shift 2
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Check if ROS is sourced
if ! command -v ros2 &> /dev/null; then
    echo "Error: ROS 2 commands not found. Make sure you've sourced your ROS installation."
    echo "Run: source /opt/ros/humble/setup.bash"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo "Creating output directory: $OUTPUT_DIR"

# Start LIDAR data capture in background
echo "Starting LIDAR data capture at $LIDAR_RATE Hz..."
./src/data_capture/lidar_capture.py --output-dir "$OUTPUT_DIR" --rate "$LIDAR_RATE" --duration "$DURATION" &
LIDAR_PID=$!

# Start camera data capture in background
echo "Starting camera data capture at $CAMERA_RATE Hz..."
./src/data_capture/camera_capture.py --output-dir "$OUTPUT_DIR" --rate "$CAMERA_RATE" --duration "$DURATION" &
CAMERA_PID=$!

# Start room simulator
echo "Starting room simulator for $DURATION seconds in $ROOM_TYPE layout..."
./src/data_capture/room_simulator.py --room "$ROOM_TYPE" --exploration-time "$DURATION"

# Wait for background processes to complete
wait $LIDAR_PID
wait $CAMERA_PID

# Validate collected data
echo "Validating collected data..."
./src/data_capture/data_validation.py --data-dir "$OUTPUT_DIR"

echo "Data collection complete. Results saved to $OUTPUT_DIR" 