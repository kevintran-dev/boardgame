"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_boardgame_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, BoardGame

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///boardgame_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "password")
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_boardgame_model(self):
        """Does basic model work?"""
        
        game = BoardGame(
            name="Resident Evil",
            ownedby=self.uid
        )

        db.session.add(game)
        db.session.commit()

        # User should have 1 boardgame
        self.assertEqual(len(self.u.boardgame), 1)
        self.assertEqual(self.u.boardgame[0].name, "Resident Evil")
