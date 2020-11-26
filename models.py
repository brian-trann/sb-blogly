"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

    @property
    def full_name(self):
        '''Return full name'''
        return f'{self.first_name} {self.last_name}'