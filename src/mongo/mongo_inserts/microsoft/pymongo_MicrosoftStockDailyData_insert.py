import os
import requests
from datetime import datetime
from datetime import timedelta  
from dotenv import load_dotenv
from src.mongo.pymongo_get_database import get_database

load_dotenv()

dbname = get_database()
collection_name = dbname["MicrosoftDailyStockData"]

url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED'
         '&symbol=MSFT'
         '&outputsize=full'
         '&apikey={}').format(os.getenv("alphavantageAPIKey"))

response = requests.get(url)
dailyPrices = response.json()["Time Series (Daily)"]

print(response.json())

dateObj = datetime(2022, 3, 7)
while dateObj != datetime(2023, 7, 22):
  if(dailyPrices.keys().__contains__(dateObj.strftime("%Y-%m-%d"))):

    item = {
        "Date" : dateObj.strftime("%Y-%m-%d"),
        "Close" : dailyPrices[dateObj.strftime("%Y-%m-%d")]["5. adjusted close"],
    } 

    collection_name.insert_one(item)
  
  dateObj = dateObj + timedelta(days=1)
