import requests
from datetime import datetime  
from datetime import timedelta  
from src.mongo.pymongo_get_database import get_database


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
        'api_token=644bb53acdefe0.46250516').format(dateString, dateString)

  response = requests.get(url)

  for i in range(len(response.json())):
    item = {
      "date" : response.json()[i]["date"],
      "content" : response.json()[i]["content"]
    }

    collection_name.insert_one(item)

  dateObj = dateObj + timedelta(days=1)

# item_1 = {
#   "item_name" : "Blender",
#   "max_discount" : "10%",
#   "batch_number" : "RR450020FRG",
#   "price" : 340,
#   "category" : "kitchen appliance"
# }

# item_2 = {
#   "item_name" : "Egg",
#   "category" : "food",
#   "quantity" : 12,
#   "price" : 36,
#   "item_description" : "brown country eggs"
# }

# collection_name.insert_many([item_1,item_2])