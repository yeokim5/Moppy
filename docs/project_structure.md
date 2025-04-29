# Moppy Project Structure

## Overview

This is the file structure for the Moppy floor mopping robot project. The structure is organized to support the full development lifecycle as described in the README.

## Directory Structure

..

## Component Descriptions

### Simulation

- **Webots Simulation**: Virtual environment where the robot operates
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
