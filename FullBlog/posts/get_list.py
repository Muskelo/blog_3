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
        log += "&search=" + search
        list__items = list__items.filter(Post.title.contains(search) |
                                         Post.text.contains(search))

    if search_by_tag:
        log += "&tag=" + search_by_tag
        tags = search_by_tag.split(" ")

        for tag in tags:
            tag_ = Tag.query.filter(Tag.name == tag).first()

            if tag_:
                list__items = list__items.filter(Post.tags.contains(tag_))
            else:
                errors.append("Can'f find tag {}".format(tag))

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
