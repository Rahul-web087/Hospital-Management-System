from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from extensions import db
from models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            full_name=full_name,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

# =====================================
# Logout
# =====================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )