import json
import logging
import os
import secrets

from flask import (Flask, abort, current_app, flash, jsonify, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from modules import AlchemyEncoder, create_app, database
from modules.models import User

from .forms import LoginForm

from . import auth_blueprint


@auth_blueprint.route("/", methods=["GET"])
@login_required
def home():
    return render_template("index.html")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        flash("Already logged in!")
        current_app.logger.debug(f"Duplicate login attempt by user: {current_user.email}")
        return render_template("index.html")

    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            query = database.select(User).where(User.email == form.email.data)
            user = database.session.execute(query).scalar_one()

            if user and user.is_password_correct(form.password.data):
                # User's credentials have been validated, so log them in
                login_user(user, remember=form.remember_me.data)
                flash(f"Thanks for logging in, {current_user.email}!", "success")
                current_app.logger.debug(f"Logged in user: {current_user.email}")
                next_url = request.args.get('next')
                if next_url:
                    return redirect(next_url)

                return render_template("index.html")
            else:
                flash('ERROR! Incorrect login credentials.', 'error')
    
    return render_template("login.html", form=form)

@auth_blueprint.route("/logout")
@login_required
def logout():
    email=current_user.get_id()
    form=LoginForm()
    form.email.data=email

    current_app.logger.debug(f"Logged out user: {email}")
    logout_user()
    flash("Goodbye!")
    return render_template("login.html", form=form)

