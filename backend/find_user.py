from flask import Blueprint, request
from flask import Flask, render_template, session, Blueprint, Response
from flask_login import login_required
import json
from models import db, Users


find_user = Blueprint('find_user', __name__)

@find_user.route('/find_user', methods=['GET', 'POST'])
def index():
    data = request.get_json()
    print(data['id'])
    id = int(data['id'])
    user = Users.query.filter_by(id=id).first()
    if user:
        r = {'user_email': str(user.email)}
        return Response(json.dumps(r), status=200, content_type="application.json")

    else:
        return Response("User not found", status=404, content_type="text/plain")

