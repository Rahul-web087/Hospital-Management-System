from datetime import datetime
from extensions import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)

    supplier_code = db.Column(db.String(20), unique=True, nullable=False)

    company_name = db.Column(db.String(150), nullable=False)

    contact_person = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    email = db.Column(db.String(120))

    address = db.Column(db.Text)

    gst_number = db.Column(db.String(30))

    status = db.Column(db.String(20), default="Active")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Supplier {self.company_name}>"