from flask import request, render_template
from flask_login import current_user

from app import app
from get_list import get_post_list, get_tag_list,get_user_list
from models import Post, Tag,User
from utils import get_num_near_pages,redirect_url


@app.route('/')
def index():
    return render_template("index.html", current_user=current_user)


items = {
    "post": [Post, "post_in_list.html", get_post_list, "Posts"],
    "tag": [Tag, "tag_in_list.html", get_tag_list, "Tags"],
    "user": [User, "user_in_list.html", get_user_list, "Tags"]
}


@app.route('/list/<item>/')
def list_items(item):
    errors = []

    # select template items
    item_template = items[item][1]

    # num page
    page_number = request.args.get("page")

    page_name = items[item][3]

    # SEARCH

    list__items, log, errors = items[item][2](errors)

    # PAGINATE

    if page_number and page_number.isdigit():
        page_number = int(page_number)
    else:
        page_number = 1

    page = list__items.paginate(page=page_number, per_page=10)
    pages_near = get_num_near_pages(page_number, page.pages, 4)

    return render_template("list.html",
                           current_user=current_user,
                           page=page,
                           page_name=page_name,
                           errors=errors,
                           pages_near=pages_near,
                           log=log,
                           item_template=item_template
                           )


