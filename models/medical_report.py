from datetime import datetime

from extensions import db


class MedicalReport(db.Model):
    __tablename__ = "medical_reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    report_no = db.Column(
        db.String(30),
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

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=False
    )

    report_type = db.Column(
        db.String(100),
        nullable=False
    )

    report_date = db.Column(
        db.Date,
        nullable=False
    )

    report_file = db.Column(
        db.String(255)
    )

    findings = db.Column(
        db.Text
    )

    diagnosis = db.Column(
        db.Text
    )

    remarks = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        default="Pending"
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

    # ==========================
    # Relationships
    # ==========================

    patient = db.relationship(
        "Patient",
        backref="medical_reports"
    )

    doctor = db.relationship(
        "Doctor",
        backref="medical_reports"
    )

    appointment = db.relationship(
        "Appointment",
        backref="medical_reports"
    )

    def __repr__(self):
        return f"<MedicalReport {self.report_no}>"