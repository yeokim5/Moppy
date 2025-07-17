import mlflow
import yaml
from ultralytics import YOLO
import os
import shutil
from pathlib import Path
from datetime import datetime


def train_model():
    
    # Get the correct paths relative to the src directory
    src_dir = Path(__file__).parent.parent
    config_dir = src_dir / "configs"
    artifacts_dir = src_dir / "artifacts"
    model_dir = artifacts_dir / "model"
    
    # Create model directory if it doesn't exist
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Load parameters
    with open(config_dir / 'params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    

    with open(config_dir / 'mlflow_config.yaml', 'r') as f:
        mlflow_config = yaml.safe_load(f)
    
    # Set DagsHub MLflow tracking URI
    mlflow.set_tracking_uri(mlflow_config['mlflow']['tracking_uri'])
    
    # Set DagsHub credentials as environment variables
    os.environ['MLFLOW_TRACKING_USERNAME'] = mlflow_config['MLFLOW_TRACKING_USERNAME']
    os.environ['MLFLOW_TRACKING_PASSWORD'] = mlflow_config['MLFLOW_TRACKING_PASSWORD']
    
    # Get or create experiment (this will use the remote tracking URI)
    experiment_name = mlflow_config['mlflow']['experiment_name']
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id
    
    # Create unique run name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"training_run_{timestamp}"
    
    with mlflow.start_run(experiment_id=experiment_id, run_name=run_name):
        # Log parameters
        mlflow.log_params(params)
        
        # Load model
        model = YOLO(params['WEIGHTS'])
        
        # Change to artifacts directory for training
        original_cwd = os.getcwd()
        os.chdir(str(artifacts_dir))
        
        try:
            # Train model with unique run name to avoid overlapping
            # Set project=None to disable YOLO's built-in MLflow integration
            results = model.train(
                data=str(config_dir / 'data.yaml'),
                epochs=params['EPOCHS'],
                batch=params['BATCH_SIZE'],
                imgsz=params['IMAGE_SIZE'],
                project=None,  # Disable YOLO's built-in MLflow integration
                name=run_name,
                exist_ok=False
            )
        finally:
            # Change back to original directory
            os.chdir(original_cwd)
        
        # The model is now saved in a unique directory: model_dir/run_name/
        # No need to move files around since YOLO creates the proper structure
        print(f"Model training completed and saved in: {model_dir}/{run_name}/")
        
        # Log the training run directory
        mlflow.log_param("training_run_directory", str(model_dir / run_name))
        
        # Log metrics
        mlflow.log_metrics({
            'mAP50': results.results_dict['metrics/mAP50(B)'],
            'mAP50-95': results.results_dict['metrics/mAP50-95(B)'],
            'precision': results.results_dict['metrics/precision(B)'],
            'recall': results.results_dict['metrics/recall(B)']
        })
        
        # Log model artifacts from the unique run directory
        run_model_dir = model_dir / run_name / 'weights'
        if run_model_dir.exists():
            # Log the best model
            best_model_path = run_model_dir / 'best.pt'
            if best_model_path.exists():
                mlflow.log_artifact(str(best_model_path))
            
            # Log the last model
            last_model_path = run_model_dir / 'last.pt'
            if last_model_path.exists():
                mlflow.log_artifact(str(last_model_path))
        
        print(f"Training completed! Check your runs at: {mlflow_config['mlflow']['tracking_uri']}")

if __name__ == "__main__":
    train_model()