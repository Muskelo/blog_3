from db import db
from models import Role
from utils import access


def create_role(errors, form):
    if not access(["God"]):
        errors.append("no access")

        return errors

    # SEARCH SUCH ROLE
    name_in_db = Role.query.filter(Role.name == form.name.data).first()

    if name_in_db:
        errors.append("Role with that name already added")

        return errors

    errors = create_role_body(errors, form)

    return errors


def create_role_body(errors, form):
    role = Role()
    role.name = form.name.data
    role.description = form.description.data

    try:
        db.session.add(role)
        db.session.commit()
    except:
        errors.append("Can't save in db role id{}".format(role.id))

    return errors
