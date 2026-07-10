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

from models.billing import Bill, BillItem
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.prescription import Prescription


# =====================================
# Blueprint
# =====================================

billing = Blueprint(
    "billing",
    __name__,
    url_prefix="/billing"
)


# =====================================
# Bill List
# =====================================

@billing.route("/")
def list_bills():

    bills = Bill.query.order_by(
        Bill.created_at.desc()
    ).all()

    return render_template(
        "billing/invoices.html",
        bills=bills
    )


# =====================================
# View Bill
# =====================================

@billing.route("/view/<int:id>")
def view_bill(id):

    bill = Bill.query.get_or_404(id)

    items = BillItem.query.filter_by(
        bill_id=id
    ).all()

    return render_template(
        "billing/view.html",
        bill=bill,
        items=items
    )


# =====================================
# Billing History
# =====================================

@billing.route("/history")
def billing_history():

    bills = Bill.query.order_by(
        Bill.created_at.desc()
    ).all()

    return render_template(
        "billing/history.html",
        bills=bills
    )
# =====================================
# Add Bill
# =====================================

@billing.route("/add", methods=["GET", "POST"])
def add_bill():

    patients = Patient.query.order_by(
        Patient.user_id
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.user_id
    ).all()

    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc()
    ).all()

    prescriptions = Prescription.query.order_by(
        Prescription.created_at.desc()
    ).all()

    if request.method == "POST":

        try:

            patient_id = request.form.get("patient_id")
            doctor_id = request.form.get("doctor_id")
            appointment_id = request.form.get("appointment_id")
            prescription_id = request.form.get("prescription_id") or None

            consultation_fee = float(
                request.form.get("consultation_fee") or 0
            )

            medicine_total = float(
                request.form.get("medicine_total") or 0
            )

            lab_total = float(
                request.form.get("lab_total") or 0
            )

            other_charges = float(
                request.form.get("other_charges") or 0
            )

            discount = float(
                request.form.get("discount") or 0
            )

            tax = float(
                request.form.get("tax") or 0
            )

            payment_method = request.form.get(
                "payment_method"
            )

            payment_status = request.form.get(
                "payment_status"
            )

            remarks = request.form.get(
                "remarks"
            )

            # -------------------------
            # Bill Items
            # -------------------------

            item_names = request.form.getlist(
                "item_name[]"
            )

            quantities = request.form.getlist(
                "quantity[]"
            )

            prices = request.form.getlist(
                "price[]"
            )

            totals = request.form.getlist(
                "total[]"
            )

            item_total = sum(

                float(total or 0)

                for total in totals

            )

            # -------------------------
            # Grand Total
            # -------------------------

            grand_total = (

                consultation_fee

                + medicine_total

                + lab_total

                + other_charges

                + item_total

                + tax

                - discount

            )

            # -------------------------
            # Bill Number
            # -------------------------

            last_bill = Bill.query.order_by(
                Bill.id.desc()
            ).first()

            if last_bill:

                number = last_bill.id + 1

            else:

                number = 1

            bill_no = datetime.now().strftime(
                "BILL%Y%m%d"
            ) + f"{number:03d}"

            bill = Bill(

                bill_no=bill_no,

                patient_id=patient_id,

                doctor_id=doctor_id,

                appointment_id=appointment_id,

                prescription_id=prescription_id,

                consultation_fee=consultation_fee,

                medicine_total=medicine_total,

                lab_total=lab_total,

                other_charges=other_charges,

                discount=discount,

                tax=tax,

                grand_total=grand_total,

                payment_method=payment_method,

                payment_status=payment_status,

                remarks=remarks

            )

            db.session.add(bill)

            db.session.flush()

            # -------------------------
            # Save Bill Items
            # -------------------------

            for i in range(len(item_names)):

                if item_names[i].strip() == "":

                    continue

                item = BillItem(

                    bill_id=bill.id,

                    item_name=item_names[i],

                    quantity=int(
                        quantities[i] or 1
                    ),

                    price=float(
                        prices[i] or 0
                    ),

                    total=float(
                        totals[i] or 0
                    )

                )

                db.session.add(item)

            db.session.commit()

            flash(
                "Bill created successfully.",
                "success"
            )

            return redirect(
                url_for("billing.list_bills")
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error: {str(e)}",
                "danger"
            )

    return render_template(

        "billing/payment.html",

        patients=patients,

        doctors=doctors,

        appointments=appointments,

        prescriptions=prescriptions

    )
# =====================================
# Edit Bill
# =====================================

