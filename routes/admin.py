from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from extensions import db


from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.department import Department
from models.appointment import Appointment
from models.prescription import Prescription
from models.medical_report import MedicalReport
from models.billing import Bill

admin = Blueprint("admin", __name__, url_prefix="/admin")


# ==========================================
# Admin Dashboard
# ==========================================

@admin.route("/dashboard")
@login_required
def dashboard():

    # --------------------------------------
    # Admin Access
    # --------------------------------------

    if not current_user.is_admin:
        return render_template("errors/403.html"), 403

    # --------------------------------------
    # Total Counts
    # --------------------------------------

    total_patients = Patient.query.count()

    total_doctors = Doctor.query.count()

    total_departments = Department.query.count()

    total_appointments = Appointment.query.count()

    total_prescriptions = Prescription.query.count()

    total_reports = MedicalReport.query.count()

    total_bills = Bill.query.count()

    # --------------------------------------
    # Revenue
    # --------------------------------------

    revenue = db.session.query(
        func.sum(Bill.grand_total)
    ).scalar()

    total_revenue = revenue or 0

    # --------------------------------------
    # Payment Status
    # --------------------------------------

    paid_bills = Bill.query.filter_by(
        payment_status="Paid"
    ).count()

    pending_bills = Bill.query.filter_by(
        payment_status="Pending"
    ).count()

    # --------------------------------------
    # Appointment Status
    # --------------------------------------

    pending_appointments = Appointment.query.filter_by(
        status="Pending"
    ).count()

    completed_appointments = Appointment.query.filter_by(
        status="Completed"
    ).count()

    cancelled_appointments = Appointment.query.filter_by(
        status="Cancelled"
    ).count()

    # --------------------------------------
    # Recent Patients
    # --------------------------------------

    recent_patients = (
        Patient.query
        .order_by(Patient.created_at.desc())
        .limit(5)
        .all()
    )

    # --------------------------------------
    # Recent Doctors
    # --------------------------------------

    recent_doctors = (
        Doctor.query
        .order_by(Doctor.created_at.desc())
        .limit(5)
        .all()
    )

    # --------------------------------------
    # Recent Appointments
    # --------------------------------------

    recent_appointments = (
        Appointment.query
        .order_by(Appointment.created_at.desc())
        .limit(5)
        .all()
    )

    # --------------------------------------
    # Recent Bills
    # --------------------------------------

    recent_bills = (
        Bill.query
        .order_by(Bill.created_at.desc())
        .limit(5)
        .all()
    )

    # --------------------------------------
    # Recent Prescriptions
    # --------------------------------------

    recent_prescriptions = (
        Prescription.query
        .order_by(Prescription.created_at.desc())
        .limit(5)
        .all()
    )

    # --------------------------------------
    # Recent Reports
    # --------------------------------------

    recent_reports = (
        MedicalReport.query
        .order_by(MedicalReport.created_at.desc())
        .limit(5)
        .all()
    )

    # --------------------------------------
    # Monthly Patient Registration Chart
    # --------------------------------------

    patient_chart = (
        db.session.query(
            func.extract("month", Patient.created_at),
            func.count(Patient.id)
        )
        .group_by(func.extract("month", Patient.created_at))
        .all()
    )

    patient_labels = []

    patient_values = []

    for month, total in patient_chart:

        patient_labels.append(int(month))

        patient_values.append(total)

    # --------------------------------------
    # Monthly Appointment Chart
    # --------------------------------------

    appointment_chart = (
        db.session.query(
            func.extract("month", Appointment.created_at),
            func.count(Appointment.id)
        )
        .group_by(func.extract("month", Appointment.created_at))
        .all()
    )

    appointment_labels = []

    appointment_values = []

    for month, total in appointment_chart:

        appointment_labels.append(int(month))

        appointment_values.append(total)

    # --------------------------------------
    # Monthly Revenue Chart
    # --------------------------------------

    revenue_chart = (
        db.session.query(
            func.extract("month", Bill.created_at),
            func.sum(Bill.grand_total)
        )
        .group_by(func.extract("month", Bill.created_at))
        .all()
    )

    revenue_labels = []

    revenue_values = []

    for month, total in revenue_chart:

        revenue_labels.append(int(month))

        revenue_values.append(float(total or 0))

    # --------------------------------------
    # Department Chart
    # --------------------------------------

    department_chart = (
        db.session.query(
            Department.name,
            func.count(Doctor.id)
        )
        .outerjoin(Doctor)
        .group_by(Department.name)
        .all()
    )

    department_labels = []

    department_values = []

    for name, total in department_chart:

        department_labels.append(name)

        department_values.append(total)

    # --------------------------------------
    # Dashboard
    # --------------------------------------

    return render_template(

        "admin/dashboard.html",

        total_patients=total_patients,
        total_doctors=total_doctors,
        total_departments=total_departments,
        total_appointments=total_appointments,
        total_prescriptions=total_prescriptions,
        total_reports=total_reports,
        total_bills=total_bills,

        total_revenue=total_revenue,

        paid_bills=paid_bills,
        pending_bills=pending_bills,

        pending_appointments=pending_appointments,
        completed_appointments=completed_appointments,
        cancelled_appointments=cancelled_appointments,

        recent_patients=recent_patients,
        recent_doctors=recent_doctors,
        recent_appointments=recent_appointments,
        recent_bills=recent_bills,
        recent_prescriptions=recent_prescriptions,
        recent_reports=recent_reports,

        patient_labels=patient_labels,
        patient_values=patient_values,

        appointment_labels=appointment_labels,
        appointment_values=appointment_values,

        revenue_labels=revenue_labels,
        revenue_values=revenue_values,

        department_labels=department_labels,
        department_values=department_values
    )