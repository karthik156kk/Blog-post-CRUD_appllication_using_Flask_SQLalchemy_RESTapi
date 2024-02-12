from flask import render_template, url_for, flash, redirect, request, abort
from karthik_blog_website import app, bcrypt, db
from karthik_blog_website.models import User, Post
from karthik_blog_website.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required

title = 'flask home page'
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts = posts, title='title')

@app.route("/about")
def about():
    return render_template('about.html', title='about')