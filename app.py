"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

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
    posts = (Post
        .query
        .filter(Post.user_id == user.id)
        .order_by(Post.created_at.desc())
        .all())
    return render_template("user_detail.html", user=user, posts=posts)

@app.get("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """Show form for editing details about a particular user"""

    user = User.query.get_or_404(user_id)
    posts = User.posts
    return render_template('edit_user.html', user=user, posts=posts)

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
    """Delete the user and user's posts from the database"""

    user = User.query.get_or_404(user_id)

    Post.query.filter(Post.user_id == user.id).delete()
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.first_name} {user.last_name} \
        deleted successfully.")

    return redirect('/users')

@app.get("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """Show new post form."""

    User.query.get_or_404(user_id) # Just to validate.
    tags = Tag.query.all()
    return render_template("create_post.html", user_id=user_id, tags=tags)

@app.post("/users/<int:user_id>/posts/new")
def handle_new_post_submit(user_id):
    """
    Updates the database with the new post,
    redirects to /posts.
    """

    User.query.get_or_404(user_id) # Just to validate.

    title = request.form["title"]
    content = request.form["content"]

    tag_ids = [int(tag_id) for tag_id in request.form.getlist('tag')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title, content=content, user_id=user_id)
    post.tags = tags
    #breakpoint()

    db.session.add(post)
    db.session.commit()

    flash(f"\"{title}\" successfully posted.")

    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def show_post_content(post_id):
    """Shows the content of a particular post."""

    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@app.get("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """Shows the form where a user can edit a post."""

    post = Post.query.get_or_404(post_id)

    unselected_tags = Tag.query.filter(~Tag.id.in_([tag.id for tag in post.tags]))

    return render_template(
        "edit_post.html",
        post=post,
        unselected_tags=unselected_tags)

@app.post("/posts/<int:post_id>/edit")
def handle_edit_post_submission(post_id):
    """
    Handles updating the database and redirecting after
    a user submits an edit to a post.
    """

    post = Post.query.get_or_404(post_id)

    tag_ids = [int(tag_id) for tag_id in request.form.getlist('tag')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = tags

    db.session.commit()

    flash(f"\"{post.title}\" successfully updated.")

    return redirect(f"/posts/{post.id}")

@app.post("/posts/<int:post_id>/delete")
def handle_delete_post(post_id):
    """Handles deleting a post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post \"{post.title}\" deleted successfully.")

    return redirect(f'/users/{post.user_id}')

@app.get("/tags")
def show_tags():
    """Shows a list of all tags."""

    tags = Tag.query.order_by('name').all()
    return render_template("tags.html", tags=tags)


@app.get("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """Shows details about a specific tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_detail.html", tag=tag)

@app.get("/tags/new")
def show_new_tag_form():
    """Shows new tag form."""

    return render_template("create_tag.html")


@app.post("/tags/new")
def handle_new_tag_submit():
    """Handles new tag submit."""

    name = request.form['name']

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    flash(f"Tag \"{tag.name}\" added successfully.")

    return redirect(f'/tags')


@app.get("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
    """Shows edit tag form."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("create_tag.html", tag=tag)

@app.post("/tags/<int:tag_id>/edit")
def handle_edit_tag_submission(tag_id):
    """Handles edit tag submit."""

    name = request.form['name']

    tag = Tag.query.get_or_404(tag_id)
    tag.name = name

    db.session.commit()

    flash(f"Tag \"{tag.name}\" updated successfully.")

    return redirect(f'/tags')

@app.post("/tags/<int:tag_id>/delete")
def handle_delete_tag(tag_id):
    """Handles deleting a tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag \"{tag.name}\" deleted successfully.")

    return redirect(f'/tags')