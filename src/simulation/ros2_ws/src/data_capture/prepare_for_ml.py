#!/usr/bin/env python3

import os
import sys
import argparse
import json
import yaml
import datetime
import pandas as pd
import numpy as np
from PIL import Image
import shutil
import uuid
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ml_preparation.log')
    ]
)
logger = logging.getLogger('prepare_for_ml')

class MLDataPreparer:
    """
    Prepares simulation data for ML training by:
    1. Validating the dataset structure and contents
    2. Generating additional metadata required for ML frameworks
    3. Creating samples of the data for quick experimentation
    4. Setting up the data for registration with MLflow
    """
    
    def __init__(self, data_dir, config_file, output_dir=None):
        """
        Initialize the ML data preparer.
        
        Args:
            data_dir: Directory containing the collected simulation data
            config_file: Path to the data pipeline configuration file
            output_dir: Directory to save the prepared data (default: data_dir/ml_ready)
        """
        self.data_dir = data_dir
        self.config_file = config_file
        self.output_dir = output_dir if output_dir else os.path.join(data_dir, 'ml_ready')
        
        # Load configuration
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load dataset metadata if it exists
        self.dataset_info = self._load_dataset_info()
        
        # Set up unique ID for this preparation run
        self.run_id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def _load_dataset_info(self):
        """Load dataset information from metadata files"""
        try:
            info_path = os.path.join(self.data_dir, 'metadata', 'dataset_info.json')
            if os.path.exists(info_path):
                with open(info_path, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Dataset info file not found at {info_path}")
                return {
                    "dataset_id": f"unknown_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "version": "unknown",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "description": "Unknown dataset - metadata not found"
                }
        except Exception as e:
            logger.error(f"Error loading dataset info: {e}")
            return {}
    
    def validate_dataset(self):
        """Validate the dataset structure and contents"""
        logger.info("Validating dataset structure and contents...")
        
        # Check for required directories
        required_dirs = ['images', 'raw', 'metadata']
        missing_dirs = [d for d in required_dirs if not os.path.isdir(os.path.join(self.data_dir, d))]
        
        if missing_dirs:
            logger.error(f"Missing required directories: {missing_dirs}")
            return False
        
        # Check for labeled data directory (should be created by data_labeler.py)
        labeled_dir = os.path.join(self.data_dir, 'labeled')
        if not os.path.isdir(labeled_dir):
            logger.warning("Labeled data directory not found. Data may not have been labeled yet.")
        
        # Check for image files
        image_files = [f for f in os.listdir(os.path.join(self.data_dir, 'images')) 
                      if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            logger.error("No image files found in images directory")
            return False
        
        # Check for LIDAR data files
        lidar_files = [f for f in os.listdir(os.path.join(self.data_dir, 'raw')) 
                      if f.endswith('.csv') and 'lidar' in f]
        if not lidar_files:
            logger.error("No LIDAR data files found in raw directory")
            return False
        
        # Check for metadata files
        metadata_files = os.listdir(os.path.join(self.data_dir, 'metadata'))
        if not metadata_files:
            logger.warning("No metadata files found in metadata directory")
        
        logger.info(f"Dataset validation completed. Found {len(image_files)} images and {len(lidar_files)} LIDAR files.")
        return True
    
    def prepare_data_sample(self, sample_size=10):
        """
        Prepare a small sample of the data for quick experimentation
        
        Args:
            sample_size: Number of samples to include
        """
        logger.info(f"Preparing data sample with {sample_size} samples...")
        
        # Create sample directory
        sample_dir = os.path.join(self.output_dir, 'sample')
        os.makedirs(sample_dir, exist_ok=True)
        os.makedirs(os.path.join(sample_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(sample_dir, 'lidar'), exist_ok=True)
        
        # Find labeled data
        if os.path.isdir(os.path.join(self.data_dir, 'labeled')):
            # Get camera metadata
            camera_csvs = [f for f in os.listdir(os.path.join(self.data_dir, 'labeled')) 
                          if f.endswith('.csv') and 'camera' in f]
            
            if camera_csvs:
                camera_csv = os.path.join(self.data_dir, 'labeled', camera_csvs[0])
                try:
                    # Read the camera metadata
                    camera_df = pd.read_csv(camera_csv)
                    
                    # Select a random sample
                    sample_df = camera_df.sample(min(sample_size, len(camera_df)))
                    
                    # Copy the selected images
                    for _, row in sample_df.iterrows():
                        if 'image_filename' in row:
                            src_path = os.path.join(self.data_dir, 'images', row['image_filename'])
                            if os.path.exists(src_path):
                                dst_path = os.path.join(sample_dir, 'images', row['image_filename'])
                                shutil.copy2(src_path, dst_path)
                    
                    # Save the sample metadata
                    sample_df.to_csv(os.path.join(sample_dir, 'camera_metadata_sample.csv'), index=False)
                    
                    logger.info(f"Created sample with {len(sample_df)} camera images.")
                except Exception as e:
                    logger.error(f"Error preparing camera sample: {e}")
            
            # Get LIDAR data
            lidar_csvs = [f for f in os.listdir(os.path.join(self.data_dir, 'labeled')) 
                         if f.endswith('.csv') and 'lidar' in f]
            
            if lidar_csvs:
                lidar_csv = os.path.join(self.data_dir, 'labeled', lidar_csvs[0])
                try:
                    # Read the LIDAR data
                    lidar_df = pd.read_csv(lidar_csv)
                    
                    # Select a random sample
                    sample_df = lidar_df.sample(min(sample_size, len(lidar_df)))
                    
                    # Save the sample metadata
                    sample_df.to_csv(os.path.join(sample_dir, 'lidar_data_sample.csv'), index=False)
                    
                    logger.info(f"Created sample with {len(sample_df)} LIDAR readings.")
                except Exception as e:
                    logger.error(f"Error preparing LIDAR sample: {e}")
        else:
            logger.warning("Labeled data directory not found. Cannot create sample.")
    
    def prepare_mlflow_artifacts(self):
        """Prepare artifacts for MLflow tracking"""
        logger.info("Preparing MLflow artifacts...")
        
        # Create MLflow artifacts directory
        mlflow_dir = os.path.join(self.output_dir, 'mlflow')
        os.makedirs(mlflow_dir, exist_ok=True)
        
        # Copy existing MLflow metadata if available
        mlflow_metadata_path = os.path.join(self.data_dir, 'metadata', 'mlflow_metadata.json')
        if os.path.exists(mlflow_metadata_path):
            with open(mlflow_metadata_path, 'r') as f:
                mlflow_metadata = json.load(f)
        else:
            # Create basic MLflow metadata
            mlflow_metadata = {
                "dataset": {
                    "name": f"simulation_dataset_{self.dataset_info.get('dataset_id', 'unknown')}",
                    "version": self.dataset_info.get('version', 'unknown'),
                    "description": "Simulated LIDAR and camera data for obstacle detection and floor classification",
                    "metrics": self._compute_dataset_metrics()
                }
            }
        
        # Add preparation info
        mlflow_metadata["preparation"] = {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "config_file": os.path.basename(self.config_file),
            "validation_status": "passed" if self.validate_dataset() else "failed"
        }
        
        # Save updated MLflow metadata
        with open(os.path.join(mlflow_dir, 'mlflow_metadata.json'), 'w') as f:
            json.dump(mlflow_metadata, f, indent=2)
        
        # Create MLflow tags file
        tags = {
            "source": "webots_simulation",
            "data_type": "multi_sensor",
            "sensors": "lidar,camera",
            "environment": "indoor",
            "dataset_id": self.dataset_info.get('dataset_id', 'unknown'),
            "dataset_version": self.dataset_info.get('version', 'unknown'),
            "preparation_run_id": self.run_id
        }
        
        with open(os.path.join(mlflow_dir, 'tags.json'), 'w') as f:
            json.dump(tags, f, indent=2)
        
        # Create MLflow metrics file
        metrics = self._compute_dataset_metrics()
        with open(os.path.join(mlflow_dir, 'metrics.json'), 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Create dataset overview file for MLflow UI
        self._create_dataset_overview(mlflow_dir)
        
        logger.info("MLflow artifacts prepared successfully.")
    
    def _compute_dataset_metrics(self):
        """Compute metrics about the dataset for MLflow tracking"""
        metrics = {}
        
        # Count images
        image_dir = os.path.join(self.data_dir, 'images')
        if os.path.isdir(image_dir):
            metrics["total_images"] = len([f for f in os.listdir(image_dir) 
                                         if f.endswith(('.jpg', '.jpeg', '.png'))])
        
        # Get LIDAR stats if available
        lidar_stats_path = os.path.join(self.data_dir, 'metadata', 'lidar_stats.json')
        if os.path.exists(lidar_stats_path):
            with open(lidar_stats_path, 'r') as f:
                lidar_stats = json.load(f)
                metrics.update({f"lidar_{k}": v for k, v in lidar_stats.items() 
                              if isinstance(v, (int, float))})
        
        # Get camera stats if available
        camera_stats_path = os.path.join(self.data_dir, 'metadata', 'camera_stats.json')
        if os.path.exists(camera_stats_path):
            with open(camera_stats_path, 'r') as f:
                camera_stats = json.load(f)
                metrics.update({f"camera_{k}": v for k, v in camera_stats.items() 
                              if isinstance(v, (int, float))})
        
        # Check for labeled data
        labeled_dir = os.path.join(self.data_dir, 'labeled')
        if os.path.isdir(labeled_dir):
            train_dir = os.path.join(labeled_dir, 'train')
            val_dir = os.path.join(labeled_dir, 'val')
            test_dir = os.path.join(labeled_dir, 'test')
            
            if os.path.isdir(train_dir) and os.path.isdir(val_dir) and os.path.isdir(test_dir):
                metrics["train_samples"] = len(os.listdir(os.path.join(train_dir, 'images')))
                metrics["val_samples"] = len(os.listdir(os.path.join(val_dir, 'images')))
                metrics["test_samples"] = len(os.listdir(os.path.join(test_dir, 'images')))
        
        return metrics
    
    def _create_dataset_overview(self, output_dir):
        """Create an overview markdown file for the dataset"""
        overview = f"""# Simulation Dataset Overview

## Dataset Information
- **ID**: {self.dataset_info.get('dataset_id', 'unknown')}
- **Version**: {self.dataset_info.get('version', 'unknown')}
- **Timestamp**: {self.dataset_info.get('timestamp', 'unknown')}

## Contents
This dataset contains simulated LIDAR and camera data for obstacle detection and 
floor classification tasks. It was generated using the Webots simulation environment.

### Data Statistics
- Total images: {self._compute_dataset_metrics().get('total_images', 'unknown')}
- Training samples: {self._compute_dataset_metrics().get('train_samples', 'unknown')}
- Validation samples: {self._compute_dataset_metrics().get('val_samples', 'unknown')}
- Test samples: {self._compute_dataset_metrics().get('test_samples', 'unknown')}

## Data Format
- LIDAR data: CSV files with timestamp, position, orientation, and range readings
- Camera data: {self.dataset_info.get('formats', {}).get('images', 'JPG/PNG')} files with position metadata

## Labels
- Obstacle detection: Binary classification (obstacle vs. no obstacle)
- Floor classification: Multi-class (tile, carpet, wood, other)

## Preparation
- Prepared by: prepare_for_ml.py
- Run ID: {self.run_id}
- Timestamp: {self.timestamp}
"""
        
        with open(os.path.join(output_dir, 'dataset_overview.md'), 'w') as f:
            f.write(overview)
    
    def copy_to_ml_directory(self):
        """
        Copy the labeled data to the ML-ready directory structure
        following the expected format for the pipeline.
        """
        logger.info("Copying labeled data to ML-ready directory...")
        
        # Check if labeled data exists
        labeled_dir = os.path.join(self.data_dir, 'labeled')
        if not os.path.isdir(labeled_dir):
            logger.error("Labeled data directory not found. Please run data_labeler.py first.")
            return False
        
        # Create data splits directories
        for split in ['train', 'val', 'test']:
            os.makedirs(os.path.join(self.output_dir, split), exist_ok=True)
            os.makedirs(os.path.join(self.output_dir, split, 'images'), exist_ok=True)
            os.makedirs(os.path.join(self.output_dir, split, 'lidar'), exist_ok=True)
        
        # Copy data for each split
        for split in ['train', 'val', 'test']:
            # Copy images
            src_img_dir = os.path.join(labeled_dir, split, 'images')
            dst_img_dir = os.path.join(self.output_dir, split, 'images')
            
            if os.path.isdir(src_img_dir):
                for img_file in os.listdir(src_img_dir):
                    if img_file.endswith(('.jpg', '.jpeg', '.png')):
                        src_path = os.path.join(src_img_dir, img_file)
                        dst_path = os.path.join(dst_img_dir, img_file)
                        shutil.copy2(src_path, dst_path)
            
            # Copy CSV files
            src_split_dir = os.path.join(labeled_dir, split)
            dst_split_dir = os.path.join(self.output_dir, split)
            
            if os.path.isdir(src_split_dir):
                for csv_file in os.listdir(src_split_dir):
                    if csv_file.endswith('.csv'):
                        src_path = os.path.join(src_split_dir, csv_file)
                        if 'lidar' in csv_file:
                            dst_path = os.path.join(dst_split_dir, 'lidar', csv_file)
                        else:
                            dst_path = os.path.join(dst_split_dir, csv_file)
                        shutil.copy2(src_path, dst_path)
        
        # Copy configuration file
        shutil.copy2(self.config_file, os.path.join(self.output_dir, 'pipeline_config.yaml'))
        
        # Copy metadata
        metadata_dir = os.path.join(self.data_dir, 'metadata')
        if os.path.isdir(metadata_dir):
            for meta_file in os.listdir(metadata_dir):
                src_path = os.path.join(metadata_dir, meta_file)
                dst_path = os.path.join(self.output_dir, meta_file)
                shutil.copy2(src_path, dst_path)
        
        logger.info(f"Data copied to ML-ready directory: {self.output_dir}")
        return True
    
    def generate_data_report(self):
        """Generate a report on the prepared data"""
        logger.info("Generating data report...")
        
        # Create report directory
        report_dir = os.path.join(self.output_dir, 'report')
        os.makedirs(report_dir, exist_ok=True)
        
        # Calculate basic statistics
        metrics = self._compute_dataset_metrics()
        
        # Save metrics to report
        with open(os.path.join(report_dir, 'metrics.json'), 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Generate report markdown
        report = f"""# ML Data Preparation Report

## Overview
- **Dataset ID**: {self.dataset_info.get('dataset_id', 'unknown')}
- **Preparation Run ID**: {self.run_id}
- **Timestamp**: {self.timestamp}

## Data Statistics
- Total images: {metrics.get('total_images', 'unknown')}
- Training samples: {metrics.get('train_samples', 'unknown')}
- Validation samples: {metrics.get('val_samples', 'unknown')}
- Test samples: {metrics.get('test_samples', 'unknown')}

## Data Quality
- Validation status: {'Passed' if self.validate_dataset() else 'Failed'}

## Next Steps
1. Run the Airflow DAG to process this data
2. Train models using the processed data
3. Evaluate model performance
4. Deploy the trained model to the Raspberry Pi

## MLflow Integration
MLflow artifacts have been prepared in the `mlflow` directory.
Use these to track experiments and models.
"""
        
        with open(os.path.join(report_dir, 'report.md'), 'w') as f:
            f.write(report)
        
        logger.info(f"Report generated in {report_dir}")
        return True
    
    def run_all(self):
        """Run all preparation steps"""
        logger.info(f"Starting ML data preparation for dataset: {self.dataset_info.get('dataset_id', 'unknown')}")
        
        # Run all preparation steps
        validation_ok = self.validate_dataset()
        if not validation_ok:
            logger.error("Dataset validation failed. Aborting preparation.")
            return False
        
        self.prepare_data_sample()
        self.prepare_mlflow_artifacts()
        self.copy_to_ml_directory()
        self.generate_data_report()
        
        logger.info(f"ML data preparation completed successfully. Output directory: {self.output_dir}")
        return True

def main():
    parser = argparse.ArgumentParser(description='Prepare simulation data for ML training')
    parser.add_argument('--data-dir', type=str, required=True,
                        help='Directory containing the collected simulation data')
    parser.add_argument('--config-file', type=str, default=None,
                        help='Path to the data pipeline configuration file')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Directory to save the prepared data (default: data_dir/ml_ready)')
    parser.add_argument('--sample-only', action='store_true',
                        help='Only create a data sample, not the full preparation')
    parser.add_argument('--sample-size', type=int, default=10,
                        help='Number of samples to include in the sample')
    
    args = parser.parse_args()
    
    # Find config file if not specified
    if args.config_file is None:
        default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                     'data_pipeline_config.yaml')
        if os.path.exists(default_config):
            args.config_file = default_config
        else:
            print("Error: No configuration file specified and default not found.")
            return 1
    
    # Initialize preparer
    preparer = MLDataPreparer(args.data_dir, args.config_file, args.output_dir)
    
    # Run preparation
    if args.sample_only:
        preparer.validate_dataset()
        preparer.prepare_data_sample(args.sample_size)
        print(f"Sample data prepared in {preparer.output_dir}/sample")
    else:
        success = preparer.run_all()
        if not success:
            print("Data preparation failed. See logs for details.")
            return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 