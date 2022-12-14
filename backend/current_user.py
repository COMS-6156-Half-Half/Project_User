from flask import Blueprint
from flask import Flask, render_template, session, Blueprint, Response
from flask_login import login_required
import json
current_user = Blueprint('current_user', __name__)

@current_user.route('/current_user')
def index():
    if '_user_id' not in session:
        return Response("User not log in", status=404, content_type="text/plain")
    else:
        user_id = session['_user_id']
        result = {'user_id': user_id}
        return Response(json.dumps(result), status=200, content_type="application.json")

