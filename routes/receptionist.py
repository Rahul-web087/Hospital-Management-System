from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.billing import Bill

receptionist = Blueprint(
    "receptionist",
    __name__,
    url_prefix="/reception"
)


# =====================================
# Receptionist Dashboard
# =====================================
@receptionist.route("/dashboard")
@login_required
def dashboard():

    if not current_user.is_receptionist:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    today = date.today()

    total_patients = Patient.query.count()

    today_patients = Patient.query.filter(
        db.func.date(Patient.created_at) == today
    ).count()

    total_doctors = Doctor.query.count()

    today_appointments = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == today
    ).count()

    waiting = Appointment.query.filter_by(status="Pending").count()

    completed = Appointment.query.filter_by(status="Completed").count()

    pending_bills = Bill.query.filter_by(payment_status="Pending").count()

    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc()
    ).limit(10).all()

    return render_template(
        "receptionist/dashboard.html",
        total_patients=total_patients,
        today_patients=today_patients,
        total_doctors=total_doctors,
        today_appointments=today_appointments,
        waiting=waiting,
        completed=completed,
        pending_bills=pending_bills,
        appointments=appointments,
    )


# =====================================
# Register Patient
# =====================================
@receptionist.route("/register-patient")
@login_required
def register_patient():

    if not current_user.is_receptionist:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("patient.add_patient"))


# =====================================
# Search Patient
# =====================================
@receptionist.route("/search-patient")
@login_required
def search_patient():

    if not current_user.is_receptionist:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("patient.list_patients"))


# =====================================
# Book Appointment
# =====================================
@receptionist.route("/book-appointment")
@login_required
def book_appointment():

    if not current_user.is_receptionist:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("appointment.add_appointment"))


# =====================================
# Queue Management
# =====================================
@receptionist.route("/queue")
@login_required
def queue():

    if not current_user.is_receptionist:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    queue = Appointment.query.filter_by(
        status="Pending"
    ).order_by(
        Appointment.token_number.asc()
    ).all()

    return render_template(
        "receptionist/queue.html",
        queue=queue
    )


# =====================================
# Today's Appointments
# =====================================
@receptionist.route("/today")
@login_required
def today():

    if not current_user.is_receptionist:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("appointment.today_appointments"))


# =====================================
# Billing
# =====================================
@receptionist.route("/billing")
@login_required
def billing():

    if not current_user.is_receptionist:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("billing.list_bills"))