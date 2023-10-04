"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "IT'S A SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.get("/")
def redirect_to_users():
    """Redirects to /users."""

    return redirect("/users")

@app.get("/users")
def list_users():
    """List all users"""

    users = User.query.order_by('last_name', 'first_name').all()
    return render_template('users.html', users=users)

@app.get("/users/new")
def display_new_user_form():
    """Display the form for adding a new user"""

    return render_template('create_user.html')

@app.post("/users/new")
def handle_new_user_form_submit():
    """Add new user's details to database"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']

    image_url = (request.form['image_url'] or None)

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    flash(f"User successfully added: {first_name} {last_name}")

    return redirect('/users')

@app.get("/users/<int:user_id>")
def show_user_details(user_id):
    """Show details about a particular user"""

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.get("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """Show form for editing details about a particular user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.post("/users/<int:user_id>/edit")
def update_user_details(user_id):
    """Update the user's details in the database"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    flash(f"User updated successfully: {first_name} {last_name}")

    return redirect('/users')

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user from the database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User deleted successfully: {user.first_name} {user.last_name}")

    return redirect('/users')