@billing.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_bill(id):

    bill = Bill.query.get_or_404(id)

    patients = Patient.query.order_by(
        Patient.user_id
    ).all()

    doctors = Doctor.query.order_by(
        Doctor.user_id
    ).all()

    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc()
    ).all()

    prescriptions = Prescription.query.order_by(
        Prescription.created_at.desc()
    ).all()

    items = BillItem.query.filter_by(
        bill_id=id
    ).all()

    if request.method == "POST":

        try:

            bill.patient_id = request.form.get(
                "patient_id"
            )

            bill.doctor_id = request.form.get(
                "doctor_id"
            )

            bill.appointment_id = request.form.get(
                "appointment_id"
            )

            bill.prescription_id = request.form.get(
                "prescription_id"
            ) or None

            bill.consultation_fee = float(
                request.form.get(
                    "consultation_fee"
                ) or 0
            )

            bill.medicine_total = float(
                request.form.get(
                    "medicine_total"
                ) or 0
            )

            bill.lab_total = float(
                request.form.get(
                    "lab_total"
                ) or 0
            )

            bill.other_charges = float(
                request.form.get(
                    "other_charges"
                ) or 0
            )

            bill.discount = float(
                request.form.get(
                    "discount"
                ) or 0
            )

            bill.tax = float(
                request.form.get(
                    "tax"
                ) or 0
            )

            bill.payment_method = request.form.get(
                "payment_method"
            )

            bill.payment_status = request.form.get(
                "payment_status"
            )

            bill.remarks = request.form.get(
                "remarks"
            )

            # -------------------------
            # Bill Items
            # -------------------------

            item_names = request.form.getlist(
                "item_name[]"
            )

            quantities = request.form.getlist(
                "quantity[]"
            )

            prices = request.form.getlist(
                "price[]"
            )

            totals = request.form.getlist(
                "total[]"
            )

            item_total = sum(
                float(total or 0)
                for total in totals
            )

            # -------------------------
            # Grand Total
            # -------------------------

            bill.grand_total = (

                bill.consultation_fee

                + bill.medicine_total

                + bill.lab_total

                + bill.other_charges

                + item_total

                + bill.tax

                - bill.discount

            )

            # -------------------------
            # Delete Old Items
            # -------------------------

            BillItem.query.filter_by(
                bill_id=id
            ).delete()

            # -------------------------
            # Save New Items
            # -------------------------

            for i in range(len(item_names)):

                if item_names[i].strip() == "":

                    continue

                item = BillItem(

                    bill_id=id,

                    item_name=item_names[i],

                    quantity=int(
                        quantities[i] or 1
                    ),

                    price=float(
                        prices[i] or 0
                    ),

                    total=float(
                        totals[i] or 0
                    )

                )

                db.session.add(item)

            db.session.commit()

            flash(
                "Bill updated successfully.",
                "success"
            )

            return redirect(
                url_for("billing.list_bills")
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error: {str(e)}",
                "danger"
            )

    return render_template(

        "billing/payment.html",

        bill=bill,

        items=items,

        patients=patients,

        doctors=doctors,

        appointments=appointments,

        prescriptions=prescriptions

    )


# =====================================
# Delete Bill
# =====================================

@billing.route("/delete/<int:id>", methods=["POST"])
def delete_bill(id):

    bill = Bill.query.get_or_404(id)

    try:

        BillItem.query.filter_by(
            bill_id=id
        ).delete()

        db.session.delete(bill)

        db.session.commit()

        flash(
            "Bill deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error: {str(e)}",
            "danger"
        )

    return redirect(
        url_for("billing.list_bills")
    )

# =====================================
# Change Payment Status
# =====================================

@billing.route("/status/<int:id>/<status>")
def change_payment_status(id, status):

    bill = Bill.query.get_or_404(id)

    allowed = [
        "Pending",
        "Paid",
        "Cancelled"
    ]

    if status not in allowed:

        flash(
            "Invalid payment status.",
            "danger"
        )

        return redirect(
            url_for("billing.list_bills")
        )

    try:

        bill.payment_status = status

        db.session.commit()

        flash(
            "Payment status updated successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error: {str(e)}",
            "danger"
        )

    return redirect(
        url_for("billing.list_bills")
    )


# =====================================
# Paid Bills
# =====================================

@billing.route("/paid")
def paid_bills():

    bills = Bill.query.filter_by(
        payment_status="Paid"
    ).order_by(
        Bill.created_at.desc()
    ).all()

    return render_template(
        "billing/invoices.html",
        bills=bills
    )


# =====================================
# Pending Bills
# =====================================

@billing.route("/pending")
def pending_bills():

    bills = Bill.query.filter_by(
        payment_status="Pending"
    ).order_by(
        Bill.created_at.desc()
    ).all()

    return render_template(
        "billing/invoices.html",
        bills=bills
    )


# =====================================
# Cancelled Bills
# =====================================

@billing.route("/cancelled")
def cancelled_bills():

    bills = Bill.query.filter_by(
        payment_status="Cancelled"
    ).order_by(
        Bill.created_at.desc()
    ).all()

    return render_template(
        "billing/invoices.html",
        bills=bills
    )


# =====================================
# Print Invoice
# =====================================

@billing.route("/print/<int:id>")
def print_bill(id):

    bill = Bill.query.get_or_404(id)

    items = BillItem.query.filter_by(
        bill_id=id
    ).order_by(
        BillItem.id.asc()
    ).all()

    return render_template(
        "billing/print.html",
        bill=bill,
        items=items
    )