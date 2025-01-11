from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            if bcrypt.check_password_hash(existing_user.password, password):
                flash("Logged in successfully!!", category="success")
                login_user(existing_user, remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash("Incorrect password, try again", category="error")
        else:
            flash("User does not exist", category="error")

    return  render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return  redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        fullname = request.form.get("fullname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(fullname) < 6:
            flash("Full name must be more than 5 characters", category="error")
        elif len(email) < 8:
            flash("Email must be more than 7 characters", category="error")
        elif len(password1) < 8:
            flash("Password must be more than 7 characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        else:
            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists. Please use a different email.', category='error')
            else:
                # Hash the password and create a new user
                hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
                new_user = User(fullname=fullname, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created', category='success')
                login_user(existing_user, remember=True)
                return redirect(url_for('views.homepage'))

    return  render_template("sign-up.html", user=current_user)