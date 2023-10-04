"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.britannica.com%2Fanimal%2Fspider-monkey&psig=AOvVaw04gVIUjTS33w119ZRWqQTg&ust=1696544103994000&source=images&cd=vfe&opi=89978449&ved=0CBAQjRxqFwoTCPit37a13YEDFQAAAAAdAAAAABAE'

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
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )
    # TODO: Use the default image
    image_url = db.Column(
        db.Text,
        nullable=True
    )


