from flask import session
from functools import wraps
from flask import render_template


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_google = dict(session).get('profile', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user_google:
            return f(*args, **kwargs)
        return render_template('index.html')
    return decorated_function
