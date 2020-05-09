from flask_security import current_user

from db import db
from models import Post, Tag
from posts.utils import save_image
from utils import access


# POST

def create_post(errors, form):
    if not current_user.is_authenticated():
        errors.append("no access")

        return errors

    name_in_db = Post.query.filter(Post.title == form.title.data).first()
    if name_in_db:
        errors.append("Post with that title already added")

        return errors

    errors = create_post_body(errors, form)

    return errors


def create_post_body(errors, form):
    new_post = Post()
    new_post.title = form.title.data
    new_post.text = form.text.data
    new_post.author = current_user

    for tag in form.tags.data:
        new_post.tags.append(Tag.query.filter(Tag.id == tag).first())

    # FLUSH(to get post's id)

    try:
        db.session.add(new_post)
        db.session.flush()
    except:
        errors.append("Can't flush post id{}".format(new_post.id))

        return errors

    # SAVE IMAGES

    errors = save_image(form, new_post, errors)

    if errors:
        return errors

    # COMMIT

    try:
        db.session.commit()
    except:
        errors.append("Can't save in db post id{}".format(new_post.id))
        db.session.rollback()

    return errors


# TAG

def create_tag(errors, form):
    if not access(["moder"]):
        errors.append("no access")

        return errors

    # SEARCH SUCH TAG
    name_in_db = Tag.query.filter(Tag.name == form.name.data).first()

    if name_in_db:
        errors.append("Tag with that name already added")

        return errors

    errors = create_tag_body(errors, form)

    return errors


def create_tag_body(errors, form):
    tag = Tag()
    tag.name = form.name.data

    try:
        db.session.add(tag)
        db.session.commit()
    except:
        errors.append("Can't save in db tag id{}".format(tag.id))

    return errors
