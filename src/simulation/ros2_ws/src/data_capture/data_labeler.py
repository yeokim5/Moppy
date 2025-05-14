import os
import pandas as pd
import json
import argparse
from PIL import Image
import datetime
import numpy as np
import uuid
import shutil

class DataLabeler:
    def __init__(self, data_dir, output_dir=None):
        self.data_dir = data_dir
        self.output_dir = output_dir if output_dir else os.path.join(data_dir, 'labeled')
        self.obstacle_types = {'obstacle': 1, 'none': 0}
        self.floor_types = {'tile': 0, 'carpet': 1, 'wood': 2, 'other': 3}
        
        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'train'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'val'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'test'), exist_ok=True)
        
        # Dataset versioning
        self.dataset_version = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.dataset_id = str(uuid.uuid4())[:8]

    def label_lidar_data(self, lidar_csv):
        """
        Process LIDAR data and apply labels based on distance thresholds
        """
        if not os.path.exists(lidar_csv):
            print(f"Error: LIDAR CSV file {lidar_csv} not found")
            return False
            
        # Load LIDAR data
        try:
            lidar_df = pd.read_csv(lidar_csv)
        except Exception as e:
            print(f"Error loading LIDAR data: {e}")
            return False
            
        # Initialize obstacle label column
        lidar_df['obstacle_detected'] = 0
        
        # Apply simple thresholding for obstacle detection
        # This is a very basic approach - in a real system, you would use more sophisticated methods
        for col in lidar_df.columns:
            if col.startswith('range_'):
                # Mark readings below threshold as obstacles (e.g., < 0.5m is an obstacle)
                lidar_df.loc[lidar_df[col] < 0.5, 'obstacle_detected'] = 1
        
        # Save labeled LIDAR data
        labeled_csv = os.path.join(self.output_dir, f"labeled_{os.path.basename(lidar_csv)}")
        lidar_df.to_csv(labeled_csv, index=False)
        print(f"Labeled LIDAR data saved to {labeled_csv}")
        
        # Create a summary file with statistics
        stats = {
            'total_readings': len(lidar_df),
            'obstacle_readings': lidar_df['obstacle_detected'].sum(),
            'non_obstacle_readings': len(lidar_df) - lidar_df['obstacle_detected'].sum(),
            'dataset_version': self.dataset_version,
            'dataset_id': self.dataset_id
        }
        
        with open(os.path.join(self.output_dir, 'lidar_stats.json'), 'w') as f:
            json.dump(stats, f, indent=2)
            
        return True

    def label_camera_data(self, camera_csv):
        """
        Process camera images and create labels for surface type classification
        """
        if not os.path.exists(camera_csv):
            print(f"Error: Camera CSV file {camera_csv} not found")
            return False
            
        # Load camera metadata
        try:
            camera_df = pd.read_csv(camera_csv)
        except Exception as e:
            print(f"Error loading camera metadata: {e}")
            return False
            
        # Initialize surface type labels using a simple approach
        # In a real implementation, you would use image analysis to determine floor types
        camera_df['surface_type'] = self.floor_types['tile']  # Default to tile for now
        
        # Simulate adding some variety for demonstration
        camera_df.loc[0:int(len(camera_df)*0.3), 'surface_type'] = self.floor_types['carpet']
        camera_df.loc[int(len(camera_df)*0.3):int(len(camera_df)*0.6), 'surface_type'] = self.floor_types['tile']
        camera_df.loc[int(len(camera_df)*0.6):int(len(camera_df)*0.9), 'surface_type'] = self.floor_types['wood']
        camera_df.loc[int(len(camera_df)*0.9):, 'surface_type'] = self.floor_types['other']
        
        # Add obstacle labels (this would normally come from detailed image analysis)
        camera_df['obstacle_in_image'] = 0
        
        # Save labeled camera data
        labeled_csv = os.path.join(self.output_dir, f"labeled_{os.path.basename(camera_csv)}")
        camera_df.to_csv(labeled_csv, index=False)
        print(f"Labeled camera data saved to {labeled_csv}")
        
        # Create a summary file with statistics
        stats = {
            'total_images': len(camera_df),
            'surface_type_counts': {
                'tile': sum(camera_df['surface_type'] == self.floor_types['tile']),
                'carpet': sum(camera_df['surface_type'] == self.floor_types['carpet']),
                'wood': sum(camera_df['surface_type'] == self.floor_types['wood']),
                'other': sum(camera_df['surface_type'] == self.floor_types['other'])
            },
            'dataset_version': self.dataset_version,
            'dataset_id': self.dataset_id
        }
        
        with open(os.path.join(self.output_dir, 'camera_stats.json'), 'w') as f:
            json.dump(stats, f, indent=2)
            
        return True

    def organize_dataset(self):
        """
        Organize labeled data into train/val/test splits
        """
        print("Organizing dataset into train/val/test splits...")
        
        # Create directories if they don't exist
        for split in ['train', 'val', 'test']:
            os.makedirs(os.path.join(self.output_dir, split, 'images'), exist_ok=True)
            os.makedirs(os.path.join(self.output_dir, split, 'lidar'), exist_ok=True)
        
        # Find labeled CSV files
        labeled_files = [f for f in os.listdir(self.output_dir) if f.startswith('labeled_') and f.endswith('.csv')]
        
        for file in labeled_files:
            file_path = os.path.join(self.output_dir, file)
            df = pd.read_csv(file_path)
            
            # Shuffle data
            df = df.sample(frac=1, random_state=42)
            
            # Split data: 70% train, 15% val, 15% test
            train_size = int(0.7 * len(df))
            val_size = int(0.15 * len(df))
            
            train_df = df[:train_size]
            val_df = df[train_size:train_size+val_size]
            test_df = df[train_size+val_size:]
            
            # Save splits
            if 'camera' in file:
                # For camera data, also organize the image files
                for split_name, split_df in [('train', train_df), ('val', val_df), ('test', test_df)]:
                    split_df.to_csv(os.path.join(self.output_dir, split_name, f"{file}"), index=False)
                    
                    # Copy images to the appropriate split directory
                    for _, row in split_df.iterrows():
                        if 'image_filename' in row:
                            src_path = os.path.join(self.data_dir, 'images', row['image_filename'])
                            if os.path.exists(src_path):
                                dst_path = os.path.join(self.output_dir, split_name, 'images', row['image_filename'])
                                shutil.copy2(src_path, dst_path)
            
            elif 'lidar' in file:
                # For LIDAR data, just save the CSVs
                train_df.to_csv(os.path.join(self.output_dir, 'train', f"{file}"), index=False)
                val_df.to_csv(os.path.join(self.output_dir, 'val', f"{file}"), index=False)
                test_df.to_csv(os.path.join(self.output_dir, 'test', f"{file}"), index=False)
        
        # Create a dataset manifest file
        self._create_dataset_manifest()
        
        print("Dataset organization complete!")
        return True

    def _create_dataset_manifest(self):
        """
        Create a detailed manifest file for the dataset to support MLflow tracking
        """
        manifest = {
            'dataset_id': self.dataset_id,
            'dataset_version': self.dataset_version,
            'creation_date': datetime.datetime.now().isoformat(),
            'source_directory': self.data_dir,
            'output_directory': self.output_dir,
            'splits': {
                'train': self._count_files_in_split('train'),
                'val': self._count_files_in_split('val'),
                'test': self._count_files_in_split('test')
            },
            'labels': {
                'obstacle_types': self.obstacle_types,
                'floor_types': self.floor_types
            },
            'data_formats': {
                'lidar': 'CSV with timestamp, position, orientation, and range readings',
                'images': 'RGB images in JPEG/PNG format with position metadata'
            }
        }
        
        # Save manifest
        with open(os.path.join(self.output_dir, 'dataset_manifest.json'), 'w') as f:
            json.dump(manifest, f, indent=2)
            
        # Create a simplified version for MLflow tracking
        self._create_mlflow_metadata()
        
        return True
    
    def _count_files_in_split(self, split):
        """Helper to count files in each data split"""
        counts = {
            'images': len([f for f in os.listdir(os.path.join(self.output_dir, split, 'images')) 
                           if os.path.isfile(os.path.join(self.output_dir, split, 'images', f))]),
            'lidar': len([f for f in os.listdir(os.path.join(self.output_dir, split, 'lidar')) 
                          if os.path.isfile(os.path.join(self.output_dir, split, 'lidar', f))])
        }
        return counts

    def _create_mlflow_metadata(self):
        """
        Create metadata format compatible with MLflow tracking
        """
        mlflow_metadata = {
            'dataset': {
                'name': f'simulation_dataset_{self.dataset_id}',
                'version': self.dataset_version,
                'description': 'Simulated LIDAR and camera data for obstacle detection and floor classification',
                'size_mb': self._calculate_dataset_size_mb(),
                'metrics': {
                    'total_images': sum(self._count_files_in_split(split)['images'] for split in ['train', 'val', 'test']),
                    'total_lidar_samples': sum(self._count_files_in_split(split)['lidar'] for split in ['train', 'val', 'test'])
                },
                'tags': {
                    'source': 'webots_simulation',
                    'environment': 'indoor',
                    'sensors': 'lidar,camera',
                    'annotations': 'obstacles,floor_types'
                }
            }
        }
        
        # Save MLflow metadata
        with open(os.path.join(self.output_dir, 'mlflow_metadata.json'), 'w') as f:
            json.dump(mlflow_metadata, f, indent=2)
            
        return True
    
    def _calculate_dataset_size_mb(self):
        """Calculate the total size of the dataset in MB"""
        total_bytes = 0
        for root, dirs, files in os.walk(self.output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                total_bytes += os.path.getsize(file_path)
        
        return total_bytes / (1024 * 1024)  # Convert to MB

def main():
    parser = argparse.ArgumentParser(description='Label and organize captured simulation data')
    parser.add_argument('--data-dir', type=str, required=True,
                        help='Directory containing the captured data')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Directory to save labeled data (defaults to data_dir/labeled)')
    parser.add_argument('--lidar-csv', type=str, default=None,
                        help='Specific LIDAR CSV file to process (if not provided, will find latest)')
    parser.add_argument('--camera-csv', type=str, default=None,
                        help='Specific camera metadata CSV file to process (if not provided, will find latest)')
    parser.add_argument('--organize', action='store_true',
                        help='Organize data into train/val/test splits after labeling')
    
    args = parser.parse_args()
    
    # Find latest CSV files if not specified
    if not args.lidar_csv:
        lidar_csvs = [f for f in os.listdir(args.data_dir) if f.endswith('.csv') and 'lidar' in f]
        lidar_csvs.sort(reverse=True)  # Most recent first
        if lidar_csvs:
            args.lidar_csv = os.path.join(args.data_dir, lidar_csvs[0])
    
    if not args.camera_csv:
        camera_csvs = [f for f in os.listdir(args.data_dir) if f.endswith('.csv') and 'camera' in f]
        camera_csvs.sort(reverse=True)  # Most recent first
        if camera_csvs:
            args.camera_csv = os.path.join(args.data_dir, camera_csvs[0])
    
    # Initialize data labeler
    labeler = DataLabeler(args.data_dir, args.output_dir)
    
    # Process LIDAR data
    if args.lidar_csv and os.path.exists(args.lidar_csv):
        print(f"Processing LIDAR data: {args.lidar_csv}")
        labeler.label_lidar_data(args.lidar_csv)
    else:
        print("No LIDAR data found to process")
    
    # Process camera data
    if args.camera_csv and os.path.exists(args.camera_csv):
        print(f"Processing camera data: {args.camera_csv}")
        labeler.label_camera_data(args.camera_csv)
    else:
        print("No camera metadata found to process")
    
    # Organize dataset if requested
    if args.organize:
        labeler.organize_dataset()

if __name__ == '__main__':
    main() 