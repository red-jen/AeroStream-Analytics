"""
AeroStream Pipeline DAG
=======================
Pipeline: Fetch → Clean → Predict → (Auto-save to DB)

Ce DAG s'exécute toutes les minutes pour:
1. Récupérer des tweets depuis l'API générateur
2. Nettoyer le texte des tweets
3. Prédire le sentiment et sauvegarder en base
"""
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import des tâches
from tasks.fetch import fetch_tweets
from tasks.clean import clean_tweets
from tasks.predict import predict_sentiment

# ============================================
# CONFIGURATION
# ============================================
# Note: host.docker.internal = accès à localhost depuis Docker
TWEET_API_URL = "http://host.docker.internal:8001"    # Générateur de tweets
PREDICT_API_URL = "http://host.docker.internal:8000"  # API de prédiction
BATCH_SIZE = 10                                        # Tweets par exécution

# ============================================
# DÉFINITION DU DAG
# ============================================
with DAG(
    dag_id="aerostream_dag",
    description="Pipeline de classification des sentiments",
    start_date=datetime(2025, 1, 1),
    schedule_interval="*/1 * * * *",  # Toutes les 1 minute
    catchup=False,                     # Ne pas exécuter les anciens runs
) as dag:

    # Tâche 1: Récupérer les tweets
    task_fetch = PythonOperator(
        task_id="fetch_tweets",
        python_callable=fetch_tweets,
        op_args=[TWEET_API_URL, BATCH_SIZE],
    )

    # Tâche 2: Nettoyer les tweets
    task_clean = PythonOperator(
        task_id="clean_tweets",
        python_callable=clean_tweets,
    )

    # Tâche 3: Prédire et sauvegarder
    task_predict = PythonOperator(
        task_id="predict_sentiment",
        python_callable=predict_sentiment,
        op_args=[PREDICT_API_URL],
    )

    # ============================================
    # ORDRE D'EXÉCUTION (Pipeline)
    # ============================================
    task_fetch >> task_clean >> task_predict

