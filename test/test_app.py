# Import the necessary modules
from flask import redirect, url_for, render_template, request
from flask_testing import TestCase

# import the app's classes and objects
from application import app, db
from application.models import ToDos
from application.forms import TaskForm

# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app. 
        # Here we use sqlite without a persistent database for our tests.
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///data.db",
                SECRET_KEY="shhh it's a secret",
                DEBUG=True,
                WTF_CSRF_ENABLED=False
                )
        return app

    # Will be called before every test
    def setUp(self):
        # Create table
        db.create_all()
        # Create test registree
        sample1 = ToDos(task="MsWoman")
        # save users to database
        db.session.add(sample1)
        db.session.commit()

    # Will be called after every test
    def tearDown(self):
        # Close the database session and remove all contents of the database
        db.session.remove()
        db.drop_all()

# Write a test class to test Read functionality
class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'MsWoman', response.data)

    def test_about_get(self):
        response = self.client.get(url_for('about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is the abut page', response.data)

# class TestCreate(TestBase):
#     def test_create(self):
#         response = self.client.post(
#             url_for('addtask'),
#             data = Todos(task="Ryan", completed=True)
#         )
#         self.assertIn(b'Ryan', response.data)

