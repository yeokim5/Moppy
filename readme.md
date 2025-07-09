Moppy/
├── andino_hardware/        # Hardware assembly instructions and STL files
├── andino_ws/              # ROS 2 workspace
│   └── src/                # ROS 2 packages
│       ├── andino_bringup/ # Robot bringup launch files
│       ├── andino_slam/    # SLAM configuration
│       ├── perception_node/# Object detection ROS node
│       └── semantic_mapper_node/ # Semantic mapping node
├── ml_pipeline/            # ML development pipeline
│   ├── configs/            # Model configurations
│   ├── data/               # Dataset storage
│   │   ├── raw/            # Raw collected images
│   │   ├── labeled/        # Labeled dataset
│   │   ├── train/          # Training split
│   │   ├── val/            # Validation split
│   │   └── test/           # Test split
│   ├── models/             # Trained models
│   ├── notebooks/          # Jupyter notebooks for exploration
│   └── scripts/            # Training and automation scripts
│       ├── train.py
│       ├── evaluate.py
│       ├── export.py
│       └── retrain.py
├── docs/                   # Project documentation
├── maps/                   # Generated SLAM maps
├── blueprints/             # Final semantic blueprints
└── Makefile                # Automation rules