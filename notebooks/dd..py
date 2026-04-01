from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:Ren-ji24@localhost:5432/aerostream"
engine = create_engine(DATABASE_URL)

# Example: Fetching data using raw SQL
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM tweet_predictions"))
    for row in result:
        print(row)

