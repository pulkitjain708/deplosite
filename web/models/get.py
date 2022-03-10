import config
from pymongo import MongoClient


def getDb():
    mongo = MongoClient(config.MONGO_URI)
    deplo=mongo.deplo
    return deplo