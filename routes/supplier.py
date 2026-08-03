from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.supplier import Supplier
from sqlalchemy import or_

supplier = Blueprint(
    "supplier",
    __name__,
    url_prefix="/supplier"
)


# =====================================
# Supplier Dashboard
# =====================================
@supplier.route("/dashboard")
@login_required
def dashboard():

    if not (current_user.is_admin or current_user.is_pharmacist):
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    total_suppliers = Supplier.query.count()

    active_suppliers = Supplier.query.filter_by(
        status="Active"
    ).count()

    inactive_suppliers = Supplier.query.filter_by(
        status="Inactive"
    ).count()

    recent_suppliers = Supplier.query.order_by(
        Supplier.created_at.desc()
    ).limit(10).all()

    return render_template(
        "supplier/dashboard.html",
        total_suppliers=total_suppliers,
        active_suppliers=active_suppliers,
        inactive_suppliers=inactive_suppliers,
        recent_suppliers=recent_suppliers
    )





# Supplier List

@supplier.route("/")
@login_required
def list_suppliers():

    search = request.args.get("search", "").strip()

    query = Supplier.query

    if search:

        query = query.filter(

            or_(

                Supplier.company_name.ilike(f"%{search}%"),

                Supplier.contact_person.ilike(f"%{search}%"),

                Supplier.phone.ilike(f"%{search}%"),

                Supplier.email.ilike(f"%{search}%"),

                Supplier.supplier_code.ilike(f"%{search}%")

            )

        )

    suppliers = query.order_by(
        Supplier.company_name.asc()
    ).all()

    return render_template(
        "supplier/list.html",
        suppliers=suppliers
    )


# =====================================
# Add Supplier
# =====================================
@supplier.route("/add", methods=["GET", "POST"])
@login_required
def add_supplier():

    if request.method == "POST":

        existing = Supplier.query.filter_by(
            supplier_code=request.form["supplier_code"]
        ).first()

        if existing:
            flash("Supplier Code already exists.", "danger")
            return redirect(url_for("supplier.add_supplier"))

        supplier_obj = Supplier(
            supplier_code=request.form["supplier_code"],
            company_name=request.form["company_name"],
            contact_person=request.form["contact_person"],
            phone=request.form["phone"],
            email=request.form["email"],
            address=request.form["address"],
            gst_number=request.form["gst_number"],
            status=request.form["status"]
        )

        db.session.add(supplier_obj)
        db.session.commit()

        flash("Supplier added successfully.", "success")

        return redirect(url_for("supplier.list_suppliers"))

    return render_template("supplier/add.html")


# =====================================
# Edit Supplier
# =====================================
@supplier.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    if request.method == "POST":

        supplier.company_name = request.form["company_name"]
        supplier.contact_person = request.form["contact_person"]
        supplier.phone = request.form["phone"]
        supplier.email = request.form["email"]
        supplier.address = request.form["address"]
        supplier.gst_number = request.form["gst_number"]
        supplier.status = request.form["status"]

        db.session.commit()

        flash("Supplier updated successfully.", "success")

        return redirect(url_for("supplier.list_suppliers"))

    return render_template(
        "supplier/edit.html",
        supplier=supplier
    )

# =====================================
# Delete Supplier
# =====================================
@supplier.route("/delete/<int:id>")
@login_required
def delete_supplier(id):

    supplier_obj = Supplier.query.get_or_404(id)

    db.session.delete(supplier_obj)
    db.session.commit()

    flash("Supplier deleted successfully.", "success")

    return redirect(url_for("supplier.list_suppliers"))


# =====================================
# Toggle Supplier Status
# =====================================
@supplier.route("/toggle-status/<int:id>")
@login_required
def toggle_status(id):

    supplier_obj = Supplier.query.get_or_404(id)

    if supplier_obj.status == "Active":
        supplier_obj.status = "Inactive"
    else:
        supplier_obj.status = "Active"

    db.session.commit()

    flash("Supplier status updated.", "success")

    return redirect(url_for("supplier.list_suppliers"))