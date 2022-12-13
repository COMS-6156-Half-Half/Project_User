# AS simeple as possbile flask google oAuth 2.0
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from login import login
# decorator for routes that should be accessible only by logged in users
from auth_decorator import login_required
from models import db, Users
from flask_login import LoginManager
from register import register
from home import home
from flask import render_template
from logout import logout


import sqlalchemy
# dotenv setup
# from dotenv import load_dotenv
# load_dotenv()


# App config
app = Flask(__name__)
# Session config
app.secret_key = '12345678'
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id= '734766617604-8lmbqsoqd4100fn0cm1ho69lqdufgak3.apps.googleusercontent.com',
    client_secret= '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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url=CONF_URL,
)




app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:13886003474cjw@e61561.cwsqeuuovxq1.us-east-1.rds.amazonaws.com:3306/user"

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()


app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(home)
app.register_blueprint(logout)

@app.route('/')
@login_required
def hello_world():
    email = dict(session)['profile']['email']
    return render_template('hello_google.html')

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    # user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # # Here you use the profile/user data that you got and query your database find/register the user
    # # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/home_google')

@app.route('/home_google')
def hello_google():
    email = dict(session)['profile']['email']
    return render_template('hello_google.html')


@app.route('/logout_google')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
