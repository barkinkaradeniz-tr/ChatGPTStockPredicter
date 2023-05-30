import os
import openai
from dotenv import load_dotenv
from src.mongo.pymongo_get_database import get_database

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("ORGANIZATION_KEY")

dbname = get_database()
collection_name = dbname["AlphabetNews"]

for item in collection_name.find():
    promptText = "I want you to analyze the next news article I give you, extract a sentiment score from it, and evaluate how positive or negative it is for the company Alphabet. '-10' being extremely negative and '10' being extremely positive. Don't forget to consider relevancy. You are allowed to use floating-point numbers. Don't explain anything further. Don't use any other character. Only '+', '-', '.' and numbers."
    promptText += item["content"]

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": promptText}], top_p=0.1)

    myQuery = {"_id" : item["_id"]}
    newValues = {"$set" : {"sentiment" : completion["choices"][0]["message"]["content"]}}
    collection_name.update_one(myQuery, newValues)
