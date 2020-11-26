from unittest import TestCase
from app import app
from models import db, User

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
        User.query.delete()
        user = User(first_name="TestFirst", last_name="testLast",image_url='/static/no-profile-photo-150.png')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
    
    def tearDown(self):
        '''Clean up test db or any bad transaction '''
        db.session.rollback()
    
    def test_index(self):
        ''' Tests the index route'''
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code,302)
            self.assertEqual(res.location, 'http://localhost/users')
    
    def test_users(self):
        ''' Tests the /users route'''
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<form action="/users/new">', html)

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

    