from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class AddBoardGameForm(FlaskForm):
    """Add Board Game to list"""
    BOOL_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    game_name = StringField('Board Game Name', validators=[DataRequired()])
    bgg_id = StringField('Board Game Geek ID (optional)')
    favorite = SelectField('Favorite?', choices=BOOL_CHOICES)
    opened = SelectField('Have you opened the game yet?',choices=BOOL_CHOICES)
    played = SelectField('Have you played this?',choices=BOOL_CHOICES)

class EditBoardGameForm(FlaskForm):
    """Edit Board Game to list"""
    BOOL_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    name = StringField('Board Game Name', validators=[DataRequired()])
    comments = StringField('Comments?')
    favorite = SelectField('Favorite?', choices=BOOL_CHOICES)
    opened = SelectField('Have you opened the game yet?', choices=BOOL_CHOICES )
    played = SelectField('Have you played this?', choices=BOOL_CHOICES)
