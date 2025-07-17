Via DVC: dvc repro data_ingestion
Directly: python src/pipeline/stage_01_data_ingestion.py
As component: python -c "from src.components.data_ingestion import DataIngestion; DataIngestion().run()"


python ml_pipeline/src/pipeline/stage_02_model_train.py

env
dataset_url = "https://app.roboflow.com/ds/VZK0X7Sb58?key=cmocbrIQg3"
MLFLOW_TRACKING_USERNAME: yeokim5
MLFLOW_TRACKING_PASSWORD: b050ac9d7f7aac1d90aa60783d6d46fa83d34403


