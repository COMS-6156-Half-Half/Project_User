from flask import Blueprint, url_for, render_template, redirect, request,  Response
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from models import db, Users
login = Blueprint('login', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(login)

@login.route('/login_account', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = Users.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return Response("Login Success", status=200, content_type="text/plain")
            else:
                return Response("incorrect-password", status=404, content_type="text/plain")

        else:
            return Response("user-not-found", status=404, content_type="text/plain")

    else:
        return Response("method should be Post", status=404, content_type="text/plain")



