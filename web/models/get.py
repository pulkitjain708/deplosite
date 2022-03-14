import config
from pymongo import MongoClient


def getDb(collection=None):
    mongo = MongoClient(config.MONGO_URI)
    return mongo.deplo[collection] if collection else mongo.deplo