#!/usr/bin/env python3

import os
import sys
import argparse
import glob
import json
import csv
from PIL import Image

# Handle NumPy compatibility issues
try:
    import numpy as np
    import pandas as pd
    HAS_NUMPY = True
except ImportError:
    print("NumPy or pandas not available - will use basic validation without them")
    HAS_NUMPY = False

# Handle matplotlib compatibility issues
try:
    import cv2
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    print("Matplotlib or OpenCV not available - visualizations will be disabled")
    HAS_MATPLOTLIB = False

# Custom JSON encoder to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

class DataValidator:
    """
    DataValidator checks the quality and consistency of captured sensor data
    to ensure it's suitable for training.
    """
    
    def __init__(self, data_dir, output_dir=None, verbose=True):
        self.data_dir = data_dir
        self.output_dir = output_dir if output_dir else os.path.join(data_dir, 'validation')
        self.verbose = verbose
        
        # Create output directory if it doesn't exist
        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize results
        self.validation_results = {
            'lidar_files': [],
            'camera_files': [],
            'lidar_validation': {},
            'camera_validation': {},
            'overall_result': 'PENDING'
        }
    
    def log(self, message):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def validate_lidar_data(self):
        """Validate LIDAR CSV data files for completeness and consistency."""
        self.log("Validating LIDAR data files...")
        
        # Find all LIDAR data files
        lidar_files = glob.glob(os.path.join(self.data_dir, '*lidar*.csv'))
        self.validation_results['lidar_files'] = lidar_files
        
        if not lidar_files:
            self.log("No LIDAR data files found.")
            self.validation_results['lidar_validation']['status'] = 'FAILED'
            self.validation_results['lidar_validation']['errors'] = ['No LIDAR data files found.']
            return False
        
        self.log(f"Found {len(lidar_files)} LIDAR data files.")
        
        # Validation metrics
        total_readings = 0
        valid_readings = 0
        errors = []
        
        for file_path in lidar_files:
            try:
                if HAS_NUMPY:
                    # Advanced validation with pandas/numpy
                    file_total, file_valid = self._validate_lidar_file_with_numpy(file_path, errors)
                    total_readings += file_total
                    valid_readings += file_valid
                else:
                    # Basic validation without pandas/numpy
                    file_total, file_valid = self._validate_lidar_file_basic(file_path, errors)
                    total_readings += file_total
                    valid_readings += file_valid
                    
            except Exception as e:
                errors.append(f"Error processing file {os.path.basename(file_path)}: {str(e)}")
        
        # Calculate quality score
        if total_readings > 0:
            quality_score = valid_readings / total_readings
            self.log(f"LIDAR data quality score: {quality_score:.2f} "
                    f"({valid_readings}/{total_readings} valid readings)")
        else:
            quality_score = 0.0
            self.log("No LIDAR readings found.")
        
        # Store validation results
        self.validation_results['lidar_validation'] = {
            'status': 'PASSED' if (quality_score > 0.8 and not errors) else 'FAILED',
            'quality_score': quality_score,
            'total_readings': total_readings,
            'valid_readings': valid_readings,
            'errors': errors
        }
        
        return quality_score > 0.8 and not errors
    
    def _validate_lidar_file_with_numpy(self, file_path, errors):
        """Validate LIDAR file using pandas and numpy."""
        # Load CSV file
        df = pd.read_csv(file_path)
        
        # Check if file has expected columns
        expected_columns = ['timestamp', 'x_position', 'y_position', 'theta']
        for col in expected_columns:
            if col not in df.columns:
                errors.append(f"File {os.path.basename(file_path)} missing column: {col}")
        
        # Count readings
        file_total = len(df)
        
        # Count NaN or missing values
        nan_count = df.isna().sum().sum()
        infinite_count = np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
        
        # Check range values (excluding position columns)
        range_columns = [col for col in df.columns if col.startswith('range_')]
        
        total_readings = 0
        valid_readings = 0
        
        if range_columns:
            # Count valid range readings (non-inf, non-NaN, within expected ranges)
            valid_ranges = ((df[range_columns] > 0) & 
                            (df[range_columns] < 50) &  # Assuming max range of 50m
                            np.isfinite(df[range_columns]))
            
            # Convert to numpy array to avoid multi-dimensional indexing issues
            valid_ranges_np = np.array(valid_ranges)
            valid_count = np.sum(valid_ranges_np)
            
            # Calculate totals for this file
            total_readings = len(df) * len(range_columns)
            valid_readings = valid_count
        else:
            errors.append(f"File {os.path.basename(file_path)} has no range columns.")
        
        # Log per-file stats
        self.log(f"  {os.path.basename(file_path)}: {file_total} readings, "
                f"{nan_count} NaN values, {infinite_count} infinite values")
        
        # Generate visualization for this file if output_dir is specified
        if self.output_dir and HAS_MATPLOTLIB:
            self._generate_lidar_visualization(df, file_path)
            
        return total_readings, valid_readings
    
    def _validate_lidar_file_basic(self, file_path, errors):
        """Validate LIDAR file using basic Python without pandas/numpy."""
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            # Check if file has expected columns
            expected_columns = ['timestamp', 'x_position', 'y_position', 'theta']
            for col in expected_columns:
                if col not in headers:
                    errors.append(f"File {os.path.basename(file_path)} missing column: {col}")
            
            # Count range columns
            range_columns = [i for i, col in enumerate(headers) if col.startswith('range_')]
            
            if not range_columns:
                errors.append(f"File {os.path.basename(file_path)} has no range columns.")
                return 0, 0
            
            # Count readings and valid values
            row_count = 0
            file_total_readings = 0
            file_valid_readings = 0
            
            for row in reader:
                row_count += 1
                for idx in range_columns:
                    file_total_readings += 1
                    try:
                        value = float(row[idx])
                        if 0 < value < 50:  # Assuming max range of 50m
                            file_valid_readings += 1
                    except (ValueError, IndexError):
                        pass
            
            # Log per-file stats
            self.log(f"  {os.path.basename(file_path)}: {row_count} readings, {file_valid_readings} valid range values out of {file_total_readings}")
            
            return file_total_readings, file_valid_readings
    
    def validate_camera_data(self):
        """Validate camera image files and metadata for quality and consistency."""
        self.log("Validating camera data files...")
        
        # Find all camera metadata files
        metadata_files = glob.glob(os.path.join(self.data_dir, '*camera_metadata*.csv'))
        self.validation_results['camera_files'] = metadata_files
        
        if not metadata_files:
            self.log("No camera metadata files found.")
            self.validation_results['camera_validation']['status'] = 'FAILED'
            self.validation_results['camera_validation']['errors'] = ['No camera metadata files found.']
            return False
        
        self.log(f"Found {len(metadata_files)} camera metadata files.")
        
        # Validation metrics
        total_images = 0
        valid_images = 0
        errors = []
        
        for file_path in metadata_files:
            try:
                with open(file_path, 'r') as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    
                    # Check if file has expected columns
                    expected_columns = ['timestamp', 'image_filename', 'x_position', 'y_position', 'theta']
                    for col in expected_columns:
                        if col not in headers:
                            errors.append(f"File {os.path.basename(file_path)} missing column: {col}")
                    
                    # Get the directory containing the metadata file
                    base_dir = os.path.dirname(file_path)
                    
                    # Check if all image files exist
                    images_dir = os.path.join(base_dir, 'images')
                    missing_images = 0
                    corrupt_images = 0
                    
                    # Get filename column index
                    try:
                        filename_idx = headers.index('image_filename')
                    except ValueError:
                        errors.append(f"File {os.path.basename(file_path)} missing 'image_filename' column.")
                        continue
                    
                    # Check each image referenced in the metadata
                    rows = list(reader)  # Convert to list to get count
                    total_images += len(rows)
                    
                    for row in rows:
                        if len(row) <= filename_idx:
                            missing_images += 1
                            continue
                            
                        image_path = os.path.join(images_dir, row[filename_idx])
                        
                        # Check if image file exists
                        if not os.path.exists(image_path):
                            missing_images += 1
                            continue
                        
                        # Check if image can be opened (not corrupt)
                        try:
                            img = Image.open(image_path)
                            img.verify()  # Verify the image
                            valid_images += 1
                        except Exception:
                            corrupt_images += 1
                    
                    # Log per-file stats
                    self.log(f"  {os.path.basename(file_path)}: {len(rows)} images, "
                            f"{missing_images} missing, {corrupt_images} corrupt")
                    
                    if missing_images > 0:
                        errors.append(f"File {os.path.basename(file_path)} missing {missing_images} images.")
                    if corrupt_images > 0:
                        errors.append(f"File {os.path.basename(file_path)} has {corrupt_images} corrupt images.")
                    
                    # Generate visualization for this file if output_dir is specified
                    if self.output_dir and HAS_MATPLOTLIB and HAS_NUMPY:
                        df = pd.read_csv(file_path)
                        self._generate_camera_visualization(df, file_path, images_dir)
                    
            except Exception as e:
                errors.append(f"Error processing file {os.path.basename(file_path)}: {str(e)}")
        
        # Calculate quality score
        if total_images > 0:
            quality_score = valid_images / total_images
            self.log(f"Camera data quality score: {quality_score:.2f} "
                    f"({valid_images}/{total_images} valid images)")
        else:
            quality_score = 0.0
            self.log("No camera images found.")
        
        # Store validation results
        self.validation_results['camera_validation'] = {
            'status': 'PASSED' if (quality_score > 0.9 and not errors) else 'FAILED',
            'quality_score': quality_score,
            'total_images': total_images,
            'valid_images': valid_images,
            'errors': errors
        }
        
        return quality_score > 0.9 and not errors
    
    def _generate_lidar_visualization(self, df, file_path):
        """Generate visualization for LIDAR data."""
        if not HAS_MATPLOTLIB:
            return
            
        try:
            # Create a filename for the visualization
            base_name = os.path.basename(file_path).replace('.csv', '')
            viz_path = os.path.join(self.output_dir, f"{base_name}_viz.png")
            
            # Create plots
            fig, axs = plt.subplots(2, 1, figsize=(10, 12))
            
            # Convert to numpy arrays before indexing to avoid multi-dimensional indexing issues
            x_pos = np.array(df['x_position'])
            y_pos = np.array(df['y_position'])
            timestamps = np.array(df['timestamp'])
            
            # Plot 1: Robot path
            axs[0].plot(x_pos, y_pos, 'b-', linewidth=1)
            axs[0].plot(x_pos[0], y_pos[0], 'go', label='Start')
            axs[0].plot(x_pos[-1], y_pos[-1], 'ro', label='End')
            axs[0].set_title('Robot Path')
            axs[0].set_xlabel('X Position (m)')
            axs[0].set_ylabel('Y Position (m)')
            axs[0].grid(True)
            axs[0].axis('equal')
            axs[0].legend()
            
            # Plot 2: Sample LIDAR readings over time (first 5 angles)
            range_columns = [col for col in df.columns if col.startswith('range_')]
            if range_columns:
                # Take a subset of range columns if there are many
                sample_columns = range_columns[:5]
                for col in sample_columns:
                    angle = float(col.split('_')[-1])
                    # Convert to numpy array before indexing
                    range_values = np.array(df[col])
                    time_values = np.array(timestamps - timestamps[0])
                    axs[1].plot(time_values, range_values, label=f"{angle:.2f} rad")
                
                axs[1].set_title('Sample LIDAR Readings Over Time')
                axs[1].set_xlabel('Time (s)')
                axs[1].set_ylabel('Range (m)')
                axs[1].grid(True)
                axs[1].legend()
            
            # Save the figure
            plt.tight_layout()
            plt.savefig(viz_path)
            plt.close(fig)
            
            self.log(f"  Generated visualization: {os.path.basename(viz_path)}")
            
        except Exception as e:
            self.log(f"  Error generating LIDAR visualization: {str(e)}")
    
    def _generate_camera_visualization(self, df, file_path, images_dir):
        """Generate visualization for camera data."""
        if not HAS_MATPLOTLIB:
            return
            
        try:
            # Create a filename for the visualization
            base_name = os.path.basename(file_path).replace('.csv', '')
            viz_path = os.path.join(self.output_dir, f"{base_name}_viz.png")
            
            # Create plots
            fig, axs = plt.subplots(2, 2, figsize=(12, 10))
            
            # Convert to numpy arrays before indexing
            x_pos = np.array(df['x_position'])
            y_pos = np.array(df['y_position'])
            timestamps = np.array(df['timestamp'])
            
            # Plot 1: Robot path
            axs[0, 0].plot(x_pos, y_pos, 'b-', linewidth=1)
            axs[0, 0].plot(x_pos[0], y_pos[0], 'go', label='Start')
            axs[0, 0].plot(x_pos[-1], y_pos[-1], 'ro', label='End')
            axs[0, 0].set_title('Robot Path')
            axs[0, 0].set_xlabel('X Position (m)')
            axs[0, 0].set_ylabel('Y Position (m)')
            axs[0, 0].grid(True)
            axs[0, 0].axis('equal')
            axs[0, 0].legend()
            
            # Plot 2: Capture distribution over time
            time_diffs = np.diff(timestamps)
            axs[0, 1].hist(time_diffs, bins=20)
            axs[0, 1].set_title('Time Between Captures')
            axs[0, 1].set_xlabel('Time (s)')
            axs[0, 1].set_ylabel('Count')
            axs[0, 1].grid(True)
            
            # Plot 3 & 4: Sample images
            sample_indices = [0, len(df)-1]  # First and last
            for i, idx in enumerate(sample_indices):
                if idx < len(df):
                    # Convert to numpy array before accessing elements
                    filenames = np.array(df['image_filename'])
                    if idx < len(filenames):
                        image_path = os.path.join(images_dir, filenames[idx])
                        if os.path.exists(image_path):
                            img = cv2.imread(image_path)
                            if img is not None:
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                axs[1, i].imshow(img)
                                axs[1, i].set_title(f"{'First' if i == 0 else 'Last'} Image")
                                axs[1, i].axis('off')
            
            # Save the figure
            plt.tight_layout()
            plt.savefig(viz_path)
            plt.close(fig)
            
            self.log(f"  Generated visualization: {os.path.basename(viz_path)}")
            
        except Exception as e:
            self.log(f"  Error generating camera visualization: {str(e)}")
    
    def validate_all(self):
        """Run all validation checks and generate a summary report."""
        self.log("\n=== Starting Data Validation ===\n")
        
        lidar_result = self.validate_lidar_data()
        camera_result = self.validate_camera_data()
        
        # Determine overall result
        if lidar_result and camera_result:
            overall_result = 'PASSED'
        elif lidar_result or camera_result:
            overall_result = 'PARTIAL'
        else:
            overall_result = 'FAILED'
        
        self.validation_results['overall_result'] = overall_result
        
        # Print summary
        self.log("\n=== Validation Summary ===")
        self.log(f"LIDAR Data: {self.validation_results['lidar_validation'].get('status', 'N/A')}")
        self.log(f"Camera Data: {self.validation_results['camera_validation'].get('status', 'N/A')}")
        self.log(f"Overall Result: {overall_result}")
        
        # Save report
        if self.output_dir:
            report_path = os.path.join(self.output_dir, 'validation_report.json')
            with open(report_path, 'w') as f:
                json.dump(self.validation_results, f, indent=2, cls=NumpyEncoder)
            
            self.log(f"\nValidation report saved to: {report_path}")
        
        return overall_result

def main():
    parser = argparse.ArgumentParser(description='Validate captured sensor data')
    parser.add_argument('--data-dir', type=str, required=True,
                        help='Directory containing data to validate')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Directory to save validation results (default: data_dir/validation)')
    parser.add_argument('--quiet', action='store_true', 
                        help='Suppress verbose output')
    
    args = parser.parse_args()
    
    validator = DataValidator(args.data_dir, args.output_dir, not args.quiet)
    result = validator.validate_all()
    
    # Set exit code based on validation result
    if result == 'PASSED':
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main() 