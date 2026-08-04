from datetime import datetime

from extensions import db


class Medicine(db.Model):

    __tablename__ = "medicines"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    medicine_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    generic_name = db.Column(
        db.String(150)
    )

    # ==========================
    # Category
    # ==========================

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("medicine_categories.id"),
        nullable=False
    )

    category = db.relationship(
        "MedicineCategory",
        back_populates="medicines"
    )

    # ==========================
    # Supplier
    # ==========================

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id"),
        nullable=True
    )

    supplier = db.relationship(
        "Supplier",
        backref="medicines"
    )

    # ==========================
    # Medicine Details
    # ==========================

    manufacturer = db.Column(
        db.String(150)
    )

    batch_no = db.Column(
        db.String(50)
    )

    purchase_price = db.Column(
        db.Float,
        default=0
    )

    selling_price = db.Column(
        db.Float,
        default=0
    )

    quantity = db.Column(
        db.Integer,
        default=0
    )

    minimum_stock = db.Column(
        db.Integer,
        default=10
    )

    expiry_date = db.Column(
        db.Date
    )

    description = db.Column(
        db.Text
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

    def __repr__(self):
        return f"<Medicine {self.name}>"