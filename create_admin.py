from app import app
from extensions import db
from models.user import User

# =====================================
# Create First Admin Account
# Run: python create_admin.py
# =====================================

with app.app_context():

    # ----------------------------
    # Change these details
    # ----------------------------
    ADMIN_NAME = "Rahul Nayak"
    ADMIN_EMAIL = "hospitalmanagement491@gmail.com"      # Replace with your email
    ADMIN_PASSWORD = "Rnayakhms@10"   # Replace with your password

    # ----------------------------
    # Check if admin already exists
    # ----------------------------
    existing_admin = User.query.filter_by(email=ADMIN_EMAIL).first()

    if existing_admin:
        print("❌ Admin already exists!")
        print(f"Email: {existing_admin.email}")
    else:

        admin = User(
            full_name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            role=User.ROLE_ADMIN,
            is_active=True,
            is_verified=True
        )

        admin.set_password(ADMIN_PASSWORD)

        db.session.add(admin)
        db.session.commit()

        print("\n====================================")
        print("✅ Admin created successfully!")
        print("====================================")
        print(f"Name     : {ADMIN_NAME}")
        print(f"Email    : {ADMIN_EMAIL}")
        print("Role     : ADMIN")
        print("====================================")