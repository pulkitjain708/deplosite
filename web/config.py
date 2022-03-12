import os
from platform import system

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASE='deplo'

MONGO_URI='mongodb+srv://root:root@deplo.tevs8.mongodb.net/{DATABASE}?retryWrites=true&w=majority'

MAX_CONTENT_LENGTH=15*1000*1000

if system()=="Windows":
    UPLOAD_PATH="C:\\Users\\intern\\project\\uploads\\"
elif system()=="Linux":
    UPLOAD_PATH='~/deplosite/uploads'

ALLOWED=['htm','html','js','css','png','jpeg','jpg','txt','csv',"py"]