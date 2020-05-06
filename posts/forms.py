from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, MultipleFileField, validators

from app import app


class CreatePostForm(FlaskForm):
    title = StringField(u"Title", validators=[validators.length(min=4)])
    text = TextAreaField(u"Text")
    tagsChoice = None
    tags = SelectMultipleField(u"tags")
    images = MultipleFileField(u"Images", render_kw={'multiple': True})


class CreateTagForm(FlaskForm):
    name = StringField(u"Name")


