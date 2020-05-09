from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user
from flask_security import login_required

from db import db
from models import Tag, Post, Image, Comment
from posts.forms import CreatePostForm, CreateTagForm, CreateCommentForm, SelectMultipleField
from posts.utils import save_image
from utils import access

posts = Blueprint('posts', __name__,
                  template_folder='templates',
                  static_folder='static'
                  )


@posts.route('edit_post/<post_id>/', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    errors = []

    # search post
    post = Post.query.filter(Post.id == post_id).first()

    # search result and access
    if post and access(["moder"], author=post.author):

        # CREATE FORM

        # to auto-refresh after adding new tag
        CreatePostForm.tagsChoice = [(str(tag.id), tag.name) for tag in Tag.query.all()]
        CreatePostForm.tags = SelectMultipleField(u"Tags", choices=CreatePostForm.tagsChoice)

        form = CreatePostForm()

        if request.method == 'POST':

            # SAVE UPDATES

            post.title = form.title.data
            post.text = form.text.data
            post.tags = []

            for tag in form.tags.data:
                post.tags.append(Tag.query.filter(Tag.id == tag).first())

            # SAVE IMAGES

            errors = save_image(form, post, errors)

            # COMMIT
            if not errors:
                db.session.commit()
            else:
                db.session.rollback()
                errors.append("Something went wrong")

        # POST FORM

        form.title.data = post.title
        form.text.data = post.text
        form.tags.data = []

        for tag in post.tags:
            form.tags.data.append(str(tag.id))

        # view images
        images = Image.query.filter(Image.post_id == post_id).all()

    else:
        return "can't find or no access"

    return render_template("posts/edit_post.html",
                           form=form,
                           post_id=post_id,
                           images=images,
                           current_user=current_user,
                           errors=errors
                           )


@posts.route('edit_tag/<tag_id>/', methods=['GET', 'POST'])
@login_required
def edit_tag(tag_id):
    errors = []

    # search post
    tag = Tag.query.filter(Tag.id == tag_id).first()

    # search result and access
    if tag and access(roles=["moder"]):
        # CREATE FORM

        form = CreateTagForm()

        if request.method == "POST":
            # SAVE UPDATE

            tag.name = form.name.data

            if not errors:
                db.session.commit()

        # POST FORM
        form.name.data = tag.name

    else:
        return "can't find or no access"

    return render_template("posts/edit_tag.html",
                           form=form,
                           tag_id=tag_id,
                           current_user=current_user,
                           errors=errors
                           )


@posts.route('/<post_id>/', methods=["GET", "POST"])
def read_post(post_id):
    errors = []

    # search post
    post = Post.query.filter(Post.id == int(post_id)).first()

    if not post:
        abort(404)

    # create form
    form = CreateCommentForm()

    # EDIT COMMENT part 1

    edit = request.args.get("edit")

    if edit:  # edit comment
        comment = Comment.query.filter(Comment.id == edit).first()

        # validator

        if not comment:
            errors.append("Don't find comment for edit")

        elif not (current_user == comment.author
                  or current_user.has_role("moder")):

            errors.append("not access")

    # ADD COMMENT

    if request.method == "POST":

        # create comment
        if not edit:
            comment = Comment()

        comment.title = form.title.data
        comment.text = form.text.data
        comment.author = current_user
        comment.post_parent = post

        if not errors:
            if not edit:  # when edit don't necessary add
                db.session.add(comment)
            db.session.commit()
            return redirect(url_for("posts.read_post", post_id=post_id))

    # EDIT COMMENT part 2
    # I split  it because in ADD COMMENT use object from part 1,
    # but in part 2 edit object from ADD COMMENT
    if edit:
        # create

        if not errors:
            form.title.data = comment.title
            form.text.data = comment.text

    # GET COMMENTS FROM DB

    comments = (Comment.query
                .filter(Comment.post_id == post_id)
                .order_by(Comment.created.desc())
                )

    # GET IMAGES
    images = Image.query.filter(Image.post_id == post_id).all()

    return render_template("posts/post.html",
                           errors=errors,
                           post=post,
                           form=form,
                           access=access,
                           images=images,
                           comments=comments,
                           edit=edit
                           )
