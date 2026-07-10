import os
from uuid import uuid4
from datetime import datetime

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
from models.user import User
from models.patient import Patient


patient = Blueprint(
    "patient",
    __name__,
    url_prefix="/patients"
)


# =====================================
# Patient List
# =====================================

@patient.route("/")
def list_patients():

    patients = Patient.query.order_by(
        Patient.id.desc()
    ).all()

    return render_template(
        "patient/list.html",
        patients=patients
    )


# =====================================
# Patient Profile
# =====================================

@patient.route("/profile/<int:id>")
def profile(id):

    patient_data = Patient.query.get_or_404(id)

    return render_template(
        "patient/profile.html",
        patient=patient_data
    )


# =====================================
# Add Patient
# =====================================

@patient.route("/add", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        gender = request.form.get("gender")
        dob = request.form.get("date_of_birth")

        if dob:
            date_of_birth = datetime.strptime(
                dob,
                "%Y-%m-%d"
            ).date()
        else:
            date_of_birth = None
        address = request.form.get("address")

        blood_group = request.form.get("blood_group")
        emergency_contact = request.form.get("emergency_contact")
        emergency_phone = request.form.get("emergency_phone")
        medical_history = request.form.get("medical_history")
        allergies = request.form.get("allergies")
        insurance_provider = request.form.get("insurance_provider")
        insurance_number = request.form.get("insurance_number")

        status = request.form.get("status") == "1"

        if User.query.filter_by(email=email).first():

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("patient.add_patient")
            )

        photo = "default-patient.png"

        file = request.files.get("photo")

        if file and file.filename:

            filename = secure_filename(file.filename)

            extension = filename.rsplit(".", 1)[1].lower()

            filename = f"{uuid4().hex}.{extension}"

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "patients"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            file.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

            photo = filename

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            gender=gender,
            date_of_birth=date_of_birth,
            address=address,
            role="patient"
        )

        user.set_password("patient123")

        db.session.add(user)
        db.session.flush()

        patient_data = Patient(
            user_id=user.id,
            patient_code=f"PAT{user.id:05d}",
            blood_group=blood_group,
            emergency_contact=emergency_contact,
            emergency_phone=emergency_phone,
            medical_history=medical_history,
            allergies=allergies,
            insurance_provider=insurance_provider,
            insurance_number=insurance_number,
            photo=photo,
            status=status
        )

        db.session.add(patient_data)
        db.session.commit()

        flash(
            "Patient added successfully.",
            "success"
        )

        return redirect(
            url_for("patient.list_patients")
        )

    return render_template(
        "patient/add.html"
    )


# =====================================
# Edit Patient
# =====================================

@patient.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):

    patient_data = Patient.query.get_or_404(id)

    if request.method == "POST":

        email = request.form.get("email")

        existing_user = User.query.filter(
            User.email == email,
            User.id != patient_data.user.id
        ).first()

        if existing_user:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "patient.edit_patient",
                    id=id
                )
            )


        # --------------------
        # Update User
        # --------------------

        patient_data.user.full_name = request.form.get(
            "full_name"
        )

        patient_data.user.email = email

        patient_data.user.phone = request.form.get(
            "phone"
        )

        patient_data.user.gender = request.form.get(
            "gender"
        )

        patient_data.user.address = request.form.get(
            "address"
        )

        # Convert string to Python date object
        dob = request.form.get("date_of_birth")

        if dob:
            patient_data.user.date_of_birth = datetime.strptime(
                dob,
                "%Y-%m-%d"
            ).date()
        else:
            patient_data.user.date_of_birth = None

        # --------------------
        # Update Patient
        # --------------------

        patient_data.blood_group = request.form.get(
            "blood_group"
        )

        patient_data.emergency_contact = request.form.get(
            "emergency_contact"
        )

        patient_data.emergency_phone = request.form.get(
            "emergency_phone"
        )

        patient_data.medical_history = request.form.get(
            "medical_history"
        )

        patient_data.allergies = request.form.get(
            "allergies"
        )

        patient_data.insurance_provider = request.form.get(
            "insurance_provider"
        )

        patient_data.insurance_number = request.form.get(
            "insurance_number"
        )

        patient_data.status = (
            request.form.get("status") == "1"
        )

        # --------------------
        # Upload New Photo
        # --------------------

        file = request.files.get("photo")

        if file and file.filename:

            filename = secure_filename(
                file.filename
            )

            extension = filename.rsplit(
                ".",
                1
            )[1].lower()

            filename = f"{uuid4().hex}.{extension}"

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "patients"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            if patient_data.photo != "default-patient.png":

                old_photo = os.path.join(
                    upload_folder,
                    patient_data.photo
                )

                if os.path.exists(old_photo):
                    os.remove(old_photo)

            file.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

            patient_data.photo = filename

        db.session.commit()

        flash(
            "Patient updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "patient.list_patients"
            )
        )

    return render_template(
        "patient/edit.html",
        patient=patient_data
    )


# =====================================
# Delete Patient
# =====================================

@patient.route("/delete/<int:id>")
def delete_patient(id):

    patient_data = Patient.query.get_or_404(id)

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "patients"
    )

    # Delete patient photo
    if (
        patient_data.photo
        and patient_data.photo != "default-patient.png"
    ):

        photo_path = os.path.join(
            upload_folder,
            patient_data.photo
        )

        if os.path.exists(photo_path):
            os.remove(photo_path)

    # Delete linked user
    user = patient_data.user

    db.session.delete(patient_data)

    if user:
        db.session.delete(user)

    db.session.commit()

    flash(
        "Patient deleted successfully.",
        "success"
    )

    return redirect(
        url_for("patient.list_patients")
    )


# =====================================
# Patient Dashboard
# =====================================

@patient.route("/dashboard")
def dashboard():

    patient = Patient.query.first()

    if not patient:
        flash("No patient found.", "warning")
        return redirect(url_for("patient.list_patients"))

    return render_template(
        "patient/dashboard.html",
        patient=patient,
        appointments=[],
        prescriptions=[],
        total_appointments=0,
        total_prescriptions=0,
        total_reports=0,
        total_bills=0
    )


# =====================================
# Toggle Patient Status
# =====================================

@patient.route("/status/<int:id>")
def toggle_status(id):

    patient_data = Patient.query.get_or_404(id)

    patient_data.status = not patient_data.status

    db.session.commit()

    flash(
        "Patient status updated successfully.",
        "success"
    )

    return redirect(
        url_for("patient.list_patients")
    )


# dumy route


@patient.route("/appointments")
def appointments():
    return "<h2>Appointments Page - Coming Soon</h2>"


@patient.route("/book-appointment")
def book_appointment():
    return "<h2>Book Appointment - Coming Soon</h2>"


@patient.route("/prescriptions")
def prescriptions():
    return "<h2>Prescriptions - Coming Soon</h2>"


@patient.route("/reports")
def reports():
    return "<h2>Reports - Coming Soon</h2>"


@patient.route("/bills")
def bills():
    return "<h2>Bills - Coming Soon</h2>"


@patient.route("/chatbot")
def chatbot():
    return "<h2>AI Chatbot - Coming Soon</h2>"