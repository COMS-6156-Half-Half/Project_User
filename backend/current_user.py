from flask import Blueprint
from flask import Flask, render_template, session, Blueprint, Response, request
from flask_login import login_required
import json
current_user = Blueprint('current_user', __name__)
from models import db, Users


@current_user.route('/current_user', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        user = Users.query.filter_by(username=username).first()
        if user:
            r = {'userid': str(user.id),
                'user_email': str(user.email)}

            print(r)
            return Response(json.dumps(r), status=200, content_type="application.json")

        else:
            return Response("user-not-found", status=404, content_type="text/plain")



