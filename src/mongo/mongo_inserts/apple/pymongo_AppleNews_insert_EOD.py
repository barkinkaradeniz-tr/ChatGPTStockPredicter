import os
import requests
from datetime import datetime  
from datetime import timedelta  
from src.mongo.pymongo_get_database import get_database

from dotenv import load_dotenv
load_dotenv()

dbname = get_database()
collection_name = dbname["AppleNews"]

dateObj = datetime(2021, 1, 3)

while dateObj != datetime(2023, 4, 2):
  dateString = dateObj.strftime("%Y-%m-%d")

  url = ('https://eodhistoricaldata.com/api/news?'
        's=AAPL&'
        'language=en&'
        'from={}&'
        'to={}&'
        'api_token={}').format(dateString, dateString, os.getenv("eodhistoricaldataAPIKey"))

  response = requests.get(url)

  for i in range(len(response.json())):
    item = {
      "date" : response.json()[i]["date"],
      "content" : response.json()[i]["content"]
    }

    collection_name.insert_one(item)

  dateObj = dateObj + timedelta(days=1)
