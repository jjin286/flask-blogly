"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DEFAULT_IMAGE_URL = 'https://cdn.britannica.com/66/183466-050-78C1C9CB/spider-monkey-Venezuela-South-America.jpg'

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for Users"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default = DEFAULT_IMAGE_URL
    )


class Post(db.Model):
    """Model for Post"""

    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    user = db.relationship('User', backref='posts')
    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")


class Tag(db.Model):
    """Model for tags on posts"""

    __tablename__ = 'tags'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

class PostTag(db.Model):
    """Through table for relating posts and tags"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True
    )

    # post = db.relationship('Post', backref='posts_tags')
