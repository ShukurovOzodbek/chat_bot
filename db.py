from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

client = MongoClient(config["MONGODB_URI"])

db = client['chat_bot']

USERS = db['users']

