from flask import request

from models import Tag, Post, User, Role


def get_post_list(errors):
    log = ""

    search_by_tag = request.args.get("tag")
    search = request.args.get("search")
    author = request.args.get("author")

    # GET LIST

    list__items = Post.query.order_by(Post.created.desc())

    if search:
        list__items = list__items.filter(Post.title.contains(search) |
                                         Post.text.contains(search))

        log += "&search=" + search

    if search_by_tag:
        tag = Tag.query.filter(Tag.name == search_by_tag).first()

        if tag:
            list__items = list__items.filter(Post.tags.contains(tag))

            log += "&tag=" + tag.name
        else:
            errors.append("not such tag")

    if author:
        author_ = User.query.filter(User.email == author).first()

        if author_:
            list__items = list__items.filter(Post.author == author_)

            log += "&author=" + author
        else:
            errors.append("not such author")

            # LOG

    return [list__items, log, errors]


def get_tag_list(errors):
    search = request.args.get("search")

    if search:
        list__items = Tag.query.filter(Tag.name.contains(search))
        log = "&search=" + search
    else:
        list__items = Tag.query
        log = ""

    return [list__items, log, errors]


def get_user_list(errors):
    log = ""

    search = request.args.get("search")
    roles = request.args.get("roles")
    print(roles)

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
                errors.append("Don't find {} role".format(role))

    return [list__items, log, errors]
