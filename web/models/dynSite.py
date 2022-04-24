
import sys
import config
from pymongo import MongoClient
from datetime import date


def getDb(collection="dynamic"):
    mongo = MongoClient(config.MONGO_URI)
    return mongo.deplo[collection] if collection else mongo.deplo


class DSite():
    site = {}

    def __init__(self, objectId="", title="", project_path="",date_project=""):
        self.site={
            "userRef": objectId,
            "title": title,
            "path_project":project_path,
            "date":date_project
        }

    def save(self):
        try:
            getDb().insert_one(self.site)
        except Exception as e:
            print(e)

