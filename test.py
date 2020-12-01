from unittest import TestCase
from app import app
from models import db, User, Post, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests views for Users"""
    def setUp(self):
        '''Add Test user '''
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()
        user = User(first_name="TestFirst", last_name="testLast",image_url='/static/no-profile-photo-150.png')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        self.user = user

        tag = Tag(name="test-only")
        db.session.add(tag)
        db.session.commit()
        self.tag =tag
        self.tag_id =tag.id
        
        post = Post(title='This is a new title', content='CONTENTCONTENT CONTENT',user=self.user)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id
        self.post=post

    def tearDown(self):
        '''Clean up test db or any bad transaction '''
        db.session.rollback()
    
    def test_index(self):
        ''' Tests the index route'''
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Recent Posts</h1>', html)
    
    def test_users(self):
        ''' Tests the /users route'''
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<a href="/users/new" class="btn btn-success">Add a User</a>', html)

    def test_add_user_form(self):
        '''Tests the /users/new GET request '''
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<form action="/add-user" method="POST">', html)
    
    def test_add_user_post(self):
        '''Test adding a user POST request'''
        with app.test_client() as client:
            add_new = {'first':'NewUser', 'last':'testNewLast','img-url':'/static/no-profile-photo-150.png'}
            res = client.post('/add-user', data=add_new,follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('NewUser testNewLast', html)

    def test_show_user(self):
        ''' Test view of user page'''
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('TestFirst testLast', html)

    # test /users/user_id/posts/new GET
    def test_new_post(self):
        ''' Test view of new post page'''
        with app.test_client() as client:
            res = client.get(f'users/{self.user_id}/posts/new')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Add post for', html)

    # test /users/user_id/posts/new POST
    def test_new_post_postrequest(self):
        '''Test POST request for a new post '''
        with app.test_client() as client:
            add_new_post = {'title':'secondpost','content':'2content','user_id':self.user_id}
            res = client.post(f'/users/{self.user_id}/posts/new', data=add_new_post,follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('secondpost</a>',html)
    
    # test /posts/post_id
    def test_post_view(self):
        '''Test Get request for a given post'''
        with app.test_client() as client:
            res = client.get(f'posts/{self.post_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h2>This is a new title</h2>',html)
            self.assertIn('<p>CONTENTCONTENT CONTENT</p>',html)

    # test /posts/post_id/edit GET 
    def test_post_edit_view(self):
        '''Test a GET request for a given EDIT POST page'''
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}/edit')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h2>Edit a post</h2>',html)
            self.assertIn(f'<p>Title:     <input required placeholder="{self.post.title}" name="title"></p>',html)

    # test /posts/post_id/edit POST
    def test_edit_post(self):
        with app.test_client() as client:
            add_new_post = {'title':'post edit','content':'editing the post!','user_id':self.user_id}
            res = client.post(f'/posts/{self.post_id}/edit',data=add_new_post,follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<h2>post edit</h2>',html)
            self.assertIn('<p>editing the post!</p>',html)


    # test /posts/post_id/delete POST
    def test_post_delete(self):
        with app.test_client() as client:
            post = Post(title='delete test', content='content-delete-test',user=self.user)
            db.session.add(post)
            db.session.commit()
            res = client.post(f'/posts/{post.id}/delete')
            self.assertEqual(res.status_code,302)
    

    # test /tags GET
    def test_tags(self):
        with app.test_client() as client:
            res = client.get('/tags')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<a class="btn btn-success" href="/tags/new">Add Tags</a>',html)

    # GET /tags/[tag-id]
    def test_tagid(self):
        with app.test_client() as client:
            res = client.get(f'/tags/{self.tag_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>test-only</h1>',html)

    # GET /tags/new
    def test_tags_new(self):
        with app.test_client() as client:
            res = client.get('/tags/new')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<form action="/tags/new" method="POST">',html)

    # POST /tags/new
    def test_tags_new_post(self):
        with app.test_client() as client:
            new_tag = {'name':'newTag'}
            res = client.post('/tags/new', data=new_tag,follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('newTag',html)

    # GET /tags/[tag-id]/edit
    def test_edit_tag_view(self):
        with app.test_client() as client:
            res = client.get(f'/tags/{self.tag_id}/edit')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>test-only</h1>',html)
            self.assertIn(f'<form action="/tags/{self.tag_id}/edit" method="POST">',html)
        
    # POST /tags/[tag-id]/edit
    def test_edit_tag_post(self):
        with app.test_client() as client:
            edit_tag = {'name':'editTag'}
            res = client.post(f'/tags/{self.tag_id}/edit',data=edit_tag,follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('editTag',html)
            

    # POST /tags/[tag-id]/delete
    def test_tag_delete(self):
        with app.test_client() as client:
            del_tag = Tag(name="delete_test")
            db.session.add(del_tag)
            db.session.commit()
            res = client.post(f'/tags/{del_tag.id}/delete')
            self.assertEqual(res.status_code,302)