from flask import request

from db import db
from models import Role
from utils import access
from .forms import create_role_form


def edit_role_by_id(errors, role_id, args={}):
    role = Role.query.filter(Role.id == role_id).first()

    if not role:
        errors.append("Can't find by id {}".format(role_id))
        return errors, args

    errors, args = edit_role(errors, role)

    return errors, args


def edit_role(errors, role, args={}):
    if not access(["God"]):
        errors.append("no access")
        return errors, args

    errors, args = edit_role_body(errors, role)

    return errors, args


def edit_role_body(errors, role, args={}):
    form = create_role_form()

    if request.method == "POST":
        # SAVE UPDATE

        role.name = form.name.data
        role.description = form.description.data

        if not errors:
            db.session.commit()

    # POST FORM
    form.name.data = role.name
    form.description.data = role.description

    args["form"] = form

    return errors, args
