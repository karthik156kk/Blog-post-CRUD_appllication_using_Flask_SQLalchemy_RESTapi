from flask import render_template, url_for, redirect, request
from karthik_blog_website import app
from karthik_blog_website.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import logout_user, login_required
from karthik_blog_website.services.account_services import is_current_user_authenticated, register_user_from_form
from karthik_blog_website.services.account_services import login_user_from_form, update_user_from_form

#account creation (Create Account)
@app.route("/register", methods=['GET', 'POST'])
def register():
    if is_current_user_authenticated():
        redirect(url_for('home'))
    register_form = RegistrationForm()
    if register_user_from_form(register_form):
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title='Register', form = register_form)

#account accessing (Retrieve Account)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if is_current_user_authenticated():
        return redirect(url_for('home'))
    login_form = LoginForm()
    success, login_form = login_user_from_form(login_form)
    if success:
        next_page = request.args.get('next')
        return redirect(next_page or url_for('home'))
    return render_template('login.html', title='Log in', form=login_form)

#account accessing (Retrieve Account)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#account updation (Update Account)
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    updation_form = UpdateAccountForm()
    success, updation_form, image_file = update_user_from_form(updation_form, request.method)
    if success:
        return redirect(url_for('account'))
    else:
        return render_template('account.html', title='Account', image_file=image_file, form=updation_form)
    