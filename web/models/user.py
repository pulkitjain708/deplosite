from . import get
import sys
from flask import flash

class User():
    user={}
    def __init__(self,username="",email="",password=""):
        self.username=username
        self.email=email
        self.password=password

        self.user={
            "username":self.username,
            "email":self.email,
            "password":self.password
        }

    def save(self):
        try:
            flag=self.doesExist()
            if flag == False:
                get.getDb().deplo.user.insert_one(self.user)
                flag=True
            else:
                flag=False
        except Exception as e:
            print(e)
            flag=False
        return flag

    def doesExist(self):
        try:
            username=get.getDb().deplo.user.find_one({"username":self.username})
            email=get.getDb().deplo.user.find_one({"email":self.email})
            if (username and email) or (username or email):
                flag=True
            else:
                flag=False
        except Exception as e:
            flag=True
            print(e)
        return flag
