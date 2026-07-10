from datetime import datetime

from extensions import db


# =====================================
# Prescription
# =====================================

class Prescription(db.Model):
    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)

    prescription_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=False
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    diagnosis = db.Column(
        db.Text,
        nullable=False
    )

    symptoms = db.Column(
        db.Text
    )

    notes = db.Column(
        db.Text
    )

    follow_up_date = db.Column(
        db.Date
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships

    appointment = db.relationship(
        "Appointment",
        backref=db.backref(
            "prescriptions",
            lazy=True
        )
    )

    patient = db.relationship(
        "Patient",
        backref=db.backref(
            "prescriptions",
            lazy=True
        )
    )

    doctor = db.relationship(
        "Doctor",
        backref=db.backref(
            "prescriptions",
            lazy=True
        )
    )

    def __repr__(self):
        return f"<Prescription {self.prescription_no}>"


# =====================================
# Prescription Medicine
# =====================================

class PrescriptionMedicine(db.Model):
    __tablename__ = "prescription_medicines"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    prescription_id = db.Column(
        db.Integer,
        db.ForeignKey("prescriptions.id"),
        nullable=False
    )

    medicine_name = db.Column(
        db.String(150),
        nullable=False
    )

    dosage = db.Column(
        db.String(100)
    )

    frequency = db.Column(
        db.String(100)
    )

    duration = db.Column(
        db.String(100)
    )

    instructions = db.Column(
        db.Text
    )

    prescription = db.relationship(
        "Prescription",
        backref=db.backref(
            "medicines",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<Medicine {self.medicine_name}>"