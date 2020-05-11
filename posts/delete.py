import os

from db import db
from models import Comment, Image, Post, Tag, Icon, User
from utils import access


# COMMENT

def delete_comment_by_id(errors, comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()

    if not comment:
        errors.append("Don't find comment by id{}".format(comment_id))
        return errors

    errors = delete_comment(errors, comment)

    return errors


def delete_comment(errors, comment):
    if not access(["moder"], comment.author):
        errors.append("no access")
        return errors

    errors = delete_comment_body(errors, comment)

    return errors


def delete_comments_after_post(errors, post):
    """

    :param errors:
    :param post:
    :return:
    """
    if not access(["moder"], post.author):
        errors.append("no access")
        return errors

    for comment in post.comments:
        errors = delete_comment_body(errors, comment)

    return errors


def delete_comment_body(errors, comment):
    """Delete comment

    :param comment:
    :param errors:
    :return:
    """

    try:
        db.session.delete(comment)
        db.session.commit()
    except:
        errors.append("can't delete comment from db,id{}".format(comment.id))

    return errors


# IMAGE

def delete_image_by_id(errors, image_id):
    image = Image.query.filter(Image.id == image_id).first()

    if not image:
        errors.append("Don't find image by id{}".format(image_id))
        return errors

    errors = delete_image(errors, image)

    return errors


def delete_image(errors, image):
    if not access(["moder"], image.post_parent.author):
        errors.append("no access")
        return errors

    errors = delete_image_body(errors, image)

    return errors


def delete_image_after_post(errors, post):
    if not access(["moder"], post.author):
        errors.append("no access")
        return errors

    for image in post.images:
        errors = delete_image_body(errors, image)

    return errors


def delete_image_body(errors, image):
    # delete
    try:
        os.remove(image.address)
    except:
        errors.append("can't remove from disk,image id={}".format(image.id))

        return errors

    # commit
    try:
        db.session.delete(image)
        db.session.commit()
    except:
        errors.append("can't remove from db,image id={}".format(image.id))

    return errors


# POST

def delete_post_by_id(errors, post_id):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        errors.append("Don't find post by id{}".format(post_id))
        return errors

    errors = delete_post_body(errors, post)

    return errors


def delete_post(errors, post):
    if not access(["moder"]):
        errors.append("no access")
        return errors

    errors = delete_post_body(errors, post)

    return errors


def delete_post_body(errors, post):
    errors = delete_comments_after_post(errors, post)
    errors = delete_image_after_post(errors, post)

    try:
        db.session.delete(post)
        db.session.commit()
    except:
        errors.append("can't delete post from db,id{}".format(post.id))

    return errors


# TAG

def delete_tag_by_id(errors, tag_id):
    tag = Tag.query.filter(Tag.id == tag_id).first()

    if not tag:
        errors.append("Don't find tag by id{}".format(tag_id))
        return errors

    errors = delete_tag(errors, tag)

    return errors


def delete_tag(errors, tag):
    if not access(["moder"]):
        errors.append("no access")
        return errors

    errors = delete_tag_body(errors, tag)

    return errors


def delete_tag_body(errors, tag):
    try:
        db.session.delete(tag)
        db.session.commit()
    except:
        errors.append("can't delete tag from db,id{}".format(tag.id))

    return errors



