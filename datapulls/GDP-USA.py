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

#write the data from the observations dict into a data frame
df = pd.json_normalize(data["observations"])

# preselect the columns
df = df[["realtime_start", "date", "value"]]

# drop all empty values, they come from the API with a point(.)
df = df[df.value != "."]

# rename realtime_start column
df = df.rename(columns={"realtime_start": "lastpull"})

# change date column to be a datetime
df['date'] = pd.to_datetime(df['date'])
df['lastpull'] = pd.to_datetime(df['lastpull'])

# change data type of value to a float64
df = df.astype({"value": 'float64'})


# Post to SQL
# Create the engine
engine = sqlalchemy.create_engine(Database_URL)

# Write data into the table in PostgreSQL database
df.to_sql('GDP-USA', engine)
