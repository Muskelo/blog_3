from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, MultipleFileField, validators


class CreatePostForm(FlaskForm):
    title = StringField(u"Title", validators=[validators.length(min=4)])
    text = TextAreaField(u"Text")
    tagsChoice = None
    tags = SelectMultipleField(u"tags")
    images = MultipleFileField(u"Images", render_kw={'multiple': True})


class CreateTagForm(FlaskForm):
    name = StringField(u"Name")


class CreateCommentForm(FlaskForm):
    title = StringField(u"Title", validators=[validators.length(min=4)])
    text = TextAreaField(u"Text")
