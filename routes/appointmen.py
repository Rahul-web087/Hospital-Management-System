from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from extensions import db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor


appointment = Blueprint(
    "appointment",
    __name__,
    url_prefix="/appointments"
)


# =====================================
# Appointment List
# =====================================

@appointment.route("/")
def list_appointments():

    appointments = Appointment.query.order_by(
        Appointment.id.desc()
    ).all()

    return render_template(
        "appointment/list.html",
        appointments=appointments
    )


# =====================================
# Appointment Details
# =====================================

@appointment.route("/view/<int:id>")
def view_appointment(id):

    appointment_data = Appointment.query.get_or_404(id)

    return render_template(
        "appointment/view.html",
        appointment=appointment_data
    )


# =====================================
# Add Appointment
# =====================================

@appointment.route("/add", methods=["GET", "POST"])
def add_appointment():

    patients = Patient.query.all()
    doctors = Doctor.query.all()

    if request.method == "POST":

        patient_id = request.form.get("patient_id")
        doctor_id = request.form.get("doctor_id")

        appointment_date = datetime.strptime(
            request.form.get("appointment_date"),
            "%Y-%m-%d"
        ).date()

        appointment_time = datetime.strptime(
            request.form.get("appointment_time"),
            "%H:%M"
        ).time()

        reason = request.form.get("reason")

        visit_type = request.form.get(
            "visit_type",
            "OPD"
        )

        fee = request.form.get("fee") or 0

        status = request.form.get(
            "status",
            "Pending"
        )

        remarks = request.form.get("remarks")

        # Generate Appointment Number
        last = Appointment.query.order_by(
            Appointment.id.desc()
        ).first()

        if last:
            number = last.id + 1
        else:
            number = 1

        appointment_no = f"APT{number:05d}"

        # Token Number
        today_count = Appointment.query.filter_by(
            appointment_date=appointment_date
        ).count()

        token_number = today_count + 1

        appointment = Appointment(
            appointment_no=appointment_no,
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            visit_type=visit_type,
            token_number=token_number,
            fee=fee,
            reason=reason,
            status=status,
            remarks=remarks
        )

        db.session.add(appointment)
        db.session.commit()

        flash(
            "Appointment booked successfully.",
            "success"
        )

        return redirect(
            url_for(
                "appointment.list_appointments"
            )
        )

    return render_template(
        "appointment/add.html",
        patients=patients,
        doctors=doctors
    )

# =====================================
# Edit Appointment
# =====================================

@appointment.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_appointment(id):

    appointment_data = Appointment.query.get_or_404(id)

    patients = Patient.query.all()
    doctors = Doctor.query.all()

    if request.method == "POST":

        appointment_data.patient_id = request.form.get(
            "patient_id"
        )

        appointment_data.doctor_id = request.form.get(
            "doctor_id"
        )

        appointment_data.appointment_date = datetime.strptime(
            request.form.get("appointment_date"),
            "%Y-%m-%d"
        ).date()

        appointment_data.appointment_time = datetime.strptime(
            request.form.get("appointment_time"),
            "%H:%M"
        ).time()

        appointment_data.visit_type = request.form.get(
            "visit_type"
        )

        appointment_data.fee = request.form.get(
            "fee"
        ) or 0

        appointment_data.reason = request.form.get(
            "reason"
        )

        appointment_data.status = request.form.get(
            "status"
        )

        appointment_data.remarks = request.form.get(
            "remarks"
        )

        db.session.commit()

        flash(
            "Appointment updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "appointment.list_appointments"
            )
        )

    return render_template(
        "appointment/edit.html",
        appointment=appointment_data,
        patients=patients,
        doctors=doctors
    )


# =====================================
# Delete Appointment
# =====================================

@appointment.route("/delete/<int:id>")
def delete_appointment(id):

    appointment_data = Appointment.query.get_or_404(id)

    db.session.delete(appointment_data)

    db.session.commit()

    flash(
        "Appointment deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "appointment.list_appointments"
        )
    )


# =====================================
# Toggle Appointment Status
# =====================================

@appointment.route("/status/<int:id>/<status>")
def change_status(id, status):

    appointment_data = Appointment.query.get_or_404(id)

    allowed_status = [
        "Pending",
        "Confirmed",
        "Completed",
        "Cancelled"
    ]

    if status not in allowed_status:

        flash(
            "Invalid status.",
            "danger"
        )

        return redirect(
            url_for(
                "appointment.list_appointments"
            )
        )

    appointment_data.status = status

    db.session.commit()

    flash(
        "Appointment status updated successfully.",
        "success"
    )

    return redirect(
        url_for(
            "appointment.list_appointments"
        )
    )


# =====================================
# Today's Appointments
# =====================================

@appointment.route("/today")
def today_appointments():

    today = datetime.today().date()

    appointments = Appointment.query.filter(
        Appointment.appointment_date == today
    ).order_by(
        Appointment.appointment_time.asc()
    ).all()

    return render_template(
        "appointment/list.html",
        appointments=appointments
    )


# =====================================
# Upcoming Appointments
# =====================================

@appointment.route("/upcoming")
def upcoming_appointments():

    today = datetime.today().date()

    appointments = Appointment.query.filter(
        Appointment.appointment_date > today
    ).order_by(
        Appointment.appointment_date.asc(),
        Appointment.appointment_time.asc()
    ).all()

    return render_template(
        "appointment/list.html",
        appointments=appointments
    )


# =====================================
# Completed Appointments
# =====================================

@appointment.route("/completed")
def completed_appointments():

    appointments = Appointment.query.filter_by(
        status="Completed"
    ).order_by(
        Appointment.appointment_date.desc()
    ).all()

    return render_template(
        "appointment/list.html",
        appointments=appointments
    )


# =====================================
# Pending Appointments
# =====================================

@appointment.route("/pending")
def pending_appointments():

    appointments = Appointment.query.filter_by(
        status="Pending"
    ).order_by(
        Appointment.appointment_date.asc()
    ).all()

    return render_template(
        "appointment/list.html",
        appointments=appointments
    )