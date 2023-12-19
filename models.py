from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    boardgame = db.relationship("BoardGame", backref="user", cascade="all,delete")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"
    
    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class BoardGame(db.Model):
    """List of board games"""

    __tablename__ = 'boardgames'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    bgg_id = db.Column(
        db.Integer,
        nullable=True,
    )
    rating = db.Column(
        db.Integer,
        nullable=True,
    )
    favorite = db.Column(
        db.Text, nullable=True, 
    )
    opened = db.Column(
        db.Text, nullable=True, 
    )
    played = db.Column(
        db.Text, nullable=True,
    )
    comments = db.Column(
        db.Text, nullable=True,
    )
    ownedby = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
    )

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
