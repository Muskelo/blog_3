from flask import Blueprint, abort, render_template, request,redirect
from flask_security import current_user, login_required

from auth.forms import SelectRoleForm
from db import db
from models import User, Role

from utils import access

auth = Blueprint('auth', __name__,
                 template_folder='templates',
                 static_folder='static')


@auth.route('read_user/<user_id>', methods=['GET', 'POST'])
def read_user(user_id):
    errors = []

    # search
    user = User.query.filter(User.id == user_id).first()

    if not user:
        abort(404)

    # FORM

    form = SelectRoleForm()

    #  EDIT ROLES

    if request.method == "POST":
        user.roles = []

        if not access(["admin"]):
            errors.append("no access")

            return render_template("auth/profile.html",
                                   access=access,
                                   user=user,
                                   form=form
                                   )

        for role in form.roles.data:
            user.roles.append(Role.query.filter(Role.id == int(role)).first())

        if not errors:
            db.session.commit()

    # PUT ROLE IN FORM

    form.roles.data = []

    for role in user.roles:
        form.roles.data.append(str(role.id))

    return render_template("auth/profile.html",
                           access=access,
                           user=user,
                           form=form
                           )


@auth.route('ban_user/<user_id>', methods=['POST'])
@login_required
def ban_user(user_id):
    errors = []

    # search

    user = User.query.filter(User.id == user_id).first()

    if not user:
        errors.append("Not find user by id {}".format(user_id))

    # access
    if not access(["moder"]):
        errors.append("no access")

    if not errors:
        if user.active == 0:
            user.active = 1
        else:
            user.active = 0

        db.session.commit()

    return redirect(request.referrer)
