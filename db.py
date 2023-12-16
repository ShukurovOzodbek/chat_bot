from pymongo import MongoClient
from dotenv import get_variables

config = get_variables(".env")

client = MongoClient(config["MONGODB_URI"])

db = client['chat_bot']

USERS = db['users']

