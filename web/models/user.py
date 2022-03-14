from . import get
import sys

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
                return True
            else:
                flag=False
        except Exception as e:
            print(e)
            flag=False
        return flag

    def doesExist(self,login=0):
        if login==1:
            try:
                flag=get.getDb().deplo.user.find_one({"username":self.username,"password":self.password})
                print('flag value : ',flag,file=sys.stdout)
                return flag
            except Exception as e:
                print(e,file=sys.stdout)
                return False
        else:
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
