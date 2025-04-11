# Moppy Project Structure

## Overview

This is the file structure for the Moppy floor mopping robot project. The structure is organized to support the full development lifecycle as described in the README.

## Directory Structure

```
moppy/
│
├── .github/
│   └── workflows/            # GitHub Actions workflows
│       └── train_model.yml   # Automated model training workflow
│
├── docs/                     # Project documentation
│   └── project_structure.md  # This file
│
├── src/                      # Source code
│   ├── airflow/
│   │   └── dags/             # Apache Airflow DAGs
│   │       └── data_cleaning_dag.py  # DAG for data cleaning pipeline
│   │
│   ├── data/
│   │   ├── raw/              # Raw data from simulation
│   │   └── processed/        # Processed data for model training
│   │   └── data_processor.py # Data processing utilities
│   │
│   ├── deployment/
│   │   ├── kubernetes/       # Kubernetes configuration
│   │   │   └── deployment.yaml  # K8s deployment configuration
│   │   └── updates/          # OTA update system
│   │       └── ota_updater.py  # OTA update mechanism
│   │
│   ├── models/
│   │   ├── inference/        # Model inference code
│   │   │   ├── obstacle_detector.py   # Main obstacle detection inference
│   │   │   └── tensorrt_optimizer.py  # TensorRT optimization
│   │   └── training/         # Model training code
│   │       ├── cnn_model.py        # CNN model definition
│   │       └── mlflow_tracking.py  # MLflow integration
│   │
│   ├── monitoring/
│   │   ├── metrics/          # Metrics collection
│   │   └── prometheus_metrics.py  # Prometheus metrics export
│   │
│   ├── simulation/
│   │   ├── gazebo/           # Gazebo simulation
│   │   │   └── room_simulator.py  # Room simulation
│   │   └── sensors/          # Sensor simulation
│   │       └── lidar_capture.py  # LIDAR data capture
│   │
│   └── config.py             # Global configuration
│
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image definition
└── requirements.txt          # Python dependencies
```

## Component Descriptions

### Simulation

- **Gazebo Simulation**: Virtual environment where the robot operates
- **Sensors**: LIDAR and camera data capture from simulation

### Data Processing

- **Raw Data**: CSV files and images from simulation
- **Processed Data**: Cleaned data and extracted features
- **Airflow DAGs**: Automated data processing pipelines

### Models

- **Training**: CNN model definition and training scripts
- **MLflow Tracking**: Experiment tracking and model versioning
- **Inference**: Optimized model for deployment
- **TensorRT**: Model optimization for Jetson

### Deployment

- **Kubernetes**: Container orchestration
- **OTA Updates**: Over-the-air update system for robot

### Monitoring

- **Prometheus Metrics**: Performance and accuracy metrics
- **Grafana**: Visualization (configured in deployment)
