# Floor mopping robot Moppy.

General Flow

- Simulate a room in Webots → Capture LIDAR/camera data → Save as CSV/images.
- Run Apache Airflow DAG to clean data → Extract edges with OpenCV.
- Train a PyTorch CNN to detect obstacles → Save model.
- Automate training with GitHub Actions → Track with MLflow.
- Containerize inference service → Deploy with Kubernetes.
- Optimize model with TensorRT → Run on Jetson with OTA updates.
- Monitor accuracy with Prometheus/Grafana → Retrain if needed
