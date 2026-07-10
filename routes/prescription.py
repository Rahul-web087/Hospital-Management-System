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

from models.prescription import (
    Prescription,
    PrescriptionMedicine
)

from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor


prescription = Blueprint(
    "prescription",
    __name__,
    url_prefix="/prescriptions"
)


# =====================================
# Prescription List
# =====================================

@prescription.route("/")
def list_prescriptions():

    prescriptions = Prescription.query.order_by(
        Prescription.id.desc()
    ).all()

    return render_template(
        "prescription/list.html",
        prescriptions=prescriptions
    )


# =====================================
# View Prescription
# =====================================

@prescription.route("/view/<int:id>")
def view_prescription(id):

    prescription_data = Prescription.query.get_or_404(id)

    medicines = PrescriptionMedicine.query.filter_by(
        prescription_id=id
    ).all()

    return render_template(
        "prescription/view.html",
        prescription=prescription_data,
        medicines=medicines
    )


# =====================================
# Add Prescription
# =====================================

@prescription.route("/add", methods=["GET", "POST"])
def add_prescription():

    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc()
    ).all()

    patients = Patient.query.order_by(
        Patient.id.desc()
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.id.desc()
    ).all()

    if request.method == "POST":

        appointment_id = request.form.get(
            "appointment_id"
        )

        patient_id = request.form.get(
            "patient_id"
        )

        doctor_id = request.form.get(
            "doctor_id"
        )

        diagnosis = request.form.get(
            "diagnosis"
        )

        symptoms = request.form.get(
            "symptoms"
        )

        notes = request.form.get(
            "notes"
        )

        follow_up = request.form.get(
            "follow_up_date"
        )

        if follow_up:

            follow_up_date = datetime.strptime(
                follow_up,
                "%Y-%m-%d"
            ).date()

        else:

            follow_up_date = None

        status = request.form.get(
            "status",
            "Active"
        )

        # Generate Prescription Number

        last = Prescription.query.order_by(
            Prescription.id.desc()
        ).first()

        if last:

            number = last.id + 1

        else:

            number = 1

        prescription_no = f"PRE{number:05d}"

        prescription_data = Prescription(

            prescription_no=prescription_no,

            appointment_id=appointment_id,

            patient_id=patient_id,

            doctor_id=doctor_id,

            diagnosis=diagnosis,

            symptoms=symptoms,

            notes=notes,

            follow_up_date=follow_up_date,

            status=status

        )

        db.session.add(
            prescription_data
        )

        db.session.flush()

        # =====================================
        # Medicine List
        # =====================================

        medicines = request.form.getlist(
            "medicine_name[]"
        )

        dosages = request.form.getlist(
            "dosage[]"
        )

        frequencies = request.form.getlist(
            "frequency[]"
        )

        durations = request.form.getlist(
            "duration[]"
        )

        instructions = request.form.getlist(
            "instructions[]"
        )

        for i in range(len(medicines)):

            if medicines[i].strip() == "":

                continue

            medicine = PrescriptionMedicine(

                prescription_id=prescription_data.id,

                medicine_name=medicines[i],

                dosage=dosages[i],

                frequency=frequencies[i],

                duration=durations[i],

                instructions=instructions[i]

            )

            db.session.add(
                medicine
            )

        db.session.commit()

        flash(
            "Prescription created successfully.",
            "success"
        )

        return redirect(
            url_for(
                "prescription.list_prescriptions"
            )
        )

    return render_template(

        "prescription/add.html",

        appointments=appointments,

        patients=patients,

        doctors=doctors

    )

# =====================================
# Edit Prescription
# =====================================

