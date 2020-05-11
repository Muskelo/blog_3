class Configuration(object):
    DEBUG = True

    # SqlAlchemy
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://admin:081195@localhost/test_2"
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Flask-security
    SECRET_KEY = "QPODVJLXCJN;DFLDFH;LFDHA'OSDFLH;DLGSD"
    SECURITY_PASSWORD_SALT = "secret"
    SECURITY_PASSWORD_HASH = "sha512_crypt"
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True


    # Upload images
    UPLOAD_FOLDER = 'posts/static/posts/img'
    UPLOAD_FOLDER_AUTH = 'auth/static/auth/img'
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # Flask-mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'arsenstesttest@gmail.com'
    MAIL_PASSWORD = 'ABCabc12345678'
    MAIL_DEFAULT_SENDER = 'arsenstesttest@gmail.com'
    SECURITY_EMAIL_SENDER = "arsenstesttest@gmail.com"
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True

