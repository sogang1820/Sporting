import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGODB_URL)

user_database = client[DATABASE_NAME]
user_collection = user_database["users"]

reservation_database = client[DATABASE_NAME]
reservation_collection = reservation_database["reservations"]

stadium_database = client[DATABASE_NAME]
stadium_collection = stadium_database["stadiums"]
