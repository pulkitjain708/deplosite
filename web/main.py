from flask import Flask 
import config
import routes
from s3logger import periodic
from timeloop import Timeloop
from datetime import timedelta

t=Timeloop()

@t.job(interval=timedelta(minutes=3))
def every2hrs():
    periodic()

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['MAX_CONTENT_LENGTH'] = 15 * 1000 * 1000

app.register_blueprint(routes.mainRoutes.slash,url_prefix='/')
app.register_blueprint(routes.dashRoutes.dash,url_prefix='/dashboard')
app.register_blueprint(routes.s3Routes.s3RouteBP,url_prefix='/s3')

if __name__=='__main__':
    app.run(debug=True)



