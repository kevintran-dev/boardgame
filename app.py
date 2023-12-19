from flask import Flask, render_template, request, flash, redirect, render_template, session, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, BoardGame
from forms import UserAddForm, LoginForm, AddBoardGameForm, EditBoardGameForm
from sqlalchemy.exc import IntegrityError
import requests
import os

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL', 'postgresql:///boardgame')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# Users

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

# Main

@app.route("/")
def homepage():
    """Show homepage"""
    
    return render_template("index.html")

@app.route("/your-list")
def ownlist():
    """Show Your List"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user_id = g.user.id
    user = User.query.get(user_id)
    return render_template("ownlist.html", user=user)

@app.route("/favorites")
def favlist():
    """Show Your List"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user_id = g.user.id
    user = User.query.get(user_id)
    return render_template("favorites.html", user=user)

@app.route("/add-game", methods=["GET", "POST"])
def add_game():
    """Add Board Games"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = AddBoardGameForm()
    print(g.user.username)
    
    if form.validate_on_submit():

        game_name = form.game_name.data
        bgg_id = form.bgg_id.data
        opened = form.opened.data
        played = form.played.data
        favorite = form.favorite.data
        print(game_name)
        print(bgg_id)
        if bgg_id:
            res = requests.get(f"https://bgg-json.azurewebsites.net/thing/{bgg_id}")
            data = res.json()
            gameId = data["gameId"]
            bgg_name = data["name"]
            new_game = BoardGame(bgg_id=gameId, name=bgg_name, ownedby=g.user.id, opened=opened, played=played, favorite=favorite)
            db.session.add(new_game)
            db.session.commit()
            return redirect('/your-list')
        else:
            new_game = BoardGame(name=game_name, ownedby=g.user.id, opened=opened, played=played, favorite=favorite)
            db.session.add(new_game)
            db.session.commit()
            return redirect('/your-list')

    return render_template("addgame.html", form=form)


@app.route("/edit-game/<int:game_id>", methods=["GET", "POST"])
def update_game(game_id):
    """Edit Board Games"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    game = BoardGame.query.get_or_404(game_id)
    form = EditBoardGameForm()
    
    if form.validate_on_submit():
        form.populate_obj(game)
        
        db.session.commit()
        return redirect('/your-list')
    else:
        form.name.data = game.name
        form.comments.data = game.comments
        form.favorite.data = game.favorite
        form.opened.data = game.opened
        form.played.data = game.played
        return render_template('editgame.html', form=form, game=game)

@app.route("/game/<int:game_id>")
def game_info(game_id):
    """BGG info"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    game = BoardGame.query.get_or_404(game_id)
    
    if game.bgg_id:
        res = requests.get(f"https://bgg-json.azurewebsites.net/thing/{game.bgg_id}")
        data = res.json()
    
        description = data["description"]
        desc = description.replace("&#10;&#10;", " ").replace('&quot;', '"').replace("&#10;", " ").replace("&mdash;","—").replace("&rsquo;","'").replace("&lsquo;","'").replace("&rdquo;",'"').replace("&ldquo;",'"').replace("&hellip;","...")
        return render_template('game.html', game=game, data=data, desc=desc)

    else:
        return render_template('game.html', game=game)

@app.route("/game/delete/<int:game_id>", methods=["POST"])
def remove_game(game_id):
    """Delete board game and remove from database."""

    game = BoardGame.query.get_or_404(game_id)

    db.session.delete(game)
    db.session.commit()
    return redirect("/your-list")

@app.route("/game/<int:game_id>/rating", methods=["POST"])
def change_ratings(game_id):
    
    game = BoardGame.query.get_or_404(game_id)
    rating = request.form.get('rating')
    game.rating = rating
    db.session.commit()
    return redirect("/your-list")

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

@app.route('/confirmation')
def confirm_delete():
    """Show Your List"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    return render_template("confirmation.html")