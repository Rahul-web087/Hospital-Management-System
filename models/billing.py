from datetime import datetime

from extensions import db


# =====================================
# Bill
# =====================================

class Bill(db.Model):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)

    bill_no = db.Column(
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

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=False
    )

    prescription_id = db.Column(
        db.Integer,
        db.ForeignKey("prescriptions.id"),
        nullable=True
    )

    consultation_fee = db.Column(
        db.Float,
        default=0
    )

    medicine_total = db.Column(
        db.Float,
        default=0
    )

    lab_total = db.Column(
        db.Float,
        default=0
    )

    other_charges = db.Column(
        db.Float,
        default=0
    )

    discount = db.Column(
        db.Float,
        default=0
    )

    tax = db.Column(
        db.Float,
        default=0
    )

    grand_total = db.Column(
        db.Float,
        default=0
    )

    payment_method = db.Column(
        db.String(30),
        default="Cash"
    )

    payment_status = db.Column(
        db.String(20),
        default="Pending"
    )

    remarks = db.Column(
        db.Text
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
        backref=db.backref("bills", lazy=True)
    )

    doctor = db.relationship(
        "Doctor",
        backref=db.backref("bills", lazy=True)
    )

    appointment = db.relationship(
        "Appointment",
        backref=db.backref("bills", lazy=True)
    )

    prescription = db.relationship(
        "Prescription",
        backref=db.backref("bills", lazy=True)
    )

    def __repr__(self):
        return f"<Bill {self.bill_no}>"


# =====================================
# Bill Item
# =====================================

class BillItem(db.Model):
    __tablename__ = "bill_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    bill_id = db.Column(
        db.Integer,
        db.ForeignKey("bills.id"),
        nullable=False
    )

    item_name = db.Column(
        db.String(150),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    price = db.Column(
        db.Float,
        default=0
    )

    total = db.Column(
        db.Float,
        default=0
    )

    bill = db.relationship(
        "Bill",
        backref=db.backref(
            "items",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<BillItem {self.item_name}>"