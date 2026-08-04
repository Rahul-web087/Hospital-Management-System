from datetime import datetime

from extensions import db


class Purchase(db.Model):

    __tablename__ = "purchases"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    purchase_no = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id"),
        nullable=False
    )

    purchase_date = db.Column(
        db.Date,
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="Completed"
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

    def __repr__(self):
        return f"<Purchase {self.purchase_no}>"