import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.test_user = User(
            id=99, # Will only work as long as there are < 99 users in test db at a time.-
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        self.test_post_title = 'test1_title' # Need this for testing delete.
        self.test_post = Post(
            title=self.test_post_title,
            content='test1_content',
            user_id=self.test_user.id
        )

        db.session.add(self.test_user)
        db.session.add(self.test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.

        # self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_list_users(self):
        """Test list users page"""

        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)


    def test_display_new_user_form(self):
        """Test new user form page"""

        with app.test_client() as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Create User Form Template - used for testing -->", html)


    def test_handle_new_user_form_submit(self):
        """Test submit new user form"""

        with app.test_client() as c:
            resp = c.post("/users/new",
                          data={'first_name': 'test_new_user_first',
                                'last_name': 'test_new_user_last',
                                'image_url': DEFAULT_IMAGE_URL
                                },
                           follow_redirects=True
                                )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('test_new_user_first test_new_user_last', html)


    def test_show_user_details(self):
        """Test user detail page"""

        with app.test_client() as c:
            resp = c.get(f"/users/{self.test_user.id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- User Detail Template - used in testing -->", html)
            self.assertIn((f"<h1>{ self.test_user.first_name }"
                           f" { self.test_user.last_name }</h1>"), html)


    def test_show_edit_user_form(self):
        """Test edit user detail form page"""

        with app.test_client() as c:
            resp = c.get(f"/users/{self.test_user.id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Edit User Form Template - used in testing -->", html)
            self.assertIn((f"<h1>Edit { self.test_user.first_name }"
                           f" { self.test_user.last_name }</h1>"), html)


    def test_show_new_post_form(self):
        """Test new post form page"""

        with app.test_client() as c:
            resp = c.get(f"/users/{self.test_user.id}/posts/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Create Post Form Template - used for testing -->", html)


    def test_handle_new_post_submit(self):
        """Test handling of new post submition"""

        with app.test_client() as c:
            resp = c.post(f"/users/{self.test_user.id}/posts/new",
                          data={'user_id': self.test_user.id,
                                'title': 'test_title',
                                'content': 'test_content'
                                },
                           follow_redirects=True
                                )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('test_title', html)


    def test_show_post_content(self):
        """Test post content page"""

        with app.test_client() as c:
            resp = c.get(f"/posts/{self.test_post.id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Post Template - used for testing -->", html)
            self.assertIn(self.test_post.title, html)
            self.assertIn(self.test_post.content, html)


    def test_show_edit_post_form(self):
        """Test show edit post page"""

        with app.test_client() as c:
            resp = c.get(f"/posts/{self.test_post.id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Edit Post Form Template - used for testing -->", html)
            self.assertIn(self.test_post.title, html)
            self.assertIn(self.test_post.content, html)

    def test_handle_edit_post_submission(self):
        """Test handling an edit post submission."""

        with app.test_client() as c:
            resp = c.post(f"/posts/{self.test_post.id}/edit",
                          data={'title': 'test_title_edited',
                                'content': 'test_content_edited'
                                },
                           follow_redirects=True
                                )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('test_title_edited', html)
            self.assertIn('test_content_edited', html)

    def test_handle_delete_post(self):
        """Test handling deleting a post."""

        with app.test_client() as c:
            resp = c.post(f"/posts/{self.test_post.id}/delete",
                           follow_redirects=True
                                )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            # Deleted title should only show up once (in flashed message).
            self.assertTrue(html.count(self.test_post.title) == 1)






