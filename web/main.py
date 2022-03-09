from flask import Flask
from config import MONGO_URI
from flask_pymongo import PyMongo
from route.rootRoutes import main_route

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

app.register_blueprint(main_route,url_prefix='/')

if __name__=='__main__':
    app.run(debug=True)



