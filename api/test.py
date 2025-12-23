import requests


tweets = requests.get("http://127.0.0.1:8001/batch?batch_size=5").json()

# 2) Print each tweet to see the content
for i, t in enumerate(tweets, 1):
    print(f"\nTweet #{i}")
    print("Airline :", t["airline"])
    print("Sentiment:", t["airline_sentiment_confidence"], "(generator's confidence)")
    print("Text    :", t["text"])