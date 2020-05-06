from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user
from flask_security import login_required

from db import db
from models import Tag, Post, Image, Comment
from posts.forms import CreatePostForm, CreateTagForm, CreateCommentForm, SelectMultipleField
from posts.utils import save_image, delete_image

posts = Blueprint('posts', __name__,
                  template_folder='templates',
                  static_folder='static'
                  )


@posts.route('create_post/', methods=['GET', 'POST'])
@login_required
def create_posts():
    errors = []

    # CREATE FORM

    # to auto-refresh after adding new teg
    CreatePostForm.tagsChoice = [(str(tag.id), tag.name) for tag in Tag.query.all()]
    CreatePostForm.tags = SelectMultipleField(u"Tags", choices=CreatePostForm.tagsChoice)

    form = CreatePostForm()

    if request.method == "POST":

        # VALIDATOR

        a = Post.query.filter(Post.title == form.title.data).first()
        if a is not None:
            errors.append("Post with that title already added")

        # CREATE NEW POST

        new_post = Post()
        new_post.title = form.title.data
        new_post.text = form.text.data
        new_post.author = current_user

        for tag in form.tags.data:
            new_post.tags.append(Tag.query.filter(Tag.id == tag).first())

        if not errors:
            # FLASH(to get post's id)

            db.session.add(new_post)
            db.session.flush()

            # SAVE IMAGES

            errors = save_image(form, new_post, errors)

        # COMMIT

        if not errors:
            db.session.commit()
            return redirect(url_for("posts.create_posts"))
        else:
            db.session.rollback()

    return render_template("posts/create_post.html",
                           form=form,
                           current_user=current_user,
                           errors=errors
                           )


@posts.route('create_tag/', methods=['GET', 'POST'])
@login_required
def create_tag():
    errors = []

    # CREATE FORM

    form = CreateTagForm()

    if request.method == "POST":
        # CREATE NEW TAG
        new_tag = Tag()
        new_tag.name = form.name.data

        # VALIDATOR

        if Tag.query.filter(Tag.name == new_tag.name).first():
            errors.append("this tag already added")

        # COMMIT

        if not errors:
            db.session.add(new_tag)
            db.session.commit()

            return redirect(url_for("posts.create_tag"))

    return render_template("posts/create_tag.html",
                           form=form,
                           current_user=current_user,
                           errors=errors
                           )


@posts.route('edit_post/<post_id>/', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    errors = []

    # search post
    post = Post.query.filter(Post.id == post_id).first()

    # search result and access
    if post and (post.author == current_user or current_user.has_role("admin")):

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
    if tag and current_user.has_role("moder"):
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


@posts.route('delete_image/<image_id>/', methods=['POST'])
@login_required
def delete_img(image_id):
    errors = []

    # search
    errors, post_id = delete_image(image_id, current_user, errors)

    if not errors:
        return redirect(url_for("posts.edit_post", post_id=post_id))

    return render_template("wrong.html", request=request)


@posts.route('delete_post/<post_id>/', methods=['POST'])
@login_required
def delete_post(post_id):
    errors = []

    #  search
    post = Post.query.filter(Post.id == post_id).first()

    #  access
    if post and (current_user == post.author or
                 current_user.has_role("moder")):

        for image in post.images:
            delete_image(image.id, current_user, errors)

        #  commit
        db.session.delete(post)
        db.session.commit()

        return redirect(request.referrer)

    return render_template("wrong.html", request=request)


@posts.route('delete_tag/<tag_id>/', methods=['POST'])
@login_required
def delete_tag(tag_id):
    errors = []

    #  search
    tag = Tag.query.filter(Tag.id == tag_id).first()

    # access
    if tag and (current_user.has_role("moder")):

        # COMMIT

        if not errors:
            db.session.delete(tag)
            db.session.commit()

            return "tag deleted"

    return "something went wrong"


@posts.route('/<post_id>/', methods=["GET", "POST"])
def read_post(post_id):
    errors = []
    # search post
    post = Post.query.filter(Post.id == int(post_id)).first()

    if not post:
        abort(404)

    # create form
    form = CreateCommentForm()

    if request.method == "POST":
        # ADD COMMENT

        comment = Comment()
        comment.title = form.title.data
        comment.text = form.text.data
        comment.author = current_user
        comment.post_parent = post

        if not errors:
            db.session.add(comment)
            db.session.commit()
            # to refresh flask form
            return redirect(url_for("posts.read_post", post_id=post_id))

    # get comments
    comments = (Comment.query
                .filter(Comment.post_id == post_id)
                .order_by(Comment.created.desc())
                )

    # get images
    images = Image.query.filter(Image.post_id == post_id).all()

    return render_template("posts/post.html",
                           errors=errors,
                           post=post,
                           form=form,
                           current_user=current_user,
                           images=images,
                           comments=comments
                           )
