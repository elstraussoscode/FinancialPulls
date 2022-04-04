import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os
import sqlalchemy

load_dotenv()

api_key = os.getenv("api_key_fred")
Database_URL = os.getenv("DATABASE_URL")
if Database_URL and Database_URL.startswith("postgres://"):
    Database_URL = Database_URL.replace("postgres://", "postgresql://", 1)

parameters = {
    "series_id": "GDP",
    "api_key": api_key,
    "file_type": "json",
}

# Pull data from API
res = requests.get(url="https://api.stlouisfed.org/fred/series/observations", params=parameters)
data = res.json()
#print(data["observations"])
df = pd.json_normalize(data["observations"])
print(df)


#Post to SQL
engine = sqlalchemy.create_engine(Database_URL)
# Write data into the table in PostgreSQL database
df.to_sql('GDP-USA', engine)