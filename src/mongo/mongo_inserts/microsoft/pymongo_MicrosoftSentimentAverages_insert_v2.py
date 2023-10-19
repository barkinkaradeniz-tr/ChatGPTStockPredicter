import numpy as np
from datetime import datetime  
from datetime import timedelta  
from src.mongo.pymongo_get_database import get_database


dbname = get_database()
dailyChange = dbname["MicrosoftDailyChange"]
articles = dbname["MicrosoftNews"]
sentimentAverages = dbname["MicrosoftSentimentAveragesUpdated"]

articlesCursor = articles.find().sort("date")

counter = 0

for change in dailyChange.find():
    dayBeginning = change["date"] + "T14:30:00+00:00"
    dayEnding = change["date"] + "T21:00:00+00:00"
    
    numerator = 0
    denominator = 0 

    for article in articlesCursor:
        if dayEnding > article["date"]:
            numerator += float(article["sentiment"])
            denominator += 1
            counter += 1

    articlesCursor = articlesCursor.clone()[counter:]
    
    if(denominator != 0):
        item = {
            "date" : change["date"],
            "sentimentAverage" : numerator / denominator
        }

        sentimentAverages.insert_one(item)
    else:
        item = {
            "date" : change["date"],
            "sentimentAverage" : 99
        }

        sentimentAverages.insert_one(item)

    