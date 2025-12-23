"""
Task 1: Fetch tweets from the Tweet Generator API
"""
import requests

def fetch_tweets(api_url, batch_size):
    """
    Appelle l'API pour récupérer des tweets
    
    Args:
        api_url: URL de l'API (ex: http://host.docker.internal:8001)
        batch_size: Nombre de tweets à récupérer
    
    Returns:
        Liste de tweets (dictionnaires)
    """
    # Appel API
    response = requests.get(f"{api_url}/batch?batch_size={batch_size}")
    
    # Vérifier si succès
    if response.status_code != 200:
        print(f"Erreur: {response.status_code}")
        return []
    
    tweets = response.json()
    print(f"✅ {len(tweets)} tweets récupérés")
    
    return tweets

