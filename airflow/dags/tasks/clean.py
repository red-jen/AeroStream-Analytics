"""
Task 2: Clean the tweet text
"""
import re

def clean_tweets(ti):
    """
    Nettoie le texte des tweets (supprime @mentions, espaces)
    
    Args:
        ti: TaskInstance (pour récupérer les données de la tâche précédente)
    
    Returns:
        Liste de tweets nettoyés
    """
    # Récupérer les tweets de la tâche précédente (XCom)
    tweets = ti.xcom_pull(task_ids='fetch_tweets')
    
    # Nettoyer chaque tweet
    for tweet in tweets:
        text = tweet['text']
        text = re.sub(r'@\w+', '', text)      # Supprimer @mentions
        text = re.sub(r'\s+', ' ', text)       # Supprimer espaces multiples
        text = text.strip()                     # Supprimer espaces début/fin
        tweet['text'] = text
    
    print(f"✅ {len(tweets)} tweets nettoyés")
    
    return tweets

