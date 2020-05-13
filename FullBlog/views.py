from flask import request, render_template, redirect, url_for
from flask_security import login_required

from app import app
from auth.create import create_role
from auth.delete import delete_role_by_id, delete_user_by_id
from auth.edit import edit_role_by_id
from auth.forms import create_role_form
from auth.get_list import get_user_list, get_role_list
from posts.create import create_post, create_tag
from posts.delete import delete_comment_by_id, \
    delete_image_by_id, \
    delete_post_by_id, \
    delete_tag_by_id
from posts.edit import edit_tag_by_id, edit_post_by_id
from posts.forms import create_post_form, create_tag_form
from posts.get_list import get_post_list, get_tag_list
from utils import get_num_near_pages, access


@app.route('/')
def index():
    return render_template("index.html", access=access)


#  LIST


items_list = {
    "post": {
        "items_name": "Posts",
        "template": "posts/post_in_list.html",
        "get_list": get_post_list
    },
    "tag": {
        "items_name": "Tags",
        "template": "posts/tag_in_list.html",
        "get_list": get_tag_list
    },
    "user": {
        "items_name": "Posts",
        "template": "auth/user_in_list.html",
        "get_list": get_user_list
    },
    "role": {
        "items_name": "Roles",
        "template": "auth/role_in_list.html",
        "get_list": get_role_list
    }
}


@app.route('/list/<item>/')
def list_items(item):
    errors = []

    # select template items
    item_template = items_list[item]["template"]

    # num page
    page_number = request.args.get("page")

    page_name = items_list[item]["items_name"]

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


# DELETE

items_delete = {
    "post": {
        'items_name': "Posts",
        'function': delete_post_by_id
    },
    "tag": {
        'items_name': "Tags",
        'function': delete_tag_by_id
    },
    "comment": {
        "items_name": 'Comments',
        'function': delete_comment_by_id
    },
    "image": {
        "items_name": 'Images',
        'function': delete_image_by_id
    },
    "role": {
        "items_name": 'Roles',
        'function': delete_role_by_id
    },
    "user": {
        "items_name": 'Users',
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
        return render_template("wrong.html", request=request,
                               errors=errors, access=access)

    return redirect(request.referrer)


# CREATE

items_create = {
    "post": {
        "item_name": "Posts",
        "function": create_post,
        "get_form": create_post_form,
        "template": "/posts/create_post.html"
    },
    "tag": {
        "item_name": "Tags",
        "function": create_tag,
        "get_form": create_tag_form,
        "template": "/posts/create_tag.html"
    },
    "role": {
        "item_name": "Roles",
        "function": create_role,
        "get_form": create_role_form,
        "template": "/auth/create_role.html"
    }
}


@app.route('/create/<item_type>/', methods=['GET', 'POST'])
@login_required
def create_item(item_type):
    errors = []

    form = items_create[item_type]["get_form"]()

    if request.method == "POST":
        errors = items_create[item_type]["function"](errors, form)

        if not errors:
            return redirect(url_for("create_item", item_type=item_type))

    return render_template(items_create[item_type]["template"],
                           form=form,
                           access=access,
                           errors=errors)


# EDIT

items_edit = {
    "tag": {
        "item_name": "Tags",
        "function": edit_tag_by_id,
        "template": "/posts/edit_tag.html"
    },
    "post": {
        "item_name": "Posts",
        "function": edit_post_by_id,
        "template": "/posts/edit_post.html"
    },
    "role": {
        "item_name": "Posts",
        "function": edit_role_by_id,
        "template": "/auth/edit_role.html"
    }
}


@app.route('/edit_item/<item_type>/<item_id>/', methods=["GET", "POST"])
@login_required
def edit_item(item_type, item_id):
    errors = []

    errors, args = items_edit[item_type]["function"](errors, item_id)

    if errors:
        return render_template("wrong.html", errors=errors,
                               request=request, access=access)

    return render_template(items_edit[item_type]["template"],
                           args=args,
                           access=access,
                           errors=errors,
                           item_id=item_id
                           )
