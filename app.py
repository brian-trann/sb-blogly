"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
# ~~~~~~ User related routes
@app.route('/')
def index_page():
    ''' show index'''
    posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template('index.html',posts=posts)

@app.route('/users')
def users_page():
    users = User.query.all()
    return render_template('/users/users.html',users=users)

@app.route('/users/new')
def add_user_route():
    ''' Render add user page'''
    return render_template('/users/add.html')

@app.route('/add-user', methods=['POST'])
def add_user():
    ''' redirect and add to db'''
    first = request.form['first']
    last = request.form['last']
    image = request.form['img-url'] or None
    
    new_user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/users/user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html',user=user)

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

# ~~~~~~ Below are Post related routes

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def show_post_form(user_id):
    ''' Show form to add post for a user '''
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('/posts/add_post.html',user=user,tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_add_form(user_id):
    ''' Handle add form; add post and redirect to the user detail page'''
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    tags_list = [int(id) for id in request.form.getlist('tags')] # gets the tags.id
    tags = Tag.query.filter(Tag.id.in_(tags_list)).all() # turns the tag id's into tag objcts
    
    new_post = Post(title=title, content=content, user=user,tags=tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    ''' show a post. Show buttons to edit and delete the post'''
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/post.html',post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    '''Shows fom to edit a post, and to cancel (back to user page) This is a get request '''
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/posts/edit_post.html', post=post,tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_post(post_id):
    ''' Edits a post, given the post id. Makes a POST request '''
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']
    tags_list = [int(id) for id in request.form.getlist('tags')]
    post.tags=Tag.query.filter(Tag.id.in_(tags_list)).all()
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    ''' Delete the post'''
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('/errors/404.html'), 404

# ~~~~~~ Below are Tag related routes
@app.route('/tags')
def show_tags():
    '''Lists all tags, with links to the tag detail page.'''
    tags = Tag.query.all()
    return render_template('/tags/tags.html',tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    '''Show detail about a tag. Have links to edit form and to delete.'''
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/show_tag.html',tag=tag)

@app.route('/tags/new')
def add_tag():
    '''Shows a form to add a new tag.'''
    return render_template('/tags/add_tag.html')

@app.route('/tags/new', methods=['POST'])
def add_tag_post():
    '''Process add form, adds tag, and redirect to tag list.'''
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    '''Show edit form for a tag.'''
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/edit_tag.html',tag=tag)
    
@app.route('/tags/<int:tag_id>/edit',methods=['POST'])
def edit_tag_post(tag_id):
    '''Process edit form, edit tag, and redirects to the tags list.'''
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name']
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''Delete a tag.'''
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
