# Moppy

## Project Structure

```
Moppy/
├── andino_ws/              # ROS 2 workspace
│   └── src/                # ROS 2 packages
│       ├── andino_*        # Copy of Andino git repository
│       ├── perception_node/# Object detection ROS node
│       └── semantic_mapper_node/ # Semantic mapping node
├── ml_pipeline/            # ML development pipeline
│   ├── configs/            # Model configurations
│   ├── data/               # Dataset storage
│   ├── models/             # Trained models
│   ├── notebooks/          # Jupyter notebooks for exploration
│   └── scripts/            # Training and automation scripts
│       ├── utils/
│       ├── train.py
│       ├── evaluate.py
│       ├── export.py
│       └── retrain.py
├── maps/                   # Generated SLAM maps
└── Makefile                # Automation rules
```