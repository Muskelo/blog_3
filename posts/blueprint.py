from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user

from db import db
from models import Post, Image, Comment
from posts.forms import CreateCommentForm
from utils import access
from .edit import edit_comment_by_id

posts = Blueprint('posts', __name__,
                  template_folder='templates',
                  static_folder='static'
                  )


@posts.route('/<post_id>/', methods=["GET", "POST"])
def read_post(post_id):
    errors = []

    # search post
    post = Post.query.filter(Post.id == int(post_id)).first()

    if not post:
        abort(404)

    # create form


    # EDIT COMMENT part 1

    edit = request.args.get("edit")

    if edit:  # edit comment
        errors, args = edit_comment_by_id(errors, edit)
        if errors:
            return render_template("wrong.html",
                                   errors=errors,
                                   request=request,
                                   access=access)
        form = args["form"]
    else:
        form = CreateCommentForm()
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
