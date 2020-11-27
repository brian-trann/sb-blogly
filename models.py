"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
default_image = '/static/no-profile-photo-150.png'


def connect_db(app):
    '''Connect to database '''
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String(120), nullable=False, default=default_image)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        '''Return full name'''
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):

    """Post. FK is user_id """
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

