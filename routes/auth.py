from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models.user import User

auth = Blueprint("auth", __name__)


# =====================================
# Login
# =====================================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == User.ROLE_ADMIN:
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == User.ROLE_DOCTOR:
            return redirect(url_for("doctor.dashboard"))

        elif current_user.role == User.ROLE_PATIENT:
            return redirect(url_for("patient.dashboard"))

        return redirect(url_for("home"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found.", "danger")
            return redirect(url_for("auth.login"))

        if not user.check_password(password):
            flash("Invalid password.", "danger")
            return redirect(url_for("auth.login"))

        if not user.is_active:
            flash("Your account is disabled.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)

        flash(f"Welcome {user.full_name}", "success")

        # Role Redirect
        if user.role == User.ROLE_ADMIN:
            return redirect(url_for("admin.dashboard"))

        elif user.role == User.ROLE_DOCTOR:
            return redirect(url_for("doctor.dashboard"))

        elif user.role == User.ROLE_PATIENT:
            return redirect(url_for("patient.dashboard"))

        elif user.role == User.ROLE_RECEPTIONIST:
            return redirect(url_for("appointment.dashboard"))

        elif user.role == User.ROLE_PHARMACIST:
            return redirect(url_for("billing.list_bills"))

        elif user.role == User.ROLE_ACCOUNTANT:
            return redirect(url_for("billing.list_bills"))

        elif user.role == User.ROLE_LAB:
            return redirect(url_for("medical_report.list_reports"))

        return redirect(url_for("home"))

    return render_template("auth/login.html")


# =====================================
# Register (Patient Only)
# =====================================
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
            email=email,
            role=User.ROLE_PATIENT
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

    flash("Logged out successfully.", "success")

    return redirect(url_for("auth.login"))