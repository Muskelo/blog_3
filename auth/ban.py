from flask_security import current_user

from db import db
from models import User
from utils import access, access_bigger


def ban_user_by_id(errors, user_id):
    user = User.query.filter(User.id == user_id).first()

    if not user:
        errors.append("Can't find user by id {}".format(user_id))
        return errors

    errors = ban_user(errors, user)

    return errors


def ban_user(errors, user):
    if not access(["moder"]):
        errors.append("no access")
        return errors

    if not access_bigger(current_user, user):
        errors.append("Your access must be higher than have subject")
        return errors

    errors = ban_user_body(errors, user)

    return errors


def ban_user_body(errors, user):
    if user.active == 0:
        user.active = 1
    else:
        user.active = 0

    try:
        db.session.commit()
    except:
        errors.append("Can't save in db")

    return errors
