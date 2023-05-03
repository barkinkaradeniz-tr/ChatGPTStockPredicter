import requests
from datetime import datetime
from src.mongo.pymongo_get_database import get_database

dbname = get_database()
collection_name = dbname["AlphabetDailyChange"]

fromDateObj = datetime(2020, 12, 31)
fromDateString = fromDateObj.strftime("%Y-%m-%d")
toDateObj = datetime(2023, 4, 1)
toDateString = toDateObj.strftime("%Y-%m-%d")

url = ('https://eodhistoricaldata.com/api/eod/GOOG.US?'
      'fmt=json&'
      'from={}&'
      'to={}&'
      'api_token=644bb53acdefe0.46250516').format(fromDateObj, toDateObj)

response = requests.get(url)

for i in range(1, len(response.json())):
  priceDif = response.json()[i]["adjusted_close"] - response.json()[i - 1]["adjusted_close"]
  difPercentage = priceDif / response.json()[i]["open"] * 100
  
  item = {
    "date" : response.json()[i]["date"],
    "dailyDifferencePercentage" : '{:.2f}'.format(difPercentage)
  }

  collection_name.insert_one(item)
