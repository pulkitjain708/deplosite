import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True

DATABASE='deplo'

MONGO_URI='mongodb+srv://root:root@deplo.tevs8.mongodb.net/{DATABASE}?retryWrites=true&w=majority'
