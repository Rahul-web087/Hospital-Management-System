from datetime import datetime

from extensions import db


class MedicineCategory(db.Model):

    __tablename__ = "medicine_categories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text
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

    medicines = db.relationship(
        "Medicine",
        back_populates="category",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<MedicineCategory {self.name}>"