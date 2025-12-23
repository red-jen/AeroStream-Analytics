"""
Simple DAG to test Airflow is working
"""
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# 1) Define the DAG
with DAG(
    dag_id="hello_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # Manual trigger only
    catchup=False,
) as dag:

    # 2) Simple task: print hello
    def say_hello():
        print("Hello from Airflow!")
        return "Success"

    hello_task = PythonOperator(
        task_id="say_hello",
        python_callable=say_hello,
    )

