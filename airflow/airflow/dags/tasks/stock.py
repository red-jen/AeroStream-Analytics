
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
import os


def insert_data(ti):

    db_host = os.environ["POSTGRES_HOST"]
    db_pass = os.environ["POSTGRES_PASSWORD"]
    db_user = os.environ["POSTGRES_USER"]
    db_port = os.environ["POSTGRES_PORT"]
    db_name = os.environ["POSTGRES_DB"]

    ### Create prediction table if it does not exit

    DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)

    Base = declarative_base()

    class Prediction(Base):
        __tablename__ = "predictions"

        id = Column(Integer, primary_key=True)

        label = Column(String(10))
        text = Column(Text)
        airline = Column(String(50))
        airline_sentiment_confidence = Column(Float)
        negativereason = Column(String(50))
        tweet_created = Column(DateTime(timezone=True))
        
        predicted_at = Column(DateTime(timezone=True), server_default=func.now())

    Base.metadata.create_all(bind=engine)

    # Insert data

    data = ti.xcom_pull(task_ids="clean_data")
    predictions = ti.xcom_pull(task_ids="generate_predictions")

    db = SessionLocal()

    try:
        for i in range(len(predictions)):
            prediction = Prediction(
                text=data[i]['text'],
                label=predictions[i],
                airline = data[i]['airline'],
                airline_sentiment_confidence = data[i]['airline_sentiment_confidence'],
                negativereason = data[i]['negativereason'],
                tweet_created = data[i]['tweet_created']
            )
            db.add(prediction)
            
        db.commit()

        print("Les données ont été stockées avec succès !")
    except:
        print("Échec du stockage des données.")
    finally:
        db.close()