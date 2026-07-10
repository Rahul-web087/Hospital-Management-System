from datetime import datetime

from extensions import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    patient_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    blood_group = db.Column(
        db.String(10)
    )

    emergency_contact = db.Column(
        db.String(100)
    )

    emergency_phone = db.Column(
        db.String(20)
    )

    medical_history = db.Column(
        db.Text
    )

    allergies = db.Column(
        db.Text
    )

    insurance_provider = db.Column(
        db.String(100)
    )

    insurance_number = db.Column(
        db.String(100)
    )

    photo = db.Column(
        db.String(255),
        default="default-patient.png"
    )

    status = db.Column(
        db.Boolean,
        default=True
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

    user = db.relationship(
        "User",
        back_populates="patient"
    )

    def __repr__(self):
        return f"<Patient {self.patient_code}>"