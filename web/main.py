from flask import Flask , redirect , request as req
from google_auth_oauthlib.flow import Flow 
import config
import routes
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests

flow = Flow.from_client_secrets_file(
    client_secrets_file=config.CLIENT_SECRET_PATH,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
            redirect_uri='http://127.0.0.1:5000/callback'
)

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['MAX_CONTENT_LENGTH'] = 15 * 1000 * 1000

@app.route("/loginwithgoogle")
def serveGoogleRedirect():
    auth_url,state=flow.authorization_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    
    flow.fetch_token(
        authorization_response=req.url.replace("http","https")
        )
    # if not session["state"] == request.args["state"]:
    #     abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=config.GCID
    )

    google_id = id_info.get("sub")
    username = id_info.get("name")
    email = id_info.get("email")

    return redirect("/")

app.register_blueprint(routes.mainRoutes.slash, url_prefix='/')
app.register_blueprint(routes.dashRoutes.dash, url_prefix='/dashboard')
app.register_blueprint(routes.s3Routes.s3RouteBP, url_prefix='/s3')

if __name__ == '__main__':
    app.run(debug=True)
