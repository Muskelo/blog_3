from datetime import datetime

from flask_security import RoleMixin, UserMixin

from db import db

# for posts
post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey("post.id")),
                    db.Column('teg_id', db.Integer, db.ForeignKey("tag.id"))
                    )


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship("Tag", secondary=post_tag, backref=db.backref('Post', lazy="dynamic"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship("Comment", backref="post_parent")
    images = db.relationship("Image", backref="post_parent")

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.title


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(140))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.name


class Image(db.Model):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(140))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.id + "_" + self.post_id


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


#  Flask-security
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    posts = db.relationship("Post", backref="author")
    comments = db.relationship("Comment", backref="author")
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
