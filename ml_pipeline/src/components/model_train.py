import mlflow
import yaml
from ultralytics import YOLO
import os
from pathlib import Path
from datetime import datetime

def train_model():
    """
    This script trains a YOLOv8 model using parameters from YAML files,
    logs the experiment with MLflow, and saves the model artifacts.
    """
    
    # --- 1. Load Configuration ---
    # Get the correct paths relative to this script's location.
    # Assumes this script is in 'src/components/' and configs are in 'src/configs/'.
    src_dir = Path(__file__).parent.parent
    config_dir = src_dir / "configs"
    artifacts_dir = src_dir / "artifacts"
    model_output_dir = artifacts_dir / "model_runs" # Directory to save all training outputs
    
    # Create the main output directory if it doesn't exist
    model_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load parameters from YAML files
    with open(config_dir / 'params.yaml', 'r') as f:
        params = yaml.safe_load(f)

    with open(config_dir / 'mlflow_config.yaml', 'r') as f:
        mlflow_config = yaml.safe_load(f)

    # --- 2. Set up MLflow ---
    # Set DagsHub MLflow tracking URI and credentials
    mlflow.set_tracking_uri(mlflow_config['mlflow']['tracking_uri'])
    os.environ['MLFLOW_TRACKING_USERNAME'] = mlflow_config['MLFLOW_TRACKING_USERNAME']
    os.environ['MLFLOW_TRACKING_PASSWORD'] = mlflow_config['MLFLOW_TRACKING_PASSWORD']
    
    # Get or create the experiment
    experiment_name = mlflow_config['mlflow']['experiment_name']
    mlflow.set_experiment(experiment_name)
    
    # Create a unique run name with a timestamp for this training session
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"training_run_{timestamp}"
    
    # --- 3. Start MLflow Run & Train Model ---
    with mlflow.start_run(run_name=run_name) as run:
        print(f"Starting MLflow Run: {run_name}")
        print(f"Run ID: {run.info.run_id}")

        # Log parameters from params.yaml to MLflow
        mlflow.log_params(params['train'])
        mlflow.log_param("model_weights", params['weights'])
        
        # Load the YOLO model with the specified weights
        model = YOLO(params['weights'])
        
        # IMPORTANT: This tells Ultralytics to log to our active MLflow run
        # instead of creating a new, separate one.
        os.environ["MLFLOW_ACTIVE_RUN_ID"] = run.info.run_id
        
        # Prepare training arguments from our params file
        training_args = params['train']
        training_args['data'] = str(config_dir / 'data.yaml') # Add data.yaml path
        training_args['project'] = str(model_output_dir)      # Set output project directory
        training_args['name'] = run_name                      # Set specific run folder name
        
        print("\n--- Training Arguments ---")
        for key, value in training_args.items():
            print(f"{key}: {value}")
        print("--------------------------\n")

        # Train the model. No need for try/finally or os.chdir.
        # YOLO will save results to: artifacts/model_runs/training_run_YYYYMMDD_HHMMSS/
        results = model.train(**training_args)
        
        print("\n--- Training Completed ---")
        
        # Debug: Print available results keys
        print(f"Available results keys: {list(results.results_dict.keys())}")
        print(f"Results dict: {results.results_dict}")
        
        # --- 4. Log Results to MLflow ---
        # The results object contains final metrics
        # Safely extract metrics with proper validation
        final_metrics = {}
        
        # Define the metrics we want to log with their expected keys
        metric_keys = {
            'mAP50-95(B)': 'metrics/mAP50-95(B)',
            'mAP50(B)': 'metrics/mAP50(B)', 
            'precision(B)': 'metrics/precision(B)',
            'recall(B)': 'metrics/recall(B)',
            'val_box_loss': 'val/box_loss',
            'val_cls_loss': 'val/cls_loss',
        }
        
        # Safely extract and validate each metric
        for metric_name, key in metric_keys.items():
            value = results.results_dict.get(key)
            if value is not None and isinstance(value, (int, float)) and not (isinstance(value, float) and (value != value)):  # Check for NaN
                final_metrics[metric_name] = float(value)
            else:
                print(f"Warning: Invalid or missing metric for {metric_name} (key: {key}), value: {value}")
        
        # Only log metrics if we have valid ones
        if final_metrics:
            try:
                mlflow.log_metrics(final_metrics)
                print(f"Logged {len(final_metrics)} metrics to MLflow: {list(final_metrics.keys())}")
            except Exception as e:
                print(f"Warning: Failed to log metrics to MLflow: {e}")
                print(f"Metrics that failed to log: {final_metrics}")
        else:
            print("Warning: No valid metrics found to log to MLflow")

        # Log model artifacts (best.pt and last.pt)
        run_output_dir = model_output_dir / run_name
        mlflow.log_artifacts(str(run_output_dir), artifact_path="yolo_outputs")
        print(f"Logged all training outputs from '{run_output_dir}' to MLflow artifact path 'yolo_outputs'.")
        
        # Explicitly log the best model for easy access
        best_model_path = run_output_dir / 'weights' / 'best.pt'
        if best_model_path.exists():
            mlflow.log_artifact(str(best_model_path), artifact_path="best_model")
            print(f"Logged best model '{best_model_path.name}' to MLflow artifact path 'best_model'.")

    print(f"\nTraining and logging complete! Check your runs at: {mlflow.get_tracking_uri()}")

if __name__ == "__main__":
    train_model()
