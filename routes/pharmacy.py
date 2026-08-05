from datetime import date

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import or_

from extensions import db

from models.medicine import Medicine
from models.medicine_category import MedicineCategory
from models.supplier import Supplier


pharmacy = Blueprint(
    "pharmacy",
    __name__,
    url_prefix="/pharmacy"
)


# ==========================================
# Pharmacy Dashboard
# ==========================================

@pharmacy.route("/dashboard")
@login_required
def dashboard():

    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    total_medicines = Medicine.query.count()

    active_medicines = Medicine.query.filter_by(
        status="Active"
    ).count()

    inactive_medicines = Medicine.query.filter_by(
        status="Inactive"
    ).count()

    low_stock = Medicine.query.filter(
        Medicine.quantity <= Medicine.minimum_stock
    ).count()

    expired = Medicine.query.filter(
        Medicine.expiry_date < date.today()
    ).count()

    categories = MedicineCategory.query.count()

    suppliers = Supplier.query.count()

    medicines = (
        Medicine.query
        .order_by(Medicine.created_at.desc())
        .limit(10)
        .all()
    )

    return render_template(

        "pharmacy/dashboard.html",

        total_medicines=total_medicines,

        active_medicines=active_medicines,

        inactive_medicines=inactive_medicines,

        low_stock=low_stock,

        expired=expired,

        total_categories=categories,

        total_suppliers=suppliers,

        medicines=medicines

    )


# ==========================================
# Medicine List
# ==========================================

@pharmacy.route("/medicines")
@login_required
def list_medicines():

    search = request.args.get(
        "search",
        ""
    ).strip()

    medicines = Medicine.query

    if search:

        medicines = medicines.filter(

            or_(

                Medicine.name.ilike(f"%{search}%"),

                Medicine.medicine_code.ilike(f"%{search}%"),

                Medicine.manufacturer.ilike(f"%{search}%")

            )

        )

    medicines = medicines.order_by(
        Medicine.name.asc()
    ).all()

    return render_template(

        "pharmacy/medicines.html",

        medicines=medicines,

        search=search

    )

# ==========================================
# Add Medicine
# ==========================================

@pharmacy.route("/medicines/add", methods=["GET", "POST"])
@login_required
def add_medicine():

    if not current_user.is_admin:

        flash("Access denied.", "danger")

        return redirect(url_for("auth.login"))

    categories = (
        MedicineCategory.query
        .order_by(MedicineCategory.name.asc())
        .all()
    )

    suppliers = (
        Supplier.query
        .order_by(Supplier.name.asc())
        .all()
    )

    if request.method == "POST":

        medicine_code = request.form.get(
            "medicine_code"
        ).strip()

        existing = Medicine.query.filter_by(
            medicine_code=medicine_code
        ).first()

        if existing:

            flash(
                "Medicine code already exists.",
                "danger"
            )

            return redirect(
                url_for("pharmacy.add_medicine")
            )

        expiry_date = None

        expiry = request.form.get(
            "expiry_date"
        )

        if expiry:

            expiry_date = date.fromisoformat(
                expiry
            )

        medicine = Medicine(

            medicine_code=medicine_code,

            name=request.form.get("name"),

            category_id=request.form.get(
                "category_id"
            ),

            supplier_id=request.form.get(
                "supplier_id"
            ),

            manufacturer=request.form.get(
                "manufacturer"
            ),

            batch_no=request.form.get(
                "batch_no"
            ),

            purchase_price=float(
                request.form.get(
                    "purchase_price"
                ) or 0
            ),

            selling_price=float(
                request.form.get(
                    "selling_price"
                ) or 0
            ),

            quantity=int(
                request.form.get(
                    "quantity"
                ) or 0
            ),

            minimum_stock=int(
                request.form.get(
                    "minimum_stock"
                ) or 10
            ),

            expiry_date=expiry_date,

            status=request.form.get(
                "status"
            )

        )

        db.session.add(medicine)

        db.session.commit()

        flash(
            "Medicine added successfully.",
            "success"
        )

        return redirect(
            url_for(
                "pharmacy.list_medicines"
            )
        )

    return render_template(

        "pharmacy/add_medicine.html",

        categories=categories,

        suppliers=suppliers

    )

# ==========================================
# Edit Medicine
# ==========================================

