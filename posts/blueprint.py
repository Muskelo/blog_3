from flask import Blueprint, render_template, request, abort,redirect
from flask_security import current_user

from models import Post, Image, Comment
from utils import access
from .create import create_comment
from .edit import edit_comment_by_id
from .forms import create_comment_form

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

    # EDIT COMMENT
    edit = request.args.get("edit")
    print(request.data)
    if edit:
        errors, args = edit_comment_by_id(errors, edit)

        if errors:
            return render_template("wrong.html", errors=errors,
                                   request=request, access=access)
        form = args["form"]



    # CREATE COMMENT
    else:

        form = create_comment_form()

        args = {
            "post_id": post.id,
            "author_id": current_user.id
        }

        # add comment

        if request.method == "POST":
            errors = create_comment(errors, form, args)
            if not errors:
                return redirect(request.url)

    # PRINT ERRORS
    if errors:
        return render_template("wrong.html",
                               errors=errors,
                               request=request,
                               access=access)

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
