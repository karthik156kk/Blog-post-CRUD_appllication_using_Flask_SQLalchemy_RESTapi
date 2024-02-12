import pytest
from karthik_blog_website import app, db, bcrypt, login_manager
from karthik_blog_website.models import User, Post
from karthik_blog_website.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import current_user
@pytest.mark.parametrize('endpoint', [('/'), ('/home'), ('/about'), ('/register'), ('/login')])
def test_general_page(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200

@pytest.mark.parametrize('endpoint', [('/post/1/delete'), ('/post/1/update'), ('/post/new'), ('/account'), ('/logout')])
def test_special_page(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 302

@pytest.mark.parametrize('endpoint, output_status', [('/post/1/delete', 404), ('/post/1/update', 404), ('/post/new', 200), ('/account', 200), ('/logout', 302)])
def test_special_page(client, endpoint, output_status):
    with app.app_context():
        # Create a test user
        hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
        user = User(username='test_user', email='test@example.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # Log in the test user
        client.post('/login', data={'email': 'test@example.com', 'password': 'password123'}, follow_redirects=True)
        # Access the special page
        response = client.get(endpoint)
        assert response.status_code == output_status
