from flask import request, render_template, redirect
from flask_login import current_user
from flask_security import login_required

from app import app

from auth.delete import delete_role_by_id, delete_user_by_id
from posts.delete import delete_comment_by_id, \
    delete_image_by_id, \
    delete_post_by_id, \
    delete_tag_by_id

from auth.get_list import get_user_list
from posts.get_list import get_post_list, get_tag_list

from utils import get_num_near_pages,access


@app.route('/')
def index():
    return render_template("index.html", current_user=current_user)


items_list = {
    "post": {
        "model_name": "Posts",
        "template": "posts/post_in_list.html",
        "get_list": get_post_list
    },
    "tag": {
        "model_name": "Tags",
        "template": "posts/tag_in_list.html",
        "get_list": get_tag_list
    },
    "user": {
        "model_name": "Posts",
        "template": "auth/user_in_list.html",
        "get_list": get_user_list
    }
}


@app.route('/list/<item>/')
def list_items(item):
    errors = []

    # select template items
    item_template = items_list[item]["template"]

    # num page
    page_number = request.args.get("page")

    page_name = items_list[item]["model_name"]

    # SEARCH

    list__items, log, errors = items_list[item]["get_list"](errors)

    # PAGINATE

    if page_number and page_number.isdigit():
        page_number = int(page_number)
    else:
        page_number = 1

    page = list__items.paginate(page=page_number, per_page=10)
    pages_near = get_num_near_pages(page_number, page.pages, 4)

    return render_template("list.html",
                           access=access,
                           page=page,
                           page_name=page_name,
                           errors=errors,
                           pages_near=pages_near,
                           log=log,
                           item_template=item_template
                           )


items_delete = {
    "post": {
        'model_name': "Posts",
        'function': delete_post_by_id
    },
    "tag": {
        'model_name': "Tags",
        'function': delete_tag_by_id
    },
    "comment": {
        "model_name": 'Comments',
        'function': delete_comment_by_id
    },
    "image": {
        "model_name": 'Images',
        'function': delete_image_by_id
    },
    "role": {
        "model_name": 'Roles',
        'function': delete_role_by_id
    },
    "user": {
        "model_name": 'Users',
        'function': delete_user_by_id
    }
}


@app.route('/delete/<item_type>/<item_id>/', methods=["POST"])
@login_required
def delete_item(item_type, item_id):
    errors = []

    # DELETE

    errors = items_delete[item_type]["function"](errors, item_id)

    if errors:
        return render_template("wrong.html", request=request, errors=errors)

    return redirect(request.referrer)
