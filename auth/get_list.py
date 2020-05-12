from flask import request

from models import User, Role


def get_user_list(errors):
    log = ""

    search = request.args.get("search")
    roles = request.args.get("roles")

    list__items = User.query

    # FILTERS

    if search:
        list__items = list__items.filter(User.email.contains(search))
        log += "&search=" + search

    if roles:
        log += "&roles=" + roles
        roles = roles.split(" ")

        for role in roles:
            role_ = Role.query.filter(Role.name == role).first()

            if role_:
                list__items = list__items.filter(User.roles.contains(role_))
            else:
                errors.append("Don't find {} role".format(role.name))

    return [list__items, log, errors]


def get_role_list(errors):
    log = ""

    search = request.args.get("search")
    list__items = Role.query

    # FILTERS

    if search:
        list__items = list__items.filter(Role.name.contains(search))
        log += "&search=" + search

    return [list__items, log, errors]
