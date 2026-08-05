from extensions import db


class PurchaseItem(db.Model):

    __tablename__ = "purchase_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    purchase_id = db.Column(
        db.Integer,
        db.ForeignKey("purchases.id"),
        nullable=False
    )

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicines.id"),
        nullable=False
    )

    medicine = db.relationship(
        "Medicine"
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    purchase_price = db.Column(
        db.Float,
        nullable=False
    )

    total = db.Column(
        db.Float,
        default=0
    )