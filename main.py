import db  # noqa: F401
import mail  # noqa: F401
import posts.forms  # noqa: F401
import security  # noqa: F401
import views  # noqa: F401
from app import app
from auth.blueprint import auth
from models import Role, User  # noqa: F401
from posts.blueprint import posts

app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run()
