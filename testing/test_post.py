from karthik_blog_website import app, db, bcrypt
from karthik_blog_website.models import User, Post
from testing.conftest import setup_test_user_for_login
def test_create_update_post(client):
    with app.app_context():
        setup_test_user_for_login(client, 'test@example.com', 'password123')
        response = client.get('/post/new')
        assert response.status_code == 200
        
        # Submit a POST request to create a new post
        response = client.post('/post/new', data={
            'title': 'Test Post',
            'content': 'This is a test post content'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Check if the post exists in the database
        post = Post.query.filter_by(title='Test Post').first()
        assert post is not None

        # Update the created post
        response = client.post(f'/post/{post.id}/update', data={
            'title': 'Updated Test Post',
            'content': 'This is the updated test post content'
        }, follow_redirects=True)
        # Check if the post was updated successfully
        assert response.status_code == 200
        assert b'Your post has been updated!' in response.data
        # Check if the post was updated in the database
        updated_post = Post.query.filter_by(id=post.id).first()
        assert updated_post is not None
        assert updated_post.title == 'Updated Test Post'
        assert updated_post.content == 'This is the updated test post content'
        
        # Delete the updated post
        response = client.post(f'/post/{post.id}/delete', follow_redirects=True)
        # Check if the post was deleted successfully
        assert response.status_code == 200
        assert b'Your post has been Deleted!' in response.data
        # Check if the post was deleted from the database
        deleted_post = Post.query.filter_by(id=post.id).first()
        assert deleted_post is None

