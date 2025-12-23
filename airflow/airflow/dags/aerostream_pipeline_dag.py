from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from tasks.fetch import fetch_data
from tasks.clean import clean_data
from tasks.predict import generate_predictions
from tasks.stock import insert_data


API_BATCH_URL = "http://api:8000/api/batch"
API_PREDICT_URL = "http://api:8000/api/predict"

### DAG

with DAG(
    dag_id="aerostream_dag",
    description="Aerostream DAG",
    schedule_interval="* * * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False
):

    fetch_data_task = PythonOperator(
        task_id = "fetch_data",
        python_callable=fetch_data,
        op_args=[API_BATCH_URL, 25]
    )

    clean_data_task = PythonOperator(
        task_id = "clean_data",
        python_callable=clean_data,
    )

    generate_predictions_task = PythonOperator(
        task_id = "generate_predictions",
        python_callable=generate_predictions,
        op_args=[API_PREDICT_URL]
    )

    insert_data_task = PythonOperator(
        task_id = "insert_data",
        python_callable=insert_data
    )

    fetch_data_task >> clean_data_task >> generate_predictions_task >> insert_data_task