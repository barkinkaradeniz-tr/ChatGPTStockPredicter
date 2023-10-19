import os
import requests
from datetime import datetime  
from datetime import timedelta  
from dotenv import load_dotenv
from src.mongo.pymongo_get_database import get_database

load_dotenv()

dbname = get_database()
collection_name = dbname["AlphabetNews"]

cursor = collection_name.find().skip(21728)

for item in cursor:
  collection_name.delete_one({"_id": item["_id"]})

dateObj = datetime(2022, 3, 7)

while dateObj != datetime(2023, 7, 22):
  dateFrom = dateObj.strftime("%Y%m%d") + 'T0000'
  dateTo = dateObj.strftime("%Y%m%d") + 'T2359'

  url = ('https://www.alphavantage.co/query?function=NEWS_SENTIMENT&'
        'tickers=GOOG&'
        'time_from={}&'
        'time_to={}&'
        'limit=1000'
        'sort=EARLIEST&'
        'apikey={}').format(dateFrom, dateTo, os.getenv("alphavantageAPIKey"))

  response = requests.get(url)

  for i in range(len(response.json()["feed"])):
    sentimentArray = response.json()["feed"][i]["ticker_sentiment"]

    for j in range(len(sentimentArray)):
      if sentimentArray[j]["ticker"] == "GOOG":
        sentimentObj = sentimentArray[j]

    item = {
      "date" : datetime.strptime(response.json()["feed"][i]["time_published"], "%Y%m%dT%H%M%S").strftime("%Y-%m-%dT%H:%M:%S"),
      "title" : response.json()["feed"][i]["title"],
      "sentiment" : sentimentObj["ticker_sentiment_score"],
      "relevancy" : sentimentObj["relevance_score"]
    }

    collection_name.insert_one(item)

  dateObj = dateObj + timedelta(days=1)
