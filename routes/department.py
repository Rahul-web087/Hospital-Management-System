from flask import Blueprint, render_template, request, redirect, url_for, flash

from extensions import db
from models.department import Department


department = Blueprint(
    "department",
    __name__,
    url_prefix="/departments"
)


@department.route("/")
def list_departments():

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    return render_template(
        "department/list.html",
        departments=departments
    )


@department.route("/add", methods=["GET", "POST"])
def add_department():

    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")

        if Department.query.filter_by(name=name).first():

            flash(
                "Department already exists.",
                "danger"
            )

            return redirect(
                url_for("department.add_department")
            )

        department = Department(
            name=name,
            description=description
        )

        db.session.add(department)
        db.session.commit()

        flash(
            "Department added successfully.",
            "success"
        )

        return redirect(
            url_for("department.list_departments")
        )

    return render_template(
        "department/add.html"
    )


@department.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_department(id):

    department = Department.query.get_or_404(id)

    if request.method == "POST":

        department.name = request.form.get("name")

        department.description = request.form.get("description")

        department.status = (
            True
            if request.form.get("status")
            else False
        )

        db.session.commit()

        flash(
            "Department updated successfully.",
            "success"
        )

        return redirect(
            url_for("department.list_departments")
        )

    return render_template(
        "department/edit.html",
        department=department
    )


@department.route("/delete/<int:id>")
def delete_department(id):

    department = Department.query.get_or_404(id)

    db.session.delete(department)

    db.session.commit()

    flash(
        "Department deleted successfully.",
        "success"
    )

    return redirect(
        url_for("department.list_departments")
    )