from db import db
from models import User, Role
from utils import access


def delete_user_by_id(errors, user_id):
    user = User.query.filter(User.id == user_id).first()

    if not user:
        errors.append("Can't find user by id{}".format(user_id))
        return errors

    errors = delete_user(errors, user)

    return errors


def delete_user(errors, user):
    if not access(["admin"], user):
        errors.append("no access")
        return errors

    errors = delete_user_body(errors, user)

    return errors


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
