import re
import unittest
from flask import current_app, url_for
from app import create_app, db
from app.models import User, Role


class BlogClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.generate_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_users_visit_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_app.config['APP_NAME'] in response.get_data(as_text=True))

    def test_register_and_login(self):
        response = self.client.post('/register', data={
            'username': 'jose',
            'email': 'jose@gmail.com',
            'password': '12345jose67',
            'password_conf': '12345jose67',
        })

        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login', data={
            'email': 'jose@gmail.com',
            'password': '12345jose67'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('jose' in response.get_data(as_text=True))

        # Logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_auth_can_create_posts(self):
        author = User(email='user1@mail.com', username='user1', confirmed=True, password='user')
        response = self.client.post(url_for('posts.new'), data={
            'title': 'Post 1',
            'content': 'Content from Post 1',
            'author': author,
        })

        # Redireccionamiento del usuario al crear el post
        self.assertEqual(response.status_code, 302)

    def test_it_redirect_of_user_to_register(self):
        response = self.client.get(url_for('posts.new'))
        self.assertEqual(response.status_code, 302)

    def test_it_create_post_for_author(self):
        user = User(email='user1@mail.com', username='user1', confirmed=True, password='user')
        db.session.add(user)
        db.session.commit()
        response = self.client.post(url_for('posts.new'), data={
            'title': 'Post 1',
            'content': 'Content from Post 1',
            'user_id': user.id
        })
        self.assertEqual(response.status_code, 302)

    def test_it_create_post_view_errors_title(self):
        user = User(email='user1@mail.com', username='user1', confirmed=True, password='user')
        response = self.client.post(url_for('posts.new'), data={
            'title': '',
            'content': 'Content from Post 1',
            'user_id': user.id
        })
        self.assertEqual(response.status_code, 302)

    def test_it_create_post_view_errors_content(self):
        user = User(email='user1@mail.com', username='user1', confirmed=True, password='user')
        response = self.client.post(url_for('posts.new'), data={
            'title': 'Post 1',
            'content': '',
            'user_id': user.id
        })
        self.assertEqual(response.status_code, 302)
