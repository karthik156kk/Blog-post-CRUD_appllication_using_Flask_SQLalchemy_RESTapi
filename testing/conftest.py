import pytest
from flask import url_for, redirect
from karthik_blog_website import app, db, bcrypt, login_manager
from karthik_blog_website.routes import general_routes, account_routes, post_routes
from flask_login import login_user
from karthik_blog_website.models import User, Post

@pytest.fixture
def client():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()
#constants:
REGISTER_VALIDATION_PARAMETERS = [
    ('test_user', 'test@example.com', 'password123', 'password123', True),  # Positive test case
    ('test_user', 'invalid_email', 'password123', 'password123', False),  # Negative test case (invalid email)
    ('test_user', '@gmail.com', 'password123', 'password123', False),  # Negative test case (invalid email)
    ('test_user', 'karthik582tn@gmail..com', 'password123', 'password123', False),  # Negative test case (invalid email ..)
    ('s', 'test@example.com', 'password123', 'password123', False),  # Negative test case (short username)
]

LOGIN_VALIDATION_PARAMETERS = [
    ('test@example.com', 'password123', True),  # Positive test case
    ('test@example.com', 'wrong_password', False),  # Negative test case (incorrect password)
    ('invalid_email', 'password123', False),  # Negative test case (invalid email)
]

UPDATE_VALIDATION_PARAMETERS = [
    #POSITIVE_TEST_CASES
    ('updated_username', 'test@example.com', b'Your account has been updated!', True),
    ('test_user', 'updated_email@example.com', b'Your account has been updated!', True),
    ('updated_username', 'updated_email@example.com', b'Your account has been updated!', True), 
    #NEGATIVE_TEST_CASES
    ('', 'test@example.com', b'This field is required', False), 
    ('updated_username', '', b'This field is required', False),
    ('updated_username', 'invalid_email', b'Invalid email address.', False)
]
#imported functions:
def setup_database_with_test_user_credentials(email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username='test_user', email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

def setup_test_user_for_login(client, email, password):
    setup_database_with_test_user_credentials(email, password)
    form_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    return client.post('/login', data=form_data, follow_redirects=True)

def setup_test_user_for_registration(client):
    form_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
    return client.post('/register', data=form_data, follow_redirects=True)