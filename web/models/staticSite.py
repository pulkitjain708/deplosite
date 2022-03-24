
import sys
import config
from pymongo import MongoClient
from datetime import date


def getDb(collection="static"):
    mongo = MongoClient(config.MONGO_URI)
    return mongo.deplo[collection] if collection else mongo.deplo


class Site():
    site = {}

    def __init__(self, objectId="", title="", root="index.html", description="", error="index.html", bucketName="", url="", img=""):
        self.site = {
            "userRef": objectId,
            "title": title,
            "root": root,
            "error": error,
            "desc": description,
            'bucketName': bucketName,
            'url': url,
            'img': img,
            'date':date.today()
        }

    def save(self):
        try:
            getDb().insert_one(self.site)
        except Exception as e:
            print(e)

    def getStaticSitesByUser(self, refId, projection):
        try:
            return getDb().find({"userRef": refId}, projection)
        except Exception as e:
            print(e)

    def userHasBucket(self, userId, bucketName):
        try:
            doc = getDb().find_one({"userRef": userId, "bucketName": bucketName})
            return doc if doc else False
        except Exception as e:
            print(e)
            return False
