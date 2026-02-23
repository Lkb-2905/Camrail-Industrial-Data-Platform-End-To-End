from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Ajout du dossier source au PATH local de Airflow
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extract import extract_sensor_data, extract_maintenance_data
from src.transform import transform_and_load
from src.train import train_model

default_args = {
    'owner': 'camrail_data_engineers',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': ['dba@camrail.com'],
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'camrail_industrial_pipeline',
    default_args=default_args,
    description="Orchestration complète ETL et Recalcul IA - Nuit",
    schedule_interval="@midnight",
    catchup=False
) as dag:

    # 1. Tâche Extraction
    task_extract = PythonOperator(
        task_id='extract_raw_data_api',
        python_callable=extract_sensor_data,
    )

    t_maint = PythonOperator(
        task_id='extract_gmao',
        python_callable=extract_maintenance_data,
    )

    # 2. Tâche Transformation
    task_transform = PythonOperator(
        task_id='cleanse_merge_dwh',
        python_callable=transform_and_load,
    )

    # 3. Tâche Machine Learning
    task_train = PythonOperator(
        task_id='scikit_ml_recalibration',
        python_callable=train_model,
    )

    # Dépendances du Pipeline (Orchestration)
    [task_extract, t_maint] >> task_transform >> task_train
