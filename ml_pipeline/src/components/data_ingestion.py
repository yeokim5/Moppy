import os
import logging
import zipfile
import requests
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIngestion:
    def __init__(self):
        """
        Initialize DataIngestion
        """
        self.training_data_path = Path("ml_pipeline/src/artifacts/training_data")
        self.zip_file_path = self.training_data_path / "roboflow.zip"
        
    def download_file(self) -> str:
        '''
        Fetch data from the Roboflow URL
        '''
        try: 
            dataset_url = "https://app.roboflow.com/ds/5uYVaISbpx?key=LSeaVrHaKk"
            zip_download_dir = str(self.zip_file_path)
            
            # Create directory if it doesn't exist
            self.training_data_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            # Download using requests
            response = requests.get(dataset_url, stream=True)
            response.raise_for_status()
            
            with open(zip_download_dir, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")
            return zip_download_dir

        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            raise e
    
    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        Function returns None
        """
        try:
            unzip_path = str(self.training_data_path)
            os.makedirs(unzip_path, exist_ok=True)
            
            logger.info(f"Extracting zip file from {self.zip_file_path} to {unzip_path}")
            
            with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
            
            logger.info("Extraction completed successfully")
            
            # Remove the zip file after extraction
            if os.path.exists(self.zip_file_path):
                os.remove(self.zip_file_path)
                logger.info("Cleaned up zip file")
                
        except Exception as e:
            logger.error(f"Error extracting zip file: {e}")
            raise e
    
    def _validate_downloaded_data(self) -> None:
        """
        Validate that the downloaded data has the expected structure
        """
        logger.info("Validating downloaded data...")
        
        # Check if expected directories exist
        expected_dirs = ["train", "valid", "test"]
        for dir_name in expected_dirs:
            dir_path = self.training_data_path / dir_name
            if not dir_path.exists():
                raise Exception(f"Expected directory not found: {dir_path}")
            
            # Check if images and labels subdirectories exist
            images_dir = dir_path / "images"
            labels_dir = dir_path / "labels"
            
            if not images_dir.exists():
                raise Exception(f"Images directory not found: {images_dir}")
            if not labels_dir.exists():
                raise Exception(f"Labels directory not found: {labels_dir}")
            
            # Count files
            image_count = len(list(images_dir.glob("*.jpg"))) + len(list(images_dir.glob("*.png")))
            label_count = len(list(labels_dir.glob("*.txt")))
            
            logger.info(f"{dir_name}: {image_count} images, {label_count} labels")
            
            if image_count == 0:
                raise Exception(f"No images found in {images_dir}")
            if label_count == 0:
                raise Exception(f"No labels found in {labels_dir}")
        
        logger.info("Data validation completed successfully")
    
    def _move_data_yaml_and_cleanup(self) -> None:
        """
        Move data.yaml to configs directory, update paths, and delete README files
        """
        logger.info("Moving data.yaml to configs directory, updating paths, and cleaning up README files...")
        
        try:
            # Define paths
            source_data_yaml = self.training_data_path / "data.yaml"
            configs_dir = Path("ml_pipeline/src/configs")
            target_data_yaml = configs_dir / "data.yaml"
            
            # Create configs directory if it doesn't exist
            configs_dir.mkdir(parents=True, exist_ok=True)
            
            # Move data.yaml to configs directory
            if source_data_yaml.exists():
                import shutil
                shutil.move(str(source_data_yaml), str(target_data_yaml))
                logger.info(f"Moved data.yaml from {source_data_yaml} to {target_data_yaml}")
                
                # Update the paths in data.yaml to use correct relative paths
                self._update_data_yaml_paths(target_data_yaml)
                logger.info("Updated data.yaml paths to use correct relative paths")
            else:
                logger.warning(f"data.yaml not found at {source_data_yaml}")
            
            # Delete README files
            readme_files = [
                self.training_data_path / "README.dataset.txt",
                self.training_data_path / "README.roboflow.txt"
            ]
            
            for readme_file in readme_files:
                if readme_file.exists():
                    readme_file.unlink()
                    logger.info(f"Deleted {readme_file}")
                else:
                    logger.info(f"README file not found: {readme_file}")
            
            logger.info("Data.yaml move, path update, and README cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Error during data.yaml move and cleanup: {e}")
            raise e
    
    def _update_data_yaml_paths(self, data_yaml_path: Path) -> None:
        """
        Update the paths in data.yaml to use correct relative paths from configs directory
        """
        try:
            # Read the current content
            with open(data_yaml_path, 'r') as f:
                content = f.read()
            
            # Replace the paths to point to artifacts/training_data
            content = content.replace('train: ../train/images', 'train: ../artifacts/training_data/train/images')
            content = content.replace('val: ../valid/images', 'val: ../artifacts/training_data/valid/images')
            content = content.replace('test: ../test/images', 'test: ../artifacts/training_data/test/images')
            
            # Write the updated content back
            with open(data_yaml_path, 'w') as f:
                f.write(content)
                
            logger.info("Successfully updated data.yaml paths")
            
        except Exception as e:
            logger.error(f"Error updating data.yaml paths: {e}")
            raise e
    
    def run(self) -> None:
        """
        Main method to run the data ingestion process
        """
        logger.info("Starting data ingestion process...")
        
        try:
            # Download the dataset
            self.download_file()
            
            # Extract the zip file
            self.extract_zip_file()
            
            # Validate the downloaded data
            self._validate_downloaded_data()
            
            # Move data.yaml to configs and cleanup README files
            self._move_data_yaml_and_cleanup()
            
            logger.info("Data ingestion completed successfully!")
            
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise

def main():
    """Main function to run data ingestion"""
    try:
        data_ingestion = DataIngestion()
        data_ingestion.run()
    except Exception as e:
        logger.error(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
