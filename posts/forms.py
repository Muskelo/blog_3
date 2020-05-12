from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, MultipleFileField, validators

from models import Tag


# POST

class CreatePostForm(FlaskForm):
    title = StringField(u"Title", validators=[validators.length(min=4)])
    text = TextAreaField(u"Text")
    tagsChoice = None
    tags = SelectMultipleField(u"tags")
    images = MultipleFileField(u"Images", render_kw={'multiple': True})


def create_post_form():
    # to auto-refresh after adding new teg
    CreatePostForm.tagsChoice = [(str(tag.id), tag.name) for tag in Tag.query.all()]
    CreatePostForm.tags = SelectMultipleField(u"Tags", choices=CreatePostForm.tagsChoice)

    form = CreatePostForm()

    return form


# TAG

class CreateTagForm(FlaskForm):
    name = StringField(u"Name")


def create_tag_form():
    form = CreateTagForm()

    return form


# COMMENT

class CreateCommentForm(FlaskForm):
    title = StringField(u"Title", validators=[validators.length(min=4)])
    text = TextAreaField(u"Text")


def create_comment_form():
    form = CreateCommentForm()

    return form
