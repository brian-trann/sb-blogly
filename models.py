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

    """Post. A User has many posts. FK is user_id """
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        '''return a parsed date '''
        date = self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
        return date

class PostTag(db.Model):
    '''Post Tag. 
    Many posts have many tags
    post_id (PK,FK)
    tag_id (PK,FK)'''
    __tablename__ = "posts_tags"
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"),primary_key=True)
    tag_id = db.Column(db.Integer,db.ForeignKey("tags.id"),primary_key=True)
    

class Tag(db.Model):
    '''Tag that can be added to many posts
    id (PK)
    name -string'''
    __tablename__ = "tags"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship('Post', secondary='posts_tags',cascade='all,delete',backref='tags')