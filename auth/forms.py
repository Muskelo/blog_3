from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, FileField
from wtforms import StringField

from models import Role


class SelectRoleForm(FlaskForm):
    rolesChoice = [(str(role.id), role.name) for role in Role.query.all()]
    roles = SelectMultipleField(u"roles", choices=rolesChoice)


class CreateRoleForm(FlaskForm):
    name = StringField(u"Name")
    description = StringField(u"description")


def create_role_form():
    form = CreateRoleForm()

    return form


class UploadIconForm(FlaskForm):
    icon = FileField(u"Icon")


def upload_icon_form():
    form = UploadIconForm()

    return form
