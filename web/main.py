from flask import Flask
from flask_mongoengine import MongoEngine
import config
import routes

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(routes.mainRoutes.slash,url_prefix='/')
app.register_blueprint(routes.dashRoutes.dash,url_prefix='/dashboard')

if __name__=='__main__':
    app.run(debug=True)



