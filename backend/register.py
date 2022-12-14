from flask import Blueprint, url_for, render_template, redirect, request, Response
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlalchemy
from models import db, Users

register = Blueprint('register', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(register)

@register.route('/register', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm-password']

        if username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(
                    password, method='sha256')
                try:
                    new_user = Users(
                        username=username,
                        email=email,
                        password=hashed_password,
                    )

                    db.session.add(new_user)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    return Response("User-or-email-exists", status=404, content_type="text/plain")

                return Response("Account-Created", status=200, content_type="text/plain")
        else:
            return Response("Missing-fields", status=404, content_type="text/plain")
    else:
        return Response("Method should be POST", status=404, content_type="text/plain")
