from flask_wtf import FlaskForm
from wtforms import SelectMultipleField

from models import Role


class SelectRoleForm(FlaskForm):
    rolesChoice = [(str(role.id), role.name) for role in Role.query.all()]
    roles = SelectMultipleField(u"roles", choices=rolesChoice)
