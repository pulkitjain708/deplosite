import os
from platform import system

SECRET_KEY = "secretkeyforflaskapp"

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASE='deplo'

# MONGO_URI='mongodb+srv://root:root@deplo.tevs8.mongodb.net/{DATABASE}?retryWrites=true&w=majority'
MONGO_URI='mongodb://localhost:27017/deplo'
MAX_CONTENT_LENGTH=15*1000*1000

#for linux
# '~/project/uploads'
#for wsl
#/mnt/c/Users/intern/project/uploads
if system()=="Windows":
    UPLOAD_PATH="C:\\Users\\intern\\project\\uploads\\"
    delimiter="\\"
elif system()=="Linux":
    UPLOAD_PATH='/mnt/c/Users/intern/project/uploads'
    delimiter="/"

ALLOWED=['htm','html','js','css','png','jpeg','jpg','txt','csv','svg']

HCTI_ID="847ba16c-d12f-4720-83d6-efa8bd9eeaeb"
HCTI_KEY="68444419-2562-4eda-9342-a012ccb4d5c9"