from datetime import datetime

from extensions import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    doctor_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    qualification = db.Column(
        db.String(200),
        nullable=False
    )

    specialization = db.Column(
        db.String(100),
        nullable=False
    )

    experience = db.Column(
        db.Integer,
        default=0
    )

    consultation_fee = db.Column(
        db.Float,
        default=0.0
    )

    address = db.Column(db.Text)

    available_days = db.Column(
        db.String(100)
    )

    available_time = db.Column(
        db.String(100)
    )

    photo = db.Column(
        db.String(255),
        default="default-doctor.png"
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
        back_populates="doctor"
    )

    department = db.relationship(
        "Department",
        back_populates="doctors"
    )

    def __repr__(self):
        return f"<Doctor {self.doctor_code}>"