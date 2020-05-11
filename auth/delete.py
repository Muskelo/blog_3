import os

from flask_security import current_user

from db import db
from models import User, Role, Icon
from utils import access, access_bigger


# USER

def delete_user_by_id(errors, user_id):
    user = User.query.filter(User.id == user_id).first()

    if not user:
        errors.append("Can't find user by id{}".format(user_id))
        return errors

    errors = delete_user(errors, user)

    return errors


def delete_user(errors, user):
    if not access_bigger(current_user, user):
        errors.append("Your access must be higher than have subject")
        return errors

    if not access(["admin"], user):
        errors.append("no access")
        return errors

    errors = delete_user_body(errors, user)

    return errors


# ROLE

def delete_user_body(errors, user):
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        errors.append("Can't delete user from db,user id{}".format(user.id))

    return errors


def delete_role_by_id(errors, role_id):
    role = Role.query.filter(Role.id == role_id).first()

    if not role:
        errors.append("Can't find role by id{}".format(role_id))
        return errors

    errors = delete_role(errors, role)

    return errors


def delete_role(errors, role):
    if not access(["admin"], role):
        errors.append("no access")
        return errors

    errors = delete_user_body(errors, role)

    return errors


def delete_role_body(errors, role):
    try:
        db.session.delete(role)
        db.session.commit()
    except:
        errors.append("Can't delete role from db,role id{}".format(role.id))

    return errors


# ICON
def delete_icon_by_user(errors, user_id):
    icon = Icon.query.filter(Icon.profile_id == user_id).first()

    if icon:
        errors = delete_icon(errors, icon)

    return errors


def delete_icon_by_id(errors, icon_id):
    icon = Icon.query.filter(Icon.id == icon_id).first()

    if not icon:
        errors.append("Don't find icon by id{}".format(icon_id))
        return errors

    errors = delete_icon(errors, icon)

    return errors


def delete_icon(errors, icon):
    if not access(author=icon.user):
        errors.append("no access")
        return errors

    errors = delete_icon_body(errors, icon)

    return errors


def delete_icon_body(errors, icon):
    # delete
    try:
        os.remove(icon.address)
    except:
        errors.append("can't remove from disk,icon id={}".format(icon.id))

        return errors

    # commit
    try:
        db.session.delete(icon)
        db.session.commit()
    except:
        errors.append("can't remove from db,image id={}".format(icon.id))

    return errors
