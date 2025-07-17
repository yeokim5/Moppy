import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from components.model_train import train_model
import logging

def main():
    """
    Main function for the model training pipeline stage
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting model training pipeline stage...")
        
        # Run model training
        train_model()
        
        logger.info("Model training pipeline stage completed successfully!")
        
    except Exception as e:
        logger.error(f"Model training pipeline stage failed: {e}")
        raise

if __name__ == "__main__":
    main()
