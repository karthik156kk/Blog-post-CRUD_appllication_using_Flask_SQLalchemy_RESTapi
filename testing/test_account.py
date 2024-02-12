import pytest
from testing.conftest import setup_test_user_for_login, setup_test_user_for_registration, setup_database_with_test_user_credentials
from testing.conftest import REGISTER_VALIDATION_PARAMETERS, LOGIN_VALIDATION_PARAMETERS, UPDATE_VALIDATION_PARAMETERS
from karthik_blog_website import app, db, bcrypt, login_manager
from karthik_blog_website.models import User
from karthik_blog_website.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
#form validation check:
@pytest.mark.parametrize('username, email, password, confirm_password, expected_result', REGISTER_VALIDATION_PARAMETERS)
def test_valid_registration(client, username, email, password, confirm_password, expected_result):
    with app.app_context():  
        form = RegistrationForm(username=username, email=email, password=password, confirm_password=confirm_password)
        assert form.validate() == expected_result

def test_registration_submission(client):
    with app.app_context():
        response = setup_test_user_for_registration(client)
        assert response.status_code == 200
        assert b'Your account has been created; Your can now log in now' in response.data

def test_registration_submission_existing_user(client):
    with app.app_context():
        setup_database_with_test_user_credentials('test@email.com', 'password123')
        response = setup_test_user_for_registration(client)
        assert response.status_code == 200
        assert b'That username is taken' in response.data  # Check for error message

@pytest.mark.parametrize('email, password, expected_result', LOGIN_VALIDATION_PARAMETERS)
def test_login_account(client, email, password, expected_result):
    with app.app_context():
        response = setup_test_user_for_login(client, email, password)
        assert response.status_code == 200
        assert (b'Logged in successfully' in response.data) == expected_result  # Check for success message

@pytest.mark.parametrize('updated_username, updated_email, expected_message, test_case_type', UPDATE_VALIDATION_PARAMETERS)
def test_update_account(client, updated_username, updated_email, expected_message, test_case_type):
    with app.app_context():
        response = setup_test_user_for_login(client, 'test@example.com', 'password123')
        # Access the account update form
        response = client.get('/account')
        assert response.status_code == 200
        
        response = client.post('/account', data={
            'username': updated_username,
            'email': updated_email
        }, follow_redirects=True)

        # Check if the account was updated successfully
        assert response.status_code == 200
        assert expected_message in response.data

        # Check if the account was updated in the database
        if(test_case_type):
            updated_user = User.query.filter_by(email=updated_email).first()
            assert updated_user is not None
            assert updated_user.username == updated_username
