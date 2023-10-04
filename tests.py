import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User

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
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

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


    def test_submit_new_user_form(self):
        """Test submit new user form"""

        with app.test_client() as c:
            resp = c.post("/users/new",
                          data={'first_name': 'test_new_user_first',
                                'last_name': 'test_new_user_last',
                                'image_url':('https://www.google.com/url?sa=i&'
                                             'url=https%3A%2F%2Fen.wikipedia.org'
                                             '%2Fwiki%2FSpider_monkey&psig=AOvVa'
                                             'w2nCIQXb6JI04Ek_NBaWCpE&ust=169654'
                                             '3223657000&source=images&cd=vfe&opi'
                                             '=89978449&ved=0CBAQjRxqFwoTCMDg-pKy'
                                             '3YEDFQAAAAAdAAAAABAE')
                                },
                           follow_redirects=True
                                )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('test_new_user_first test_new_user_last', html)


    def test_show_user_details(self):
        """Test user detail page"""
# TODO: Test for user's name for correct display
        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- User Detail Template - used in testing -->", html)


    def test_show_edit_user_form(self):
        """Test edit user detail form page"""
# TODO: Test for if correct user is displayed
        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Edit User Form Template - used in testing -->", html)





