from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from extensions import db

from models.purchase import Purchase
from models.purchase_item import PurchaseItem
from models.supplier import Supplier
from models.medicine import Medicine


purchase = Blueprint(
    "purchase",
    __name__,
    url_prefix="/purchases"
)


# =====================================
# Purchase List
# =====================================

@purchase.route("/")
def list_purchases():

    purchases = Purchase.query.order_by(
        Purchase.id.desc()
    ).all()

    return render_template(
        "purchase/list.html",
        purchases=purchases
    )


# =====================================
# Purchase Details
# =====================================

@purchase.route("/view/<int:id>")
def view_purchase(id):

    purchase_data = Purchase.query.get_or_404(id)

    items = PurchaseItem.query.filter_by(
        purchase_id=id
    ).all()

    return render_template(
        "purchase/view.html",
        purchase=purchase_data,
        items=items
    )

# =====================================
# Add Purchase
# =====================================

@purchase.route("/add", methods=["GET", "POST"])
def add_purchase():

    suppliers = Supplier.query.order_by(
        Supplier.name.asc()
    ).all()

    medicines = Medicine.query.order_by(
        Medicine.name.asc()
    ).all()

    if request.method == "POST":

        supplier_id = request.form.get("supplier_id")

        invoice_no = request.form.get("invoice_no")

        purchase_date = datetime.strptime(
            request.form.get("purchase_date"),
            "%Y-%m-%d"
        ).date()

        discount = float(
            request.form.get("discount") or 0
        )

        tax = float(
            request.form.get("tax") or 0
        )

        remarks = request.form.get("remarks")

        payment_status = request.form.get(
            "payment_status",
            "Pending"
        )

        # --------------------------
        # Generate Purchase Number
        # --------------------------

        last = Purchase.query.order_by(
            Purchase.id.desc()
        ).first()

        if last:
            number = last.id + 1
        else:
            number = 1

        purchase_no = f"PUR{number:05d}"

        purchase = Purchase(

            purchase_no=purchase_no,

            supplier_id=supplier_id,

            invoice_no=invoice_no,

            purchase_date=purchase_date,

            subtotal=0,

            discount=discount,

            tax=tax,

            grand_total=0,

            payment_status=payment_status,

            remarks=remarks

        )

        db.session.add(purchase)

        db.session.flush()

        subtotal = 0

        medicine_ids = request.form.getlist(
            "medicine_id[]"
        )

        quantities = request.form.getlist(
            "quantity[]"
        )

        prices = request.form.getlist(
            "purchase_price[]"
        )

        # --------------------------
        # Purchase Items
        # --------------------------

        for i in range(len(medicine_ids)):

            medicine = Medicine.query.get(
                int(medicine_ids[i])
            )

            quantity = int(
                quantities[i]
            )

            price = float(
                prices[i]
            )

            total = quantity * price

            subtotal += total

            item = PurchaseItem(

                purchase_id=purchase.id,

                medicine_id=medicine.id,

                quantity=quantity,

                purchase_price=price,

                total=total

            )

            db.session.add(item)

            # ----------------------
            # Update Stock
            # ----------------------

            medicine.quantity += quantity

            medicine.purchase_price = price

        purchase.subtotal = subtotal

        purchase.grand_total = (
            subtotal
            - discount
            + tax
        )

        db.session.commit()

        flash(
            "Purchase added successfully.",
            "success"
        )

        return redirect(
            url_for(
                "purchase.list_purchases"
            )
        )

    return render_template(

        "purchase/add.html",

        suppliers=suppliers,

        medicines=medicines

    )



# =====================================
# Edit Purchase
# =====================================

@purchase.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_purchase():

    purchase_data = Purchase.query.get_or_404(id)

    suppliers = Supplier.query.order_by(
        Supplier.name.asc()
    ).all()

    medicines = Medicine.query.order_by(
        Medicine.name.asc()
    ).all()

    items = PurchaseItem.query.filter_by(
        purchase_id=id
    ).all()

    if request.method == "POST":

        purchase_data.supplier_id = request.form.get(
            "supplier_id"
        )

        purchase_data.invoice_no = request.form.get(
            "invoice_no"
        )

        purchase_data.purchase_date = datetime.strptime(
            request.form.get("purchase_date"),
            "%Y-%m-%d"
        ).date()

        purchase_data.discount = float(
            request.form.get("discount") or 0
        )

        purchase_data.tax = float(
            request.form.get("tax") or 0
        )

        purchase_data.payment_status = request.form.get(
            "payment_status"
        )

        purchase_data.remarks = request.form.get(
            "remarks"
        )

        db.session.commit()

        flash(
            "Purchase updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "purchase.list_purchases"
            )
        )

    return render_template(

        "purchase/edit.html",

        purchase=purchase_data,

        suppliers=suppliers,

        medicines=medicines,

        items=items

    )


# =====================================
# Delete Purchase
# =====================================

@purchase.route("/delete/<int:id>")
def delete_purchase():

    purchase_data = Purchase.query.get_or_404(id)

    items = PurchaseItem.query.filter_by(
        purchase_id=id
    ).all()

    # Restore Stock
    for item in items:

        medicine = Medicine.query.get(
            item.medicine_id
        )

        if medicine:
            medicine.quantity -= item.quantity

        db.session.delete(item)

    db.session.delete(
        purchase_data
    )

    db.session.commit()

    flash(
        "Purchase deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "purchase.list_purchases"
        )
    )


# =====================================
# Print Purchase
# =====================================

@purchase.route("/print/<int:id>")
def print_purchase():

    purchase_data = Purchase.query.get_or_404(id)

    items = PurchaseItem.query.filter_by(
        purchase_id=id
    ).all()

    return render_template(

        "purchase/print.html",

        purchase=purchase_data,

        items=items

    )


# =====================================
# Payment Status
# =====================================

@purchase.route("/payment/<int:id>/<status>")
def payment_status(id, status):

    purchase_data = Purchase.query.get_or_404(id)

    allowed = [

        "Pending",

        "Paid",

        "Partial"

    ]

    if status not in allowed:

        flash(
            "Invalid payment status.",
            "danger"
        )

        return redirect(
            url_for(
                "purchase.list_purchases"
            )
        )

    purchase_data.payment_status = status

    db.session.commit()

    flash(
        "Payment status updated.",
        "success"
    )

    return redirect(
        url_for(
            "purchase.list_purchases"
        )
    )


# =====================================
# Today's Purchases
# =====================================

@purchase.route("/today")
def today_purchases():

    today = datetime.today().date()

    purchases = Purchase.query.filter(
        Purchase.purchase_date == today
    ).order_by(
        Purchase.id.desc()
    ).all()

    return render_template(

        "purchase/list.html",

        purchases=purchases

    )