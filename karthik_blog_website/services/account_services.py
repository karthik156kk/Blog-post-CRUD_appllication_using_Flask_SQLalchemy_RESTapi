from flask import url_for, flash, request
from karthik_blog_website import bcrypt, db
from karthik_blog_website.models import User
from flask_login import login_user, current_user

#validate current user
def is_current_user_authenticated():
    if current_user.is_authenticated:
        return True
    return False

#register new user -> involves submit validation, hashing password and storing in database
def register_user_from_form(register_form):
    if register_form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(username = register_form.username.data, email = register_form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created; Your can now log in now', 'success')
        return True
    return False

#login existing user -> involves submit validation, finding user in DB using email, 
#verifying entered password with hashed password in DB and logging the user in if matched 
def login_user_from_form(login_form):
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            flash('Logged in successfully', 'success')
            return True, None
        flash('Invalid Email or Password', 'danger')
    return False, login_form

#update existing user after logging in -> involves submit validation, changing current_user details
#or populate form fields with DB details and returning result
def update_user_from_form(updation_form, http_method):
    if http_method=='POST' and updation_form.validate_on_submit():
        current_user.username = updation_form.username.data
        current_user.email = updation_form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return True, None, None
    elif http_method == 'GET':
        updation_form.username.data = current_user.username
        updation_form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return False, updation_form, image_file