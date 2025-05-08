## **Updated Plan 2: Raspberry Pi Project for Perception ML Ops**

### **1. Simulation**
- [X] Set up the Webots simulation environment to model a virtual robotics scenario.
- [X] Create 3D room models with various layouts and obstacles to simulate real-world environments.
- [X] Implement a robot model with accurate physical properties (e.g., size, weight, movement dynamics).
- [X] Configure LIDAR sensor simulation for distance and spatial data collection.
- [X] Configure camera sensor simulation for visual data capture.
- [X] Create a data capture pipeline to collect data from LIDAR and camera sensors.
- [X] Implement `room_simulator.py` with configuration options (e.g., room size, obstacle types).
- [X] Develop `lidar_capture.py` to collect and save LIDAR sensor data.
- [X] Generate CSV exports of LIDAR data for analysis and model training.
- [X] Capture and save camera image datasets for tasks like obstacle detection and surface classification.
- [X] Implement a labeling mechanism for simulation data (e.g., obstacle types, floor types).
- [X] Validate the quality and format of simulation data to ensure it meets downstream requirements.
- [X] Implement `coverage_planner.py` with the CCPP algorithm using the simulated SLAM map.
- [X] Integrate `coverage_planner.py` with the simulated robot’s navigation system in Webots.
- [X] Test the CCPP algorithm in various simulated room layouts to ensure complete coverage.

---

### **2. Data Processing**
- [ ] Set up an Apache Airflow environment to orchestrate data workflows.
- [ ] Develop `data_cleaning_dag.py` as a workflow to automate data preprocessing.
- [ ] Implement `data_processor.py` with utility functions for data handling.
- [ ] Create preprocessing steps for raw image data, including resizing and normalization.
- [ ] Implement a data augmentation pipeline for images (e.g., flipping, brightness adjustments).
- [ ] Develop feature extraction techniques for obstacle detection and surface classification.
- [ ] Organize processed data into training, validation, and test sets.
- [ ] Implement validation and quality checks to ensure image data integrity.
- [ ] Document data format specifications for use in machine learning models.

---

### **3. Model Development**
- [ ] Design a lightweight CNN architecture (e.g., MobileNet) in `cnn_model.py` optimized for real-time inference.
- [ ] Implement the model definition using PyTorch.
- [ ] Create a training pipeline with hyperparameter tuning (e.g., learning rate, batch size).
- [ ] Implement loss functions and optimization strategies for classification tasks.
- [ ] Develop evaluation metrics: accuracy, precision, recall, and F1-score.
- [ ] Create visualization tools for model performance (e.g., confusion matrices, ROC curves).
- [ ] Implement `mlflow_tracking.py` for integration with MLflow to log experiments.
- [ ] Configure experiment tracking to monitor training runs.
- [ ] Set up a model versioning system to track model iterations.
- [ ] Implement model checkpointing to save progress during training.
- [ ] Export the trained model to TorchScript or ONNX formats for deployment.

---

### **4. CI/CD Pipeline**
- [ ] Configure a GitHub repository structure for version control and collaboration.
- [ ] Create a `train_model.yml` GitHub Actions workflow to automate model training.
- [ ] Set up automated testing for code reliability.
- [ ] Implement code quality checks using tools like black, flake8, and mypy.
- [ ] Configure an MLflow server for centralized experiment tracking.
- [ ] Create a model registry to manage trained models.
- [ ] Set up automated model validation to ensure performance standards.
- [ ] Implement retraining triggers based on performance metrics (e.g., accuracy drops).
- [ ] Configure artifact storage using AWS S3 for models and datasets.
- [ ] Document the CI/CD workflow for reproducibility.
- [ ] Dockerize the training and inference code for consistency across environments.

---

### **5. Model Deployment**
- [ ] Create a Dockerfile for an inference service tailored to the Raspberry Pi.
- [ ] Implement `obstacle_detector.py` as the inference code for real-time predictions.
- [ ] Optimize the model for Raspberry Pi using frameworks like TensorFlow Lite or ONNX Runtime.
- [ ] Configure the deployment for real-time inference on the Raspberry Pi.
- [ ] Develop `ota_updater.py` for over-the-air updates to the deployed model.
- [ ] Test the deployment pipeline on the Raspberry Pi to ensure functionality.
- [ ] Deploy `coverage_planner.py` to the Raspberry Pi for real-world navigation.
- [ ] Implement `map_handler.py` to manage static and dynamic obstacles based on LIDAR and perception data.
- [ ] Integrate `obstacle_detector.py` with `map_handler.py` to update the map with detected obstacles.
- [ ] Implement dynamic replanning in `coverage_planner.py` when new obstacles are detected.
- [ ] Test the integrated system (perception + navigation) on the Raspberry Pi in real-world scenarios.


---

### **6. Monitoring & Maintenance**
- [ ] Implement `prometheus_metrics.py` to export model performance metrics to Prometheus.
- [ ] Configure a Prometheus server to collect and store metrics.
- [ ] Set up Grafana dashboards to visualize model performance over time.
- [ ] Create alert rules to notify of model performance degradation.
- [ ] Implement feedback collection mechanisms (e.g., storing misclassified images for review).
- [ ] Develop accuracy degradation detection to monitor model drift.
- [ ] Create automated retraining triggers based on data drift or performance drops.
- [ ] Set up a logging infrastructure to track system and model behavior.
- [ ] Implement performance benchmarks for inference speed and accuracy.
- [ ] Create maintenance documentation to guide future updates.

---

### **7. Documentation**
- [ ] Complete API documentation for all custom scripts and services.
- [ ] Create user manuals for operating the system.
- [ ] Document operational procedures for running simulations, training, and deployment.
- [ ] Create system architecture diagrams to illustrate the project structure.
- [ ] Write troubleshooting guides for common issues.
- [ ] Document model training and evaluation procedures for transparency.
- [ ] Create deployment guides specific to the Raspberry Pi.
- [ ] Document monitoring setup and alert configurations.
- [ ] Create a project roadmap outlining completed and future steps.
- [ ] Write a project completion report summarizing outcomes.
- [ ] Develop portfolio presentation materials (e.g., blog posts, demo videos).
- [ ] Document the CCPP algorithm and its integration with perception and navigation modules.

---