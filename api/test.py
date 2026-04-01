from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI(title="Prediction Filter API", version="1.0")

mock_predictions = [
    {"text": "Flight delayed", "airline": "United", "sentiment": "negative", "confidence": 0.9},
    {"text": "Great service", "airline": "Delta", "sentiment": "positive", "confidence": 0.95},
]
@app.get("/")
def read_root():
    return {"message": "welcome to FastApi!"}


class Prediction(BaseModel):
    text: str
    airline: str
    sentiment: str
    confidence: float




@app.get("/predictions", response_model=List[dict])
def get_predictions():
    return mock_predictions






@app.get("/prediction/filter", response_model=List[Prediction])
def filter_predictions(airline: str, limit: int = 50):
    # Filter predictions by airline
    filtered = [p for p in mock_predictions if p["airline"].lower() == airline.lower()]
    # Limit the results
    return filtered[:limit]















@app.get("/prediction/filter" , response_model=List[dict])
def filter_prediction(airline: str , limit:30):
    dd = [b for b in mock_predictions if b['airline'].lower() == airline.lower]
    return dd[:limit]