@prescription.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_prescription(id):

    prescription_data = Prescription.query.get_or_404(id)

    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc()
    ).all()

    patients = Patient.query.order_by(
        Patient.id.desc()
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.id.desc()
    ).all()

    if request.method == "POST":

        prescription_data.appointment_id = request.form.get(
            "appointment_id"
        )

        prescription_data.patient_id = request.form.get(
            "patient_id"
        )

        prescription_data.doctor_id = request.form.get(
            "doctor_id"
        )

        prescription_data.diagnosis = request.form.get(
            "diagnosis"
        )

        prescription_data.symptoms = request.form.get(
            "symptoms"
        )

        prescription_data.notes = request.form.get(
            "notes"
        )

        follow_up = request.form.get(
            "follow_up_date"
        )

        if follow_up:

            prescription_data.follow_up_date = datetime.strptime(
                follow_up,
                "%Y-%m-%d"
            ).date()

        else:

            prescription_data.follow_up_date = None

        prescription_data.status = request.form.get(
            "status"
        )

        # -----------------------------
        # Delete Old Medicines
        # -----------------------------

        PrescriptionMedicine.query.filter_by(
            prescription_id=id
        ).delete()

        medicines = request.form.getlist(
            "medicine_name[]"
        )

        dosages = request.form.getlist(
            "dosage[]"
        )

        frequencies = request.form.getlist(
            "frequency[]"
        )

        durations = request.form.getlist(
            "duration[]"
        )

        instructions = request.form.getlist(
            "instructions[]"
        )

        for i in range(len(medicines)):

            if medicines[i].strip() == "":
                continue

            medicine = PrescriptionMedicine(

                prescription_id=id,

                medicine_name=medicines[i],

                dosage=dosages[i],

                frequency=frequencies[i],

                duration=durations[i],

                instructions=instructions[i]

            )

            db.session.add(
                medicine
            )

        db.session.commit()

        flash(
            "Prescription updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "prescription.list_prescriptions"
            )
        )

    medicines = PrescriptionMedicine.query.filter_by(
        prescription_id=id
    ).all()

    return render_template(
        "prescription/edit.html",
        prescription=prescription_data,
        medicines=medicines,
        appointments=appointments,
        patients=patients,
        doctors=doctors
    )


# =====================================
# Delete Prescription
# =====================================

@prescription.route("/delete/<int:id>")
def delete_prescription(id):

    prescription_data = Prescription.query.get_or_404(id)

    PrescriptionMedicine.query.filter_by(
        prescription_id=id
    ).delete()

    db.session.delete(
        prescription_data
    )

    db.session.commit()

    flash(
        "Prescription deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "prescription.list_prescriptions"
        )
    )


# =====================================
# Change Prescription Status
# =====================================

@prescription.route("/status/<int:id>/<status>")
def change_status(id, status):

    prescription_data = Prescription.query.get_or_404(id)

    allowed = [
        "Active",
        "Completed",
        "Cancelled"
    ]

    if status not in allowed:

        flash(
            "Invalid status.",
            "danger"
        )

        return redirect(
            url_for(
                "prescription.list_prescriptions"
            )
        )

    prescription_data.status = status

    db.session.commit()

    flash(
        "Prescription status updated successfully.",
        "success"
    )

    return redirect(
        url_for(
            "prescription.list_prescriptions"
        )
    )


# =====================================
# Active Prescriptions
# =====================================

@prescription.route("/active")
def active_prescriptions():

    prescriptions = Prescription.query.filter_by(
        status="Active"
    ).order_by(
        Prescription.created_at.desc()
    ).all()

    return render_template(
        "prescription/list.html",
        prescriptions=prescriptions
    )


# =====================================
# Completed Prescriptions
# =====================================

@prescription.route("/completed")
def completed_prescriptions():

    prescriptions = Prescription.query.filter_by(
        status="Completed"
    ).order_by(
        Prescription.created_at.desc()
    ).all()

    return render_template(
        "prescription/list.html",
        prescriptions=prescriptions
    )


# =====================================
# Print Prescription
# =====================================

@prescription.route("/print/<int:id>")
def print_prescription(id):

    prescription_data = Prescription.query.get_or_404(id)

    medicines = PrescriptionMedicine.query.filter_by(
        prescription_id=id
    ).all()

    return render_template(
        "prescription/print.html",
        prescription=prescription_data,
        medicines=medicines
    )