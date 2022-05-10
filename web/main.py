from hmac import new
from flask import Flask, redirect, request as req, session, flash
from google_auth_oauthlib.flow import Flow
import config
import routes
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests
from random import randint
from models.user import User
from flask_cors import CORS

flow = Flow.from_client_secrets_file(
    client_secrets_file=config.CLIENT_SECRET_PATH,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri='http://127.0.0.1:5000/callback'
)

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')
app.config['MAX_CONTENT_LENGTH'] = 15 * 1000 * 1000


@app.route("/loginwithgoogle")
def serveGoogleRedirect():
    auth_url, state = flow.authorization_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():

    flow.fetch_token(
        authorization_response=req.url.replace("http", "https")
    )
    try:
        if session['username']:
            return redirect("/dashboard")
    except:
        return redirect("/")

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=config.GCID
    )

    google_id = id_info.get("sub")
    username = id_info.get("name")
    email = id_info.get("email")
    newUserName="{}{}".format(
        username, randint(99, 999)).replace(" ", "")
    user = User(password="g_oauth", username=newUserName, email=email)
    if not user.doesExist():
        user.save()
        id = user.getId()
        session["id"] = "{}".format(id)
        session['username'] = newUserName
        print(id, "-----------------------")
        return redirect("/dashboard")
    else:
        flash('Try Registering , Username or Mail already exists')
        return redirect('/register')


app.register_blueprint(routes.mainRoutes.slash, url_prefix='/')
app.register_blueprint(routes.dashRoutes.dash, url_prefix='/dashboard')
app.register_blueprint(routes.s3Routes.s3RouteBP, url_prefix='/s3')
app.register_blueprint(routes.dynamicRoutes.dynamicBP, url_prefix='/dynamic')

if __name__ == '__main__':
    app.run(debug=True)
