# from . import get
import sys
import config
from pymongo import MongoClient


def getDb(collection="user"):
    try:
        mongo = MongoClient(config.MONGO_URI)
        print("Connection Object , ", mongo)
        return mongo.deplo[collection] if collection else mongo.deplo
    except Exception as e:
        print(e, " : Error at Connecting DB")


class User():
    user = {}

    def __init__(self, username="", email="", password=""):
        self.username = username
        self.email = email
        self.password = password

        self.user = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def getId(self):
        flag = getDb().find_one(
            {"username": self.username, "email": self.email}, {"_id": 1})
        if flag:
            return flag["_id"]
        else:
            return flag

    def save(self):
        try:
            flag = self.doesExist()
            if flag == False:
                getDb().insert_one(self.user)
                return True
            else:
                flag = False
        except Exception as e:
            print(e)
            flag = False
        return flag

    def doesExist(self, login=0):
        if login == 1:
            try:
                flag = getDb().find_one(
                    {"username": self.username, "password": self.password})
                print('flag value : ', flag, file=sys.stdout)
                return flag
            except Exception as e:
                print(e, file=sys.stdout)
                return False
        else:
            try:
                username = getDb().find_one({"username": self.username})
                email = getDb().find_one({"email": self.email})
                if (username and email) or (username or email):
                    flag = True
                else:
                    flag = False
            except Exception as e:
                flag = True
                print(e)
            return flag
