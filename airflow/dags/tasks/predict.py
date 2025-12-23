"""
Task 3: Predict sentiment using the Prediction API
"""
import requests

def predict_sentiment(api_url, ti):
    """
    Envoie les tweets à l'API de prédiction
    
    Args:
        api_url: URL de l'API (ex: http://host.docker.internal:8000)
        ti: TaskInstance (pour récupérer les données)
    
    Returns:
        Résultat des prédictions
    """
    # Récupérer les tweets nettoyés
    tweets = ti.xcom_pull(task_ids='clean_tweets')
    
    # Préparer le payload pour l'API
    payload = {
        "tweets": [
            {
                "text": t["text"],
                "airline": t["airline"],
                "tweet_created": t["tweet_created"]
            }
            for t in tweets
        ]
    }
    
    # Appeler l'API de prédiction
    response = requests.post(f"{api_url}/predict_batch", json=payload)
    
    if response.status_code != 200:
        print(f"Erreur: {response.status_code}")
        return None
    
    result = response.json()
    print(f"✅ {result['count']} prédictions générées")
    print(f"✅ Sauvegardé en DB: {result['saved_to_db']}")
    
    return result