@pharmacy.route("/medicines/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_medicine(id):

    if not current_user.is_admin:

        flash("Access denied.", "danger")

        return redirect(url_for("auth.login"))

    medicine = Medicine.query.get_or_404(id)

    categories = (
        MedicineCategory.query
        .order_by(MedicineCategory.name.asc())
        .all()
    )

    suppliers = (
        Supplier.query
        .order_by(Supplier.name.asc())
        .all()
    )

    if request.method == "POST":

        medicine_code = request.form.get(
            "medicine_code"
        ).strip()

        existing = Medicine.query.filter(
            Medicine.medicine_code == medicine_code,
            Medicine.id != id
        ).first()

        if existing:

            flash(
                "Medicine code already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "pharmacy.edit_medicine",
                    id=id
                )
            )

        expiry_date = None

        expiry = request.form.get(
            "expiry_date"
        )

        if expiry:

            expiry_date = date.fromisoformat(
                expiry
            )

        medicine.medicine_code = medicine_code

        medicine.name = request.form.get(
            "name"
        )

        medicine.category_id = int(
            request.form.get(
                "category_id"
            )
        )

        medicine.supplier_id = int(
            request.form.get(
                "supplier_id"
            )
        )

        medicine.manufacturer = request.form.get(
            "manufacturer"
        )

        medicine.batch_no = request.form.get(
            "batch_no"
        )

        medicine.purchase_price = float(
            request.form.get(
                "purchase_price"
            ) or 0
        )

        medicine.selling_price = float(
            request.form.get(
                "selling_price"
            ) or 0
        )

        medicine.quantity = int(
            request.form.get(
                "quantity"
            ) or 0
        )

        medicine.minimum_stock = int(
            request.form.get(
                "minimum_stock"
            ) or 10
        )

        medicine.expiry_date = expiry_date

        medicine.status = request.form.get(
            "status"
        )

        db.session.commit()

        flash(
            "Medicine updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "pharmacy.list_medicines"
            )
        )

    return render_template(

        "pharmacy/edit_medicine.html",

        medicine=medicine,

        categories=categories,

        suppliers=suppliers

    )
# ==========================================
# Delete Medicine
# ==========================================

@pharmacy.route("/medicines/delete/<int:id>")
@login_required
def delete_medicine(id):

    if not current_user.is_admin:

        flash("Access denied.", "danger")

        return redirect(url_for("auth.login"))

    medicine = Medicine.query.get_or_404(id)

    db.session.delete(medicine)

    db.session.commit()

    flash(
        "Medicine deleted successfully.",
        "success"
    )

    return redirect(
        url_for("pharmacy.list_medicines")
    )


# ==========================================
# Low Stock Medicines
# ==========================================

@pharmacy.route("/low-stock")
@login_required
def low_stock():

    medicines = (
        Medicine.query
        .filter(
            Medicine.quantity <= Medicine.minimum_stock
        )
        .order_by(Medicine.quantity.asc())
        .all()
    )

    return render_template(
        "pharmacy/medicines.html",
        medicines=medicines,
        page_title="Low Stock Medicines"
    )


# ==========================================
# Expired Medicines
# ==========================================

@pharmacy.route("/expired")
@login_required
def expired():

    medicines = (
        Medicine.query
        .filter(
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date < date.today()
        )
        .order_by(Medicine.expiry_date.asc())
        .all()
    )

    return render_template(
        "pharmacy/medicines.html",
        medicines=medicines,
        page_title="Expired Medicines"
    )


# ==========================================
# Near Expiry Medicines (30 Days)
# ==========================================

@pharmacy.route("/near-expiry")
@login_required
def near_expiry():

    from datetime import timedelta

    today = date.today()

    end_date = today + timedelta(days=30)

    medicines = (
        Medicine.query
        .filter(
            Medicine.expiry_date.isnot(None),
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= end_date
        )
        .order_by(Medicine.expiry_date.asc())
        .all()
    )

    return render_template(
        "pharmacy/medicines.html",
        medicines=medicines,
        page_title="Near Expiry Medicines"
    )


# ==========================================
# Active Medicines
# ==========================================

@pharmacy.route("/active")
@login_required
def active_medicines():

    medicines = (
        Medicine.query
        .filter_by(status="Active")
        .order_by(Medicine.name.asc())
        .all()
    )

    return render_template(
        "pharmacy/medicines.html",
        medicines=medicines,
        page_title="Active Medicines"
    )


# ==========================================
# Inactive Medicines
# ==========================================

@pharmacy.route("/inactive")
@login_required
def inactive_medicines():

    medicines = (
        Medicine.query
        .filter_by(status="Inactive")
        .order_by(Medicine.name.asc())
        .all()
    )

    return render_template(
        "pharmacy/medicines.html",
        medicines=medicines,
        page_title="Inactive Medicines"
    )