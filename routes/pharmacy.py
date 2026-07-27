from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from sqlalchemy import or_

from extensions import db
from models.medicine import Medicine

pharmacy = Blueprint(
    "pharmacy",
    __name__,
    url_prefix="/pharmacy"
)


# =====================================
# Dashboard
# =====================================
@pharmacy.route("/dashboard")
@login_required
def dashboard():

    if not (current_user.is_admin or current_user.is_pharmacist):
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    total_medicines = Medicine.query.count()

    active_medicines = Medicine.query.filter_by(
        status="Active"
    ).count()

    low_stock = Medicine.query.filter(
        Medicine.quantity <= Medicine.minimum_stock
    ).count()

    expired = Medicine.query.filter(
        Medicine.expiry_date < date.today()
    ).count()

    medicines = Medicine.query.order_by(
        Medicine.created_at.desc()
    ).limit(10).all()

    return render_template(
        "pharmacy/dashboard.html",
        total_medicines=total_medicines,
        active_medicines=active_medicines,
        low_stock=low_stock,
        expired=expired,
        medicines=medicines
    )



# =====================================
# Medicine List
# =====================================
@pharmacy.route("/medicines")
@login_required
def list_medicines():

    search = request.args.get("search", "").strip()

    query = Medicine.query

    if search:
        query = query.filter(
            or_(
                Medicine.name.ilike(f"%{search}%"),
                Medicine.medicine_code.ilike(f"%{search}%"),
                Medicine.category.ilike(f"%{search}%"),
                Medicine.manufacturer.ilike(f"%{search}%")
            )
        )

    medicines = query.order_by(
        Medicine.name.asc()
    ).all()

    return render_template(
        "pharmacy/medicines.html",
        medicines=medicines
    )


# =====================================
# Add Medicine
# =====================================
@pharmacy.route("/add", methods=["GET", "POST"])
@login_required
def add_medicine():

    if request.method == "POST":

        # Check duplicate medicine code
        existing = Medicine.query.filter_by(
            medicine_code=request.form["medicine_code"]
        ).first()

        if existing:
            flash("Medicine Code already exists.", "danger")
            return redirect(url_for("pharmacy.add_medicine"))

        medicine = Medicine(

            medicine_code=request.form["medicine_code"],

            name=request.form["name"],

            category=request.form["category"],

            manufacturer=request.form["manufacturer"],

            batch_no=request.form["batch_no"],

            purchase_price=float(request.form["purchase_price"]),

            selling_price=float(request.form["selling_price"]),

            quantity=int(request.form["quantity"]),

            minimum_stock=int(request.form["minimum_stock"]),

            expiry_date=request.form["expiry_date"],

            status=request.form["status"]
        )

        db.session.add(medicine)
        db.session.commit()

        flash("Medicine added successfully.", "success")

        return redirect(url_for("pharmacy.list_medicines"))

    return render_template("pharmacy/add_medicine.html")


# =====================================
# Edit Medicine
# =====================================
@pharmacy.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_medicine(id):

    medicine = Medicine.query.get_or_404(id)

    if request.method == "POST":

        medicine.name = request.form["name"]
        medicine.category = request.form["category"]
        medicine.manufacturer = request.form["manufacturer"]
        medicine.batch_no = request.form["batch_no"]

        medicine.purchase_price = float(request.form["purchase_price"])
        medicine.selling_price = float(request.form["selling_price"])

        medicine.quantity = int(request.form["quantity"])
        medicine.minimum_stock = int(request.form["minimum_stock"])

        medicine.expiry_date = request.form["expiry_date"]
        medicine.status = request.form["status"]

        db.session.commit()

        flash("Medicine updated successfully.", "success")

        return redirect(url_for("pharmacy.list_medicines"))

    return render_template(
        "pharmacy/edit_medicine.html",
        medicine=medicine
    )

# =====================================
# Delete Medicine
# =====================================
@pharmacy.route("/delete/<int:id>")
@login_required
def delete_medicine(id):

    medicine = Medicine.query.get_or_404(id)

    db.session.delete(medicine)
    db.session.commit()

    flash("Medicine deleted successfully.", "success")

    return redirect(url_for("pharmacy.list_medicines"))


# =====================================
# Low Stock Medicines
# =====================================
@pharmacy.route("/low-stock")
@login_required
def low_stock():

    medicines = Medicine.query.filter(
        Medicine.quantity <= Medicine.minimum_stock
    ).all()

    return render_template(
        "pharmacy/medicines.html",
        medicines=medicines
    )


# =====================================
# Expired Medicines
# =====================================
@pharmacy.route("/expired")
@login_required
def expired():

    medicines = Medicine.query.filter(
        Medicine.expiry_date < date.today()
    ).all()

    return render_template(
        "pharmacy/medicines.html",
        medicines=medicines
    )