from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import re
from sentence_transformers import SentenceTransformer
import psycopg2
from contextlib import contextmanager

# FastAPI app (open `http://127.0.0.1:8000/docs` to try endpoints)
app = FastAPI(title="AeroStream Sentiment Prediction API", version="1.0")

# Load once when the API starts (so each request is fast)
print("Loading model and embedder...")
clf = joblib.load("models/logreg_embedding.joblib")
embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
print("Ready!")

# PostgreSQL connection settings (where predictions will be stored)
DB_CONFIG = {
    "host": "localhost",
    "database": "aerostream",
    "user": "postgres",
    "password": "Ren-ji24",
    "port": 5432
}

# Small helper so we always close the DB connection properly
@contextmanager
def get_db():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

# Basic cleaning: remove @mentions + URLs + extra spaces
def clean_text(text: str) -> str:
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --- Request / Response schemas (Pydantic) ---
class TweetInput(BaseModel):
    text: str
    airline: str = None
    tweet_created: str = None

class PredictionOutput(BaseModel):
    text: str
    airline: str
    tweet_created: str
    predicted_sentiment: str  # "negative" | "neutral" | "positive"
    confidence: float         # model confidence (0..1)

class BatchInput(BaseModel):
    tweets: List[TweetInput]

class BatchOutput(BaseModel):
    predictions: List[PredictionOutput]
    saved_to_db: bool
    count: int

# Quick check endpoint (useful for Docker / monitoring)
@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "logreg_embedding"}

# Predict ONE tweet + save it in PostgreSQL
@app.post("/predict", response_model=PredictionOutput)
def predict_single(tweet: TweetInput):
    text_clean = clean_text(tweet.text)
    embedding = embedder.encode([text_clean])  # text -> vector
    
    prediction = clf.predict(embedding)[0]
    probabilities = clf.predict_proba(embedding)[0]
    confidence = round(float(max(probabilities)), 3)
    
    labels = {0: "negative", 1: "neutral", 2: "positive"}
    sentiment = labels[prediction]
    
    # Save to DB (raw text + predicted label + confidence)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tweet_predictions (text, airline, tweet_created, predicted_sentiment, confidence)
            VALUES (%s, %s, %s, %s, %s)
        """, (tweet.text, tweet.airline or "Unknown", tweet.tweet_created, sentiment, confidence))
        conn.commit()
        cur.close()
    
    return PredictionOutput(
        text=tweet.text,
        airline=tweet.airline or "Unknown",
        tweet_created=tweet.tweet_created or "",
        predicted_sentiment=sentiment,
        confidence=confidence
    )

# Predict a LIST of tweets + save them in PostgreSQL
@app.post("/predict_batch", response_model=BatchOutput)
def predict_batch(batch: BatchInput):
    results = []
    
    texts_clean = [clean_text(t.text) for t in batch.tweets]
    embeddings = embedder.encode(texts_clean)  # list[text] -> matrix[vectors]
    predictions = clf.predict(embeddings)
    probabilities = clf.predict_proba(embeddings)
    
    labels = {0: "negative", 1: "neutral", 2: "positive"}
    
    # Build API response objects
    for i, tweet in enumerate(batch.tweets):
        results.append(PredictionOutput(
            text=tweet.text,
            airline=tweet.airline or "Unknown",
            tweet_created=tweet.tweet_created or "",
            predicted_sentiment=labels[predictions[i]],
            confidence=round(float(max(probabilities[i])), 3)
        ))
    
    # Insert all rows in one DB call (faster than many INSERTs)
    with get_db() as conn:
        cur = conn.cursor()
        data = [(r.text, r.airline, r.tweet_created or None, r.predicted_sentiment, r.confidence) 
                for r in results]
        cur.executemany("""
            INSERT INTO tweet_predictions (text, airline, tweet_created, predicted_sentiment, confidence)
            VALUES (%s, %s, %s, %s, %s)
        """, data)
        conn.commit()
        cur.close()
    
    return BatchOutput(predictions=results, saved_to_db=True, count=len(results))

# Read recent rows (dashboard uses this)
@app.get("/predictions")
def get_predictions(limit: int = 100):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT text, airline, predicted_sentiment, confidence, processed_at
            FROM tweet_predictions
            ORDER BY processed_at DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        cur.close()
    
    return [
        {
            "text": row[0],
            "airline": row[1],
            "sentiment": row[2],
            "confidence": row[3],
            "processed_at": row[4].isoformat() if row[4] else None
        }
        for row in rows
    ]

# Aggregations for quick dashboard KPIs / charts
@app.get("/stats")
def get_stats():
    with get_db() as conn:
        cur = conn.cursor()
        
        # Total rows
        cur.execute("SELECT COUNT(*) FROM tweet_predictions")
        total = cur.fetchone()[0]
        
        # Group by sentiment
        cur.execute("""
            SELECT predicted_sentiment, COUNT(*) 
            FROM tweet_predictions 
            GROUP BY predicted_sentiment
        """)
        by_sentiment = dict(cur.fetchall())
        
        # Group by airline
        cur.execute("""
            SELECT airline, COUNT(*) 
            FROM tweet_predictions 
            GROUP BY airline
            ORDER BY COUNT(*) DESC
        """)
        by_airline = dict(cur.fetchall())
        
        cur.close()
    
    return {
        "total_predictions": total,
        "by_sentiment": by_sentiment,
        "by_airline": by_airline
    }
