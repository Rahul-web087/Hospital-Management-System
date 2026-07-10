from datetime import datetime

from extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    appointment_no = db.Column(
        db.String(20),
        unique=True,
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

    appointment_date = db.Column(
        db.Date,
        nullable=False
    )

    appointment_time = db.Column(
        db.Time,
        nullable=False
    )
    visit_type = db.Column(
        db.String(30),
        default="OPD"
    )

    token_number = db.Column(
        db.Integer
    )

    fee = db.Column(
        db.Float,
        default=0
    )

    reason = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )

    remarks = db.Column(
        db.Text,
        nullable=True
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
    patient = db.relationship(
        "Patient",
        backref=db.backref("appointments", lazy=True)
    )

    doctor = db.relationship(
        "Doctor",
        backref=db.backref("appointments", lazy=True)
    )

    def __repr__(self):
        return (
            f"<Appointment {self.appointment_no} - "
            f"{self.patient_id} -> {self.doctor_id}>"
        )