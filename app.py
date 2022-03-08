from flask import Flask
from db.db import get_db
from routes.root import root

app = Flask(__name__)

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

init_db()


app.register_blueprint(root, url_prefix='/')

if __name__ == '__main__':
    app.debug = True
    app.run()