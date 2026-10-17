from datetime import datetime, timedelta

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from flask_mail import Message

from extensions import db, mail

from models.user import User
from models.patient import Patient
import secrets
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


auth = Blueprint("auth", __name__)


# =====================================
# Login
# =====================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if current_user.is_authenticated:

        if current_user.role == User.ROLE_ADMIN:
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == User.ROLE_DOCTOR:
            return redirect(url_for("doctor.dashboard"))

        elif current_user.role == User.ROLE_PATIENT:
            return redirect(url_for("patient.dashboard"))

        elif current_user.role == User.ROLE_PHARMACIST:
            return redirect(url_for("pharmacy.dashboard"))

        elif current_user.role == User.ROLE_ACCOUNTANT:
            return redirect(url_for("billing.list_bills"))

        elif current_user.role == User.ROLE_LAB:
            return redirect(url_for("medical_report.list_reports"))

        elif current_user.role == User.ROLE_RECEPTIONIST:
            return redirect(url_for("receptionist.dashboard"))

        return redirect(url_for("home"))

    # Login POST
    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()

        if not user:

            flash(
                "Email not found.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        if not user.check_password(password):

            flash(
                "Invalid password.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        if not user.is_active:

            flash(
                "Your account is disabled.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        login_user(
            user,
            remember=remember
        )

        flash(
            f"Welcome {user.full_name}",
            "success"
        )

        # Role Redirect
        if user.role == User.ROLE_ADMIN:
            return redirect(
                url_for("admin.dashboard")
            )

        elif user.role == User.ROLE_DOCTOR:
            return redirect(
                url_for("doctor.dashboard")
            )

        elif user.role == User.ROLE_PATIENT:
            return redirect(
                url_for("patient.dashboard")
            )

        elif user.role == User.ROLE_PHARMACIST:
            return redirect(
                url_for("pharmacy.dashboard")
            )

        elif user.role == User.ROLE_ACCOUNTANT:
            return redirect(
                url_for("billing.list_bills")
            )

        elif user.role == User.ROLE_LAB:
            return redirect(
                url_for("medical_report.list_reports")
            )

        elif user.role == User.ROLE_RECEPTIONIST:
            return redirect(
                url_for("receptionist.dashboard")
            )

        return redirect(
            url_for("home")
        )

    return render_template(
        "auth/login.html"
    )


# =====================================
# Register - Patient Only
# =====================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # Check password
        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        # Check existing email
        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        # Create user
        user = User(
            full_name=full_name,
            email=email,
            role=User.ROLE_PATIENT
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Create patient
        patient = Patient(
            user_id=user.id,
            patient_code=f"PAT{user.id:05d}",
            blood_group="",
            emergency_contact="",
            emergency_phone="",
            medical_history="",
            allergies="",
            insurance_provider="",
            insurance_number=""
        )

        db.session.add(patient)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html"
    )

@auth.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            flash(
                "No account found with that email.",
                "danger"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

        # Generate reset token
        token = secrets.token_urlsafe(32)

        user.reset_token = token

        user.reset_token_expiry = (
            datetime.utcnow()
            + timedelta(minutes=30)
        )

        db.session.commit()

        # Generate production reset URL
        reset_link = (
            current_app.config["APP_URL"]
            + url_for(
                "auth.reset_password",
                token=token
            )
        )

        # =====================================
        # Brevo API configuration
        # =====================================

        configuration = sib_api_v3_sdk.Configuration()

        configuration.api_key["api-key"] = (
            current_app.config["BREVO_API_KEY"]
        )

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        # =====================================
        # Create Password Reset Email
        # =====================================

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(

            sender={
                "name": "Hospital Management System",
                "email": current_app.config["MAIL_DEFAULT_SENDER"]
            },

            to=[
                {
                    "email": user.email,
                    "name": user.full_name
                }
            ],

            subject="Hospital Management System - Password Reset",

            # Plain-text fallback
            text_content=f"""
        Hello {user.full_name},

        A request was received to reset your password.

        Click the link below to reset your password:

        {reset_link}

        This link will expire in 30 minutes.

        If you did not request a password reset,
        you can safely ignore this email.

        Hospital Management System
        """,

            # HTML email
            html_content=f"""
        <!DOCTYPE html>
        <html lang="en">

        <head>

            <meta charset="UTF-8">

            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">

            <title>Password Reset</title>

        </head>

        <body style="
            margin:0;
            padding:0;
            background:#f4f6f9;
            font-family:Arial, Helvetica, sans-serif;
        ">

        <table width="100%"
               cellpadding="0"
               cellspacing="0"
               style="
                   background:#f4f6f9;
                   padding:40px 15px;
               ">

            <tr>

                <td align="center">

                    <table width="600"
                           cellpadding="0"
                           cellspacing="0"
                           style="
                               max-width:600px;
                               width:100%;
                               background:#ffffff;
                               border-radius:12px;
                               overflow:hidden;
                           ">

                        <!-- Header -->

                        <tr>

                            <td align="center"
                                style="
                                    background:#0d6efd;
                                    padding:30px 20px;
                                ">

                                <div style="
                                    font-size:40px;
                                    margin-bottom:10px;
                                ">

                                    🔐

                                </div>

                                <h1 style="
                                    margin:0;
                                    color:#ffffff;
                                    font-size:25px;
                                ">

                                    Hospital Management System

                                </h1>

                            </td>

                        </tr>


                        <!-- Main Content -->

                        <tr>

                            <td style="
                                padding:40px 35px;
                                color:#333333;
                            ">

                                <h2 style="
                                    margin-top:0;
                                    color:#222222;
                                ">

                                    Password Reset Request

                                </h2>


                                <p style="
                                    font-size:16px;
                                    line-height:1.6;
                                ">

                                    Hello
                                    <strong>{user.full_name}</strong>,

                                </p>


                                <p style="
                                    font-size:16px;
                                    line-height:1.6;
                                ">

                                    We received a request to reset
                                    the password for your account.

                                </p>


                                <p style="
                                    font-size:16px;
                                    line-height:1.6;
                                ">

                                    Click the button below to create
                                    a new password.

                                </p>


                                <!-- Reset Button -->

                                <table width="100%"
                                       cellpadding="0"
                                       cellspacing="0">

                                    <tr>

                                        <td align="center"
                                            style="padding:25px 0;">

                                            <a href="{reset_link}"
                                               style="
                                                   display:inline-block;
                                                   background:#0d6efd;
                                                   color:#ffffff;
                                                   text-decoration:none;
                                                   padding:14px 30px;
                                                   border-radius:6px;
                                                   font-size:16px;
                                                   font-weight:bold;
                                               ">

                                                Reset My Password

                                            </a>

                                        </td>

                                    </tr>

                                </table>


                                <!-- Expiry Warning -->

                                <div style="
                                    background:#fff3cd;
                                    border:1px solid #ffecb5;
                                    border-radius:6px;
                                    padding:15px;
                                    margin:10px 0 25px 0;
                                ">

                                    <p style="
                                        margin:0;
                                        color:#664d03;
                                        font-size:14px;
                                        line-height:1.5;
                                    ">

                                        <strong>Important:</strong>

                                        This password reset link will
                                        expire in 30 minutes.

                                    </p>

                                </div>


                                <p style="
                                    font-size:14px;
                                    color:#666666;
                                    line-height:1.6;
                                ">

                                    If you did not request a password
                                    reset, you can safely ignore this
                                    email.

                                </p>


                                <!-- Fallback Link -->

                                <p style="
                                    font-size:13px;
                                    color:#777777;
                                    line-height:1.5;
                                    margin-top:25px;
                                ">

                                    If the button does not work,
                                    copy and paste this link into
                                    your browser:

                                </p>


                                <p style="
                                    font-size:12px;
                                    word-break:break-all;
                                    color:#0d6efd;
                                ">

                                    {reset_link}

                                </p>

                            </td>

                        </tr>


                        <!-- Footer -->

                        <tr>

                            <td align="center"
                                style="
                                    background:#f8f9fa;
                                    padding:25px 20px;
                                    border-top:1px solid #eeeeee;
                                ">

                                <p style="
                                    margin:0 0 8px 0;
                                    font-size:13px;
                                    color:#777777;
                                ">

                                    Hospital Management System

                                </p>


                                <p style="
                                    margin:0;
                                    font-size:12px;
                                    color:#999999;
                                ">

                                    This is an automated email.
                                    Please do not reply.

                                </p>

                            </td>

                        </tr>

                    </table>

                </td>

            </tr>

        </table>

        </body>

        </html>
        """
        )


        # Send through Brevo API


        try:

            api_instance.send_transac_email(
                send_smtp_email
            )

        except ApiException as e:

            current_app.logger.error(
                f"Brevo API email error: {e}"
            )

            flash(
                "Unable to send password reset email. "
                "Please try again later.",
                "danger"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

        flash(
            "Password reset link has been sent to your email.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )
    return render_template(
        "auth/reset_password.html"
    )


# =====================================
# Test Email
# =====================================

@auth.route("/test-email")
@login_required
def test_email():

    msg = Message(
        subject="Hospital Management System - Email Test",
        sender=current_app.config[
            "MAIL_DEFAULT_SENDER"
        ],
        recipients=[current_user.email]
    )

    msg.body = f"""
Hello {current_user.full_name},

Congratulations!

Your Hospital Management System is successfully
connected to Brevo.

This is a test email.

Regards,
Hospital Management System
"""

    mail.send(msg)

    flash(
        "Test email sent successfully.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# =====================================
# Logout
# =====================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )