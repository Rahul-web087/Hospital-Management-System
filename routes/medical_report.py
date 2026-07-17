import os
from uuid import uuid4
from datetime import datetime
import cloudinary.uploader

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from werkzeug.utils import secure_filename

from extensions import db

from models.medical_report import MedicalReport
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment


# =====================================
# Blueprint
# =====================================

medical_report = Blueprint(
    "medical_report",
    __name__,
    url_prefix="/medical-reports"
)


# =====================================
# Medical Report List
# =====================================

@medical_report.route("/")
def list_reports():

    reports = MedicalReport.query.order_by(
        MedicalReport.created_at.desc()
    ).all()

    return render_template(
        "medical_report/list.html",
        reports=reports
    )


# =====================================
# View Medical Report
# =====================================

@medical_report.route("/view/<int:id>")
def view_report(id):

    report = MedicalReport.query.get_or_404(id)

    return render_template(
        "medical_report/view.html",
        report=report
    )


# =====================================
# Add Medical Report
# =====================================

@medical_report.route("/add", methods=["GET", "POST"])
def add_report():

    patients = Patient.query.order_by(
        Patient.user_id
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.user_id
    ).all()

    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc()
    ).all()

    if request.method == "POST":

        try:

            patient_id = request.form.get("patient_id")

            doctor_id = request.form.get("doctor_id")

            appointment_id = request.form.get(
                "appointment_id"
            )

            report_type = request.form.get(
                "report_type"
            )

            report_date = datetime.strptime(
                request.form.get("report_date"),
                "%Y-%m-%d"
            ).date()

            findings = request.form.get(
                "findings"
            )

            diagnosis = request.form.get(
                "diagnosis"
            )

            remarks = request.form.get(
                "remarks"
            )

            status = request.form.get(
                "status",
                "Pending"
            )

            # -----------------------------
            # Generate Report Number
            # -----------------------------

            last = MedicalReport.query.order_by(
                MedicalReport.id.desc()
            ).first()

            if last:
                number = last.id + 1
            else:
                number = 1

            report_no = f"REP{number:05d}"

            # -----------------------------
            # Upload Report File
            # -----------------------------

            report_file = None

            file = request.files.get("report_file")

            if file and file.filename:
                result = cloudinary.uploader.upload(
                    file,
                    folder="hospital-management/reports",
                    resource_type="auto"
                )

                report_file = result["secure_url"]

            report = MedicalReport(

                report_no=report_no,

                patient_id=patient_id,

                doctor_id=doctor_id,

                appointment_id=appointment_id,

                report_type=report_type,

                report_date=report_date,

                report_file=report_file,

                findings=findings,

                diagnosis=diagnosis,

                remarks=remarks,

                status=status

            )

            db.session.add(report)

            db.session.commit()

            flash(
                "Medical Report created successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "medical_report.list_reports"
                )
            )

        except Exception as e:

            db.session.rollback()

            flash(
                str(e),
                "danger"
            )

    return render_template(
        "medical_report/add.html",
        patients=patients,
        doctors=doctors,
        appointments=appointments
    )

# =====================================
# Edit Medical Report
# =====================================

@medical_report.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_report(id):

    report = MedicalReport.query.get_or_404(id)

    patients = Patient.query.order_by(
        Patient.user_id
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.user_id
    ).all()

    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc()
    ).all()

    if request.method == "POST":

        try:

            report.patient_id = request.form.get(
                "patient_id"
            )

            report.doctor_id = request.form.get(
                "doctor_id"
            )

            report.appointment_id = request.form.get(
                "appointment_id"
            )

            report.report_type = request.form.get(
                "report_type"
            )

            report.report_date = datetime.strptime(
                request.form.get("report_date"),
                "%Y-%m-%d"
            ).date()

            report.findings = request.form.get(
                "findings"
            )

            report.diagnosis = request.form.get(
                "diagnosis"
            )

            report.remarks = request.form.get(
                "remarks"
            )

            report.status = request.form.get(
                "status"
            )

            # -----------------------------
            # Upload New Report File
            # -----------------------------

            file = request.files.get("report_file")

            if file and file.filename:
                result = cloudinary.uploader.upload(
                    file,
                    folder="hospital-management/reports",
                    resource_type="auto"
                )

                report.report_file = result["secure_url"]

            db.session.commit()

            flash(
                "Medical Report updated successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "medical_report.list_reports"
                )
            )

        except Exception as e:

            db.session.rollback()

            flash(
                str(e),
                "danger"
            )

    return render_template(
        "medical_report/edit.html",
        report=report,
        patients=patients,
        doctors=doctors,
        appointments=appointments
    )

# =====================================
# Delete Medical Report
# =====================================

@medical_report.route("/delete/<int:id>")
def delete_report(id):

    report = MedicalReport.query.get_or_404(id)

    try:



        db.session.delete(report)
        db.session.commit()

        flash(
            "Medical Report deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            str(e),
            "danger"
        )

    return redirect(
        url_for(
            "medical_report.list_reports"
        )
    )


# =====================================
# Change Report Status
# =====================================

@medical_report.route("/status/<int:id>/<status>")
def change_status(id, status):

    report = MedicalReport.query.get_or_404(id)

    allowed_status = [
        "Pending",
        "Completed"
    ]

    if status not in allowed_status:

        flash(
            "Invalid status.",
            "danger"
        )

        return redirect(
            url_for(
                "medical_report.list_reports"
            )
        )

    report.status = status

    db.session.commit()

    flash(
        "Report status updated successfully.",
        "success"
    )

    return redirect(
        url_for(
            "medical_report.list_reports"
        )
    )


# =====================================
# Pending Reports
# =====================================

@medical_report.route("/pending")
def pending_reports():

    reports = MedicalReport.query.filter_by(
        status="Pending"
    ).order_by(
        MedicalReport.created_at.desc()
    ).all()

    return render_template(
        "medical_report/list.html",
        reports=reports
    )


# =====================================
# Completed Reports
# =====================================

@medical_report.route("/completed")
def completed_reports():

    reports = MedicalReport.query.filter_by(
        status="Completed"
    ).order_by(
        MedicalReport.created_at.desc()
    ).all()

    return render_template(
        "medical_report/list.html",
        reports=reports
    )


# =====================================
# Print Medical Report
# =====================================

@medical_report.route("/print/<int:id>")
def print_report(id):

    report = MedicalReport.query.get_or_404(id)

    return render_template(
        "medical_report/print.html",
        report=report
    )