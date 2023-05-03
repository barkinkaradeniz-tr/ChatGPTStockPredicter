import requests
from datetime import datetime  
from datetime import timedelta  
from src.mongo.pymongo_get_database import get_database


dbname = get_database()
collection_name = dbname["AlphabetNews"]

dateObj = datetime(2021, 1, 3)

while dateObj != datetime(2023, 4, 2):
  dateString = dateObj.strftime("%Y-%m-%d")

  url = ('https://eodhistoricaldata.com/api/news?'
        's=GOOG&'
        'language=en&'
        'from={}&'
        'to={}&'
        'api_token=644bb53acdefe0.46250516').format(dateString, dateString)

  response = requests.get(url)

  for i in range(len(response.json())):
    item = {
      "date" : response.json()[i]["date"],
      "content" : response.json()[i]["content"]
    }

    collection_name.insert_one(item)

  dateObj = dateObj + timedelta(days=1)
