from flask import Blueprint

auth = Blueprint('auth', __name__,
                 template_folder='templates',
                 static_folder='static')


@auth.route('create_user/', methods=['GET', 'POST'])
def create_user():
    return "hi"
