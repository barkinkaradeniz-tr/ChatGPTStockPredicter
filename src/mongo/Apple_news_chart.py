from datetime import datetime  
import matplotlib.pyplot as plt
from src.mongo.pymongo_get_database import get_database

dbname = get_database()
collection_name = dbname["AppleNews"]

dateArray = {}

for item in collection_name.find():
  dateArray[datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S+00:00").strftime("%Y-%m-%d")] = 0

for item in collection_name.find():
  dateArray[datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S+00:00").strftime("%Y-%m-%d")] = dateArray[datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S+00:00").strftime("%Y-%m-%d")] + 1

plt.plot(list(dateArray.keys()), list(dateArray.values()))
plt.show()
