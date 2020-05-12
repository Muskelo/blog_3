from flask import request

from db import db
from models import Tag, Image, Post, Comment
from utils import access, save_image_to_post
from .forms import create_tag_form, create_post_form, create_comment_form


# TAG

def edit_tag_by_id(errors, tag_id, args={}):
    tag = Tag.query.filter(Tag.id == tag_id).first()

    if not tag:
        errors.append("Can't find by id {}".format(tag_id))
        return errors, args

    errors, args = edit_tag(errors, tag)

    return errors, args


def edit_tag(errors, tag, args={}):
    if not access(["moder"]):
        errors.append("no access")
        return errors, args

    errors, args = edit_tag_body(errors, tag)

    return errors, args


def edit_tag_body(errors, tag, args={}):
    form = create_tag_form()

    if request.method == "POST":
        # SAVE UPDATE

        tag.name = form.name.data

        if not errors:
            db.session.commit()

    # POST FORM
    form.name.data = tag.name

    args["form"] = form

    return errors, args


# POST

def edit_post_by_id(errors, post_id, args={}):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        errors.append("Can't find post by id {}".format(post_id))

        return errors, args

    errors, args = edit_post(errors, post)

    return errors, args


def edit_post(errors, post, args={}):
    if not access(author=post.author):
        errors.append("no access")

        return errors, args
    errors, args = edit_post_body(errors, post)

    return errors, args


def edit_post_body(errors, post, args={}):
    form = create_post_form()

    if request.method == 'POST':

        # SAVE UPDATES

        post.title = form.title.data
        post.text = form.text.data
        post.tags = []

        for tag in form.tags.data:
            post.tags.append(Tag.query.filter(Tag.id == tag).first())

        # SAVE IMAGES

        args = {
            "post_id": post.id
        }
        errors = save_image_to_post(errors, form, args)

        # COMMIT
        if not errors:
            db.session.commit()
        else:
            db.session.rollback()
            errors.append("Can't save in db")

    # POST FORM

    form.title.data = post.title
    form.text.data = post.text
    form.tags.data = []

    for tag in post.tags:
        form.tags.data.append(str(tag.id))

    # VIEW IMAGES
    images = Image.query.filter(Image.post_id == post.id).all()

    #  RETURN
    args["form"] = form
    args["images"] = images

    return errors, args


# COMMENT

def edit_comment_by_id(errors, comment_id, args={}):
    comment = Comment.query.filter(Comment.id == comment_id).first()

    if not comment:
        errors.append("Can't find by id {}".format(comment_id))
        return errors, args

    errors, args = edit_comment(errors, comment)

    return errors, args


def edit_comment(errors, comment, args={}):
    if not access(author=comment.author):
        errors.append("no access")
        return errors, args

    errors, args = edit_comment_body(errors, comment)

    return errors, args


def edit_comment_body(errors, comment, args={}):
    form = create_comment_form()

    if request.method == "POST":
        # SAVE UPDATE

        comment.title = form.title.data
        comment.text = form.text.data

        if not errors:
            db.session.commit()

    # POST FORM
    form.title.data = comment.title
    form.text.data = comment.text

    args["form"] = form

    return errors, args
