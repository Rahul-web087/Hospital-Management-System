import os
from uuid import uuid4

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
from models.doctor import Doctor
from models.department import Department


doctor = Blueprint(
    "doctor",
    __name__,
    url_prefix="/doctors"
)


# ==========================
# Doctor List
# ==========================

@doctor.route("/")
def list_doctors():

    doctors = Doctor.query.order_by(
        Doctor.id.desc()
    ).all()

    return render_template(
        "doctor/list.html",
        doctors=doctors
    )


# ==========================
# Doctor Profile
# ==========================

@doctor.route("/profile/<int:id>")
def profile(id):

    doctor_data = Doctor.query.get_or_404(id)

    return render_template(
        "doctor/profile.html",
        doctor=doctor_data
    )


# ==========================
# Add Doctor
# ==========================

@doctor.route("/add", methods=["GET", "POST"])
def add_doctor():

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        department_id = int(request.form.get("department_id"))
        qualification = request.form.get("qualification")
        specialization = request.form.get("specialization")
        experience = int(request.form.get("experience"))
        consultation_fee = float(request.form.get("consultation_fee"))
        available_days = request.form.get("available_days")
        available_time = request.form.get("available_time")
        address = request.form.get("address")
        status = request.form.get("status") == "1"

        if User.query.filter_by(email=email).first():

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("doctor.add_doctor")
            )

        photo = "default-doctor.png"

        file = request.files.get("photo")

        if file and file.filename:

            filename = secure_filename(file.filename)

            extension = filename.rsplit(".", 1)[1].lower()

            filename = f"{uuid4().hex}.{extension}"

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "doctors"
            )

            os.makedirs(upload_folder, exist_ok=True)

            file.save(
                os.path.join(upload_folder, filename)
            )

            photo = filename

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            role="doctor"
        )

        user.set_password("doctor123")

        db.session.add(user)
        db.session.flush()

        doctor_data = Doctor(
            user_id=user.id,
            department_id=department_id,
            doctor_code=f"DOC{user.id:04d}",
            qualification=qualification,
            specialization=specialization,
            experience=experience,
            consultation_fee=consultation_fee,
            available_days=available_days,
            available_time=available_time,
            address=address,
            photo=photo,
            status=status
        )

        db.session.add(doctor_data)
        db.session.commit()

        flash(
            "Doctor added successfully.",
            "success"
        )

        return redirect(
            url_for("doctor.list_doctors")
        )

    return render_template(
        "doctor/add.html",
        departments=departments
    )

# ==========================
# Edit Doctor
# ==========================

@doctor.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):

    doctor_data = Doctor.query.get_or_404(id)

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    if request.method == "POST":

        email = request.form.get("email")

        existing_user = User.query.filter(
            User.email == email,
            User.id != doctor_data.user.id
        ).first()

        if existing_user:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "doctor.edit_doctor",
                    id=id
                )
            )

        # Update User
        doctor_data.user.full_name = request.form.get("full_name")
        doctor_data.user.email = email
        doctor_data.user.phone = request.form.get("phone")

        # Update Doctor
        doctor_data.department_id = int(
            request.form.get("department_id")
        )

        doctor_data.qualification = request.form.get(
            "qualification"
        )

        doctor_data.specialization = request.form.get(
            "specialization"
        )

        doctor_data.experience = int(
            request.form.get("experience")
        )

        doctor_data.consultation_fee = float(
            request.form.get("consultation_fee")
        )

        doctor_data.available_days = request.form.get(
            "available_days"
        )

        doctor_data.available_time = request.form.get(
            "available_time"
        )

        doctor_data.address = request.form.get(
            "address"
        )

        doctor_data.status = (
            request.form.get("status") == "1"
        )

        file = request.files.get("photo")

        if file and file.filename:

            filename = secure_filename(file.filename)

            extension = filename.rsplit(".", 1)[1].lower()

            filename = f"{uuid4().hex}.{extension}"

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "doctors"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            if doctor_data.photo != "default-doctor.png":

                old_photo = os.path.join(
                    upload_folder,
                    doctor_data.photo
                )

                if os.path.exists(old_photo):

                    os.remove(old_photo)

            file.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

            doctor_data.photo = filename

        db.session.commit()

        flash(
            "Doctor updated successfully.",
            "success"
        )

        return redirect(
            url_for("doctor.list_doctors")
        )

    return render_template(
        "doctor/edit.html",
        doctor=doctor_data,
        departments=departments
    )

# ==========================
# Delete Doctor
# ==========================

@doctor.route("/delete/<int:id>")
def delete_doctor(id):

    doctor_data = Doctor.query.get_or_404(id)

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "doctors"
    )

    # Delete doctor's photo
    if doctor_data.photo and doctor_data.photo != "default-doctor.png":

        photo_path = os.path.join(
            upload_folder,
            doctor_data.photo
        )

        if os.path.exists(photo_path):
            os.remove(photo_path)

    # Delete linked user
    user = doctor_data.user

    db.session.delete(doctor_data)

    if user:
        db.session.delete(user)

    db.session.commit()

    flash(
        "Doctor deleted successfully.",
        "success"
    )

    return redirect(
        url_for("doctor.list_doctors")
    )


# ==========================
# Optional: Toggle Status
# ==========================

@doctor.route("/status/<int:id>")
def toggle_status(id):

    doctor_data = Doctor.query.get_or_404(id)

    doctor_data.status = not doctor_data.status

    db.session.commit()

    flash(
        "Doctor status updated successfully.",
        "success"
    )

    return redirect(
        url_for("doctor.list_doctors")
    )