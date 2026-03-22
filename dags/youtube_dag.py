from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

dag_folder = os.path.dirname(os.path.abspath(__file__))

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="is459_assignment_youtube", 
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    fetch_youtube_data = BashOperator(
        task_id="fetch_youtube_data",
        bash_command=f"python {dag_folder}/fetch_youtube_data.py"
    )

    load_data_to_mongo = BashOperator(
        task_id="load_data_to_mongo",
        bash_command=f"python {dag_folder}/load_data_to_mongo.py"
    )

    fetch_youtube_data >> load_data_to_mongo