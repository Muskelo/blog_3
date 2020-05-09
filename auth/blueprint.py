from flask import Blueprint, abort, render_template, request, redirect
from flask_security import login_required

from auth.ban import ban_user_by_id
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

        if not access(["admin"]):
            errors.append("no access")

            return render_template("auth/profile.html",
                                   access=access,
                                   user=user,
                                   form=form
                                   )
        user.roles = []

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

    errors = ban_user_by_id(errors, user_id)

    if errors:
        return render_template("wrong.html", request=request, errors=errors)

    return redirect(request.referrer)
