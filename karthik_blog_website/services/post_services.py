from flask import flash
from karthik_blog_website import db
from karthik_blog_website.models import Post
from flask_login import current_user
#check if author of a post is not the current user
def is_author_not_current_user(author):
    return author != current_user
#returns Post it finds the post with specified post_id else returns 404 - forbidden page
def get_post_if_available(post_id):
    return Post.query.get_or_404(post_id)
        
def new_post_from_form(new_post_form):
    if new_post_form.validate_on_submit():
        post = Post(title=new_post_form.title.data, content=new_post_form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return True
    return False

def update_post_in_database(update_post, update_post_form, http_method):
    if update_post_form.validate_on_submit():
        update_post.title = update_post_form.title.data
        update_post.content = update_post_form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return True, update_post, None
    elif http_method == 'GET':
        update_post_form.title.data = update_post.title
        update_post_form.content.data = update_post.content
    return False, None, update_post_form

def delete_post_in_database(delete_post):
    db.session.delete(delete_post)
    db.session.commit()
    flash('Your post has been Deleted!', 'success')