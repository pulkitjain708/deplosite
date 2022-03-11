from flask import Flask
from flask_mongoengine import MongoEngine
import config
import routes

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['MAX_CONTENT_LENGTH'] = 15 * 1000 * 1000

app.register_blueprint(routes.mainRoutes.slash,url_prefix='/')
app.register_blueprint(routes.dashRoutes.dash,url_prefix='/dashboard')
app.register_blueprint(routes.uploadRoutes.upload,url_prefix='/upload')

if __name__=='__main__':
    app.run(debug=True)



