from flask import request, url_for
from flask_security import current_user


def get_num_near_pages(page, all_pages, max_way_to_neighbor):
    """Return nums of last pages

    :param page:
    :param all_pages:
    :param max_way_to_neighbor:
    :return: [min_page,max_page]
    """

    if page > max_way_to_neighbor:
        min_page = page - max_way_to_neighbor
    else:
        min_page = 1

    if (page + max_way_to_neighbor) <= all_pages:
        max_page = page + max_way_to_neighbor
    else:
        max_page = all_pages

    neighbor = [min_page, max_page + 1]

    return neighbor


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def access(roles: list = [], author=None, auth=False):
    """Access

    :param roles:
    :param auth: true if user is authenticated
    :param author: if need check author
    :return:true if one among there true
    """

    if auth and current_user.is_authenticated:
        return True

    if author and author == current_user:
        return True

    for role in roles:
        if current_user.has_role(role):
            return True

    return False


def access_bigger(user1, user2):
    list_roles_access = ["God", "admin", "moder"]

    for role in list_roles_access:
        if user1.has_role(role) and user2.has_role(role):
            return False
        if user1.has_role(role) and not user2.has_role(role):
            return True

    return False
