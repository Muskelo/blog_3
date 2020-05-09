import os

from app import app
from db import db
from models import Image


def allowed_file(filename):
    """Allow file

    :param filename:
    :return True if data format good:
    """
    filename = filename.split(".")
    return (filename[1] in app.config["ALLOWED_EXTENSIONS"]) and (len(filename) == 2)


def save_image(form, post, errors):
    """Save images

    Save image from form and return errors

    :param form:
    :param post:
    :param errors:
    :return: errors
    """

    images = form.images.data  # all images
    i = 1  # image's num

    # get post id
    post_id = post.id

    # saving
    for file in images:
        if file.filename == "":
            continue

        #  save info to db
        image = Image(post_parent=post)
        db.session.add(image)
        db.session.flush()

        if file and allowed_file(file.filename):
            filename = "{}_{}.{}".format(str(image.id), str(post_id),
                                         file.filename.split(".")[1])
            image.address = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image.address)
        else:
            errors.append("img №{} hav e invalid format".format(i))
        i += 1

    return errors
