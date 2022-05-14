
import sys
import config
from pymongo import MongoClient
from datetime import date
from bson.objectid import ObjectId


def getDb(collection="dynamic"):
    mongo = MongoClient(config.MONGO_URI)
    return mongo.deplo[collection] if collection else mongo.deplo


class DSite():
    site = {}

    def __init__(self, objectId="", title="", project_path="", date_project="", stack="php", flag_ec2=False,rootFile="index.html",dbname="db"):
        self.site = {
            "userRef": objectId,
            "title": title,
            "path_project": project_path,
            "date": date_project,
            "stack": stack,
            "ec2_on": flag_ec2,
            "ec2_toggled": False,
            "instanceId":"",
            "deployed":False,
            "rootFile":rootFile,
            "dbname":dbname
        }

    def save(self):
        try:
            getDb().insert_one(self.site)
        except Exception as e:
            print(e)

    def getSites(self, userRef):
        try:
            return getDb().find({"userRef": userRef})
        except Exception as e:
            print(e)

    def getSiteBySiteId(self, siteId):
        try:
            return getDb().find_one({"_id":  ObjectId(siteId)})
        except Exception as e:
            print(e)

    def getName(self, id):
        try:
            title = getDb().find_one({"_id": ObjectId(id)}, {
                "title": 1, "_id": 0})['title']
            return title
        except Exception as e:
            print(e)

    def toggleEC2_ON(self, id):
        getDb().find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": {"ec2_on": True}})

    def setInstanceId(self, siteId, InstanceId):
        getDb().find_one_and_update({"_id": ObjectId(siteId)}, {
            "$set": {"instanceId": InstanceId}})

    def toggleEC2(self, instanceId):
        getDb().find_one_and_update({"instanceId": instanceId},  [
            {"$set": {"ec2_toggled": {"$not": "$ec2_toggled"}}}
        ]
        )

    def setDeployed(self, id):
        getDb().find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": {"deployed": True}})
