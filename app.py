from flask import Flask, render_template
# import cloudinary_config

from config import Config
from extensions import db, mail, migrate, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"


    # Import Models
    from models.user import User
    # from models.department import Department
    # from models.doctor import Doctor
    # from models.patient import Patient
    # from models.medical_report import MedicalReport
    # from models.supplier import Supplier
    # from models.medicine_category import MedicineCategory
    # from models.medicine import Medicine
    # from models.purchase import Purchase
    # from models.purchase_item import PurchaseItem


    



    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from routes.auth import auth
    from routes.admin import admin
    from routes.department import department
    from routes.doctor import doctor
    from routes.patient import patient
    from routes.appointmen import appointment
    from routes.prescription import prescription
    from routes.billing import billing
    from routes.medical_report import medical_report
    from routes.receptionist import receptionist
    from routes.pharmacy import pharmacy
    from routes.supplier import supplier









    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(department)
    app.register_blueprint(doctor)
    app.register_blueprint(patient)
    app.register_blueprint(appointment)
    app.register_blueprint(prescription)
    app.register_blueprint(billing)
    app.register_blueprint(medical_report)
    app.register_blueprint(receptionist)
    app.register_blueprint(pharmacy)
    app.register_blueprint(supplier)





    # Home Page
    from flask import redirect, url_for
    from flask_login import current_user

    @app.route("/")
    def home():

        if current_user.is_authenticated:

            if current_user.role == User.ROLE_ADMIN:
                return redirect(url_for("admin.dashboard"))

            elif current_user.role == User.ROLE_DOCTOR:
                return redirect(url_for("doctor.dashboard"))

            elif current_user.role == User.ROLE_PATIENT:
                return redirect(url_for("patient.dashboard"))

            elif current_user.role == User.ROLE_RECEPTIONIST:
                return redirect(url_for("receptionist.dashboard"))

            elif current_user.role == User.ROLE_PHARMACIST:
                return redirect(url_for("pharmacy.dashboard"))

        return redirect(url_for("auth.login"))

    # Error Pages
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)