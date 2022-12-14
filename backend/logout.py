from flask import Blueprint, url_for, redirect, Response
from flask_login import LoginManager, login_required, logout_user

logout = Blueprint('logout', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(logout)

@logout.route('/logout')
@login_required
def show():
    logout_user()
    return Response("Logout Success", status=200, content_type="text/plain")