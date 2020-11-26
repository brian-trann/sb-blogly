"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()
@app.route('/')
def index_page():
    ''' show index'''
    return redirect('/users')

@app.route('/users')
def users_page():
    users = User.query.all()
    return render_template('index.html',users=users)

@app.route('/users/new')
def add_user_route():
    ''' Render add user page'''
    return render_template('add.html')

@app.route('/add-user', methods=['POST'])
def add_user():
    ''' redirect and add to db'''
    first = request.form['first']
    last = request.form['last']
    image = request.form['img-url'] or None
    
    new_user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
  
    return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
        
    user = User.query.get_or_404(user_id)
    first = request.form['first']
    last = request.form['last']
    image = request.form['img-url'] or None
    user.first_name=first
    user.last_name=last
    if image == None:
        image = '/static/no-profile-photo-150.png'
    user.image_url=image

    db.session.add(user)
    db.session.commit()
    return redirect('/')  


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/')

