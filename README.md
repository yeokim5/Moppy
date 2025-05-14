# Floor mopping robot Moppy.

General Flow

can you explain this project? "---

## 🧠 Autonomous Floor-Mopping Robot with Hazard Detection

**_Full ML + Robotics Pipeline: Simulation to Real-World Deployment_**
_Designed to demonstrate full-cycle machine learning development and perception system integration for autonomous navigation, tailored to the Machine Learning Engineer – Perception role at Forterra._

---

### 🚀 **Overview**

This project features an autonomous floor-mopping robot that navigates indoor environments while detecting and avoiding hazards (e.g., cables, bricks, power strips) using a perception system built with heterogeneous sensors. It spans the entire ML lifecycle—from simulation and data collection to model training and edge deployment on Raspberry Pi hardware—highlighting skills in perception modeling, real-world deployment, infrastructure maintenance, and collaborative software practices.

---

## ✅ Phase 1: Simulation & Navigation Logic (Webots + ROS2)

**🎯 Goal:** Develop and validate navigation logic in simulation, integrating simulated sensors to prepare for perception tasks.

- [ ] Configure the [**Andino robot in Webots**](https://github.com/Ekumen-OS/andino_webots) with simulated heterogeneous sensors (e.g., RGB camera, depth sensor)
- [ ] Write **Python-based boustrophedon navigation logic** for surface coverage using ROS2
- [ ] Simulate sensor data streams (RGB and depth) to mimic real-world perception inputs
- [ ] Test navigation across complex indoor layouts (e.g., obstacles, corners)
- [ ] Refactor code into a modular, **ROS2-compatible Python package** with clear documentation
- [ ] Add unit tests and set up **CI workflows** using GitHub Actions

> **_Skills Highlighted_**: Python, ROS2, simulation, modular design, automated testing, software engineering best practices.

---

## ✅ Phase 2: Hardware Bring-Up & Real-World Navigation

**🎯 Goal:** Deploy the navigation system on the Raspberry Pi–based Andino robot with real sensors.

- [ ] Assemble the Andino robot using a **Raspberry Pi 4**, RGB-D camera (e.g., RealSense), motor controllers, and battery pack
- [ ] Install **Ubuntu or Raspberry Pi OS**, ROS2, and sensor drivers on the Pi
- [ ] Optimize Python navigation code for **lightweight edge performance**
- [ ] Validate navigation in real-world structured environments (e.g., offices, homes)
- [ ] Evaluate navigation in **semi-structured indoor environments** (e.g., uneven flooring, clutter)
- [ ] Log preliminary sensor data (RGB-D) for perception model training

> **_Skills Highlighted_**: Raspberry Pi robotics, sensor integration, edge performance tuning, deployment testing.

---

## ✅ Phase 3: Dataset Collection & Annotation

**🎯 Goal:** Build a multi-modal dataset for perception, managed with modern workflow tools.

- [ ] Identify and source hazard objects (e.g., cables, bricks, power strips) for training data
- [ ] Capture **RGB and depth data** from the onboard camera during autonomous runs
- [ ] Develop a **Python script** to automate data logging and timestamping
- [ ] Orchestrate data collection using **Metaflow** for reproducibility and pipeline orchestration
- [ ] Annotate data with **Label Studio**, labeling hazards for object detection tasks
- [ ] Export annotations in **YOLO and COCO formats**
- [ ] Upload dataset to **AWS S3** for central access and model training

> **_Skills Highlighted_**: Multi-modal data collection, data pipeline orchestration, AWS storage, dataset engineering.

---

## ✅ Phase 4: Model Training & Lifecycle Management

**🎯 Goal:** Train a lightweight perception model with PyTorch, ensuring it's deployable on Pi hardware.

- [ ] Train a **YOLOv8n object detection model** in PyTorch for hazard detection
- [ ] Preprocess RGB-D data for training using custom Python scripts
- [ ] Track experiments with **Weights & Biases** and evaluate performance (e.g., **mAP \~0.78**)
- [ ] Quantize or prune the model to ensure it runs efficiently on Raspberry Pi
- [ ] Export the model to **ONNX or TorchScript** for optimized inference
- [ ] Design a retraining pipeline using **Metaflow** to update the model as new data becomes available

> **_Skills Highlighted_**: Lightweight ML modeling, training pipelines, model evaluation, lifecycle management.

---

## ✅ Phase 5: Edge Deployment & Real-Time Inference

**🎯 Goal:** Deploy the model on Raspberry Pi for real-time hazard avoidance.

- [ ] Containerize the inference pipeline using **Docker** or run with virtualenv-based deployment
- [ ] Integrate the perception model with the **ROS2 camera feed using Python nodes**
- [ ] Benchmark inference speed on Raspberry Pi (**\~3–5 FPS**) and optimize where possible
- [ ] Connect detection outputs to the navigation logic for real-time hazard avoidance
- [ ] Test the full system in **unstructured indoor environments** with natural obstacles

> **_Skills Highlighted_**: Edge deployment, resource-constrained inference, ROS2 integration, real-time robotics.

---

## ✅ Phase 6: ML Ops & System Packaging

**🎯 Goal:** Automate the ML pipeline and ensure maintainability and portability.

- [ ] Build an end-to-end automation pipeline using **Metaflow**
- [ ] Package the full navigation + perception system in a **Docker container** for reproducibility
- [ ] Implement structured logging for model inference and robot telemetry
- [ ] Sync logs and artifacts to **AWS S3** for remote monitoring and retraining triggers
- [ ] Version control for models, datasets, and system configs
- [ ] Document the system architecture, installation steps, and APIs

> **_Skills Highlighted_**: MLOps, containerization, data logging, reproducibility, cloud integration. "
