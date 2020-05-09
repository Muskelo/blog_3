from flask import request

from models import Tag, Post, User


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
