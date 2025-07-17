import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from components.data_ingestion import DataIngestion
import logging

def main():
    """
    Main function for the data ingestion pipeline stage
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting data ingestion pipeline stage...")
        
        # Initialize and run data ingestion
        data_ingestion = DataIngestion()
        data_ingestion.run()
        
        logger.info("Data ingestion pipeline stage completed successfully!")
        
    except Exception as e:
        logger.error(f"Data ingestion pipeline stage failed: {e}")
        raise

if __name__ == "__main__":
    main()
