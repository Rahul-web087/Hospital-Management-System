from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    # ===============================
    # Role Constants
    # ===============================
    ROLE_ADMIN = "admin"
    ROLE_DOCTOR = "doctor"
    ROLE_PATIENT = "patient"
    ROLE_RECEPTIONIST = "receptionist"
    ROLE_PHARMACIST = "pharmacist"
    ROLE_LAB = "lab"
    ROLE_ACCOUNTANT = "accountant"

    ROLES = [
        ROLE_ADMIN,
        ROLE_DOCTOR,
        ROLE_PATIENT,
        ROLE_RECEPTIONIST,
        ROLE_PHARMACIST,
        ROLE_LAB,
        ROLE_ACCOUNTANT
    ]

    # ===============================
    # Columns
    # ===============================
    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.String(20),
        nullable=False,
        default=ROLE_PATIENT
    )

    phone = db.Column(db.String(15))

    gender = db.Column(db.String(20))

    date_of_birth = db.Column(db.Date)

    address = db.Column(db.Text)

    profile_image = db.Column(
        db.String(255),
        default="default.png"
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    is_verified = db.Column(
        db.Boolean,
        default=False
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

    # ===============================
    # Relationships
    # ===============================
    doctor = db.relationship(
        "Doctor",
        back_populates="user",
        uselist=False
    )

    patient = db.relationship(
        "Patient",
        back_populates="user",
        uselist=False
    )

    # ===============================
    # Password Methods
    # ===============================
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    # ===============================
    # Role Helpers
    # ===============================
    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_doctor(self):
        return self.role == self.ROLE_DOCTOR

    @property
    def is_patient(self):
        return self.role == self.ROLE_PATIENT

    @property
    def is_receptionist(self):
        return self.role == self.ROLE_RECEPTIONIST

    @property
    def is_pharmacist(self):
        return self.role == self.ROLE_PHARMACIST

    @property
    def is_lab(self):
        return self.role == self.ROLE_LAB

    @property
    def is_accountant(self):
        return self.role == self.ROLE_ACCOUNTANT

    def has_role(self, *roles):
        return self.role in roles

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"