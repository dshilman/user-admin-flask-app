from datetime import datetime

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
# from flask_login import current_user, login_required
from flask_security import login_required, current_user
from modules import database, required_roles
from modules.models import User, Firm
from sqlalchemy.exc import IntegrityError


from . import users_blueprint
from .forms import UserForm



@users_blueprint.route("/get/<email>", methods=["GET"])
@login_required
@required_roles(["Admin"])
def get(email: str):

    form = UserForm()
    if email:
        query = database.select(User).where(User.email == email)
        user: User = database.session.execute(query).scalar_one_or_none()
        if user:
            form.populate(user)
            return render_template("user_profile.html", form=form)

    return render_template("user_profile.html", form=form)


@users_blueprint.route("/add", methods=["GET"])
@login_required
@required_roles(["Admin"])
def add():

    form = UserForm()
    return render_template("user_profile.html", form=form)


@users_blueprint.route("/all", methods=["GET"])
@login_required
@required_roles(["Admin"])
def get_users():

    query = database.select(User)
    users = database.session.execute(query).scalars().all()
    return render_template("users.html", users=users)


@users_blueprint.route("/delete/<email>", methods=["GET", "POST"])
@login_required
@required_roles(["Admin"])
def delete(email):
    query = database.select(User).where(User.email == email)
    user: User = database.session.execute(query).scalar_one_or_none()
    database.session.delete(user)
    database.session.commit()
    current_app.logger.debug(f"Deleted user: {email}!")
    flash(f"Thanks, user deleted: {email}!")
    return redirect(url_for("users.get_users"))


@users_blueprint.route("update/", methods=["POST"])
@login_required
@required_roles(["Admin"])
def update():

    form = UserForm()
    user_query = database.select(User).where(User.email == form.email.data)
    user: User = database.session.execute(user_query).scalar_one_or_none()

    firm_query = database.select(Firm).where(Firm.firm_name == form.firm.data)
    firm: Firm = database.session.execute(firm_query).scalar_one_or_none()
    if form.validate_on_submit():

        if user is None:
            try:
                user = User(
                    email=form.email.data,
                    password=form.password.data,
                    first_name=form.fname.data,
                    last_name=form.lname.data,
                    role=form.role.data,
                )
                user.firm = firm

                database.session.add(user)
                database.session.commit()
                flash(f"Thanks, user added: {user.email}!")
                current_app.logger.debug(f"Added user: {form.email.data}!")
                return redirect("../all")
            except IntegrityError:
                database.session.rollback()
                flash(f"ERROR! Email ({form.email.data}) already exists.", "error")
        else:
            try:
                user.update(request)
                user.firm = firm
                database.session.add(user)
                database.session.commit()
                flash(f"Thanks, user updated: {user.email}!")
                current_app.logger.debug(f"Updated user: {form.email.data}!")
                return redirect("../all")
            except IntegrityError:
                database.session.rollback()
                flash(f"ERROR! Email ({form.email.data}) already exists.", "error")
    else:
        flash(f"Error in form data!")

    return render_template("user_profile.html", form=form)
