from flask import render_template, url_for, redirect, request, abort
from karthik_blog_website import app
from karthik_blog_website.forms import PostForm
from flask_login import login_required
from karthik_blog_website.services.post_services import new_post_from_form, is_author_not_current_user, get_post_if_available
from karthik_blog_website.services.post_services import update_post_in_database, delete_post_in_database
#create a new post (Create Post)
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    new_post_form = PostForm()
    if new_post_from_form(new_post_form):
        return redirect(url_for('home'))
    else:
        return render_template('create_update_post.html',
            title='New Post', form=new_post_form, legend='Create New Post')
    
#read a specific post (Retrieve Post)
@app.route("/post/<int:post_id>")
def post(post_id):
    read_post = get_post_if_available(post_id)
    return render_template('post.html', title='Post title', post=read_post)

#update a specific post - must be logged in (Update Post)
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    update_post = get_post_if_available(post_id)
    if is_author_not_current_user(update_post.author):
        abort(403)
    update_post_form = PostForm()
    success, update_post, update_post_form = update_post_in_database(update_post, update_post_form, request.method)
    if(success):
        return redirect(url_for('post', post_id=update_post.id))
    else:
        return render_template('create_update_post.html', title='Post title', form=update_post_form, legend='Update Post')


#delete a specific post - must be logged in (Delete Post)
@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    delete_post = get_post_if_available(post_id)
    if is_author_not_current_user(delete_post.author):
        abort(403)
    delete_post_in_database(delete_post)
    return redirect(url_for('home'))