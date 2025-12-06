from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# Initialize extensions (same as your code)
db = SQLAlchemy()
bcrypt = Bcrypt()

# ------------------ USER MODEL ------------------
# I kept your exact field names (id, username, email, password) 
# and added 'role' to handle both Users and Therapists in one login system.
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Kept exact name 'password' as per your original code
    password = db.Column(db.String(200), nullable=False)

    # --- NEW ADDITIONS ---
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'therapist'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships (New)
    therapist_profile = db.relationship("TherapistProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    stories = db.relationship("Story", back_populates="author", lazy='dynamic', cascade="all, delete-orphan")
    mood_logs = db.relationship("MoodLog", backref="user", lazy='dynamic', cascade="all, delete-orphan")
    
    # Appointments (New)
    appointments_as_patient = db.relationship("Appointment", foreign_keys='Appointment.patient_id', backref="patient", lazy='dynamic')
    appointments_as_therapist = db.relationship("Appointment", foreign_keys='Appointment.therapist_id', backref="therapist", lazy='dynamic')

    # Kept your exact methods
    def set_password(self, password: str) -> None:
        """Hashes and sets the user's password."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verifies the user's password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)


# ------------------ THERAPIST PROFILE (New) ------------------
# Instead of a separate 'Therapist' table for login, we link this to the User.
# This prevents login errors.
class TherapistProfile(db.Model):
    __tablename__ = "therapist_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    specialization = db.Column(db.String(200), nullable=True)
    license_number = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    user = db.relationship("User", back_populates="therapist_profile")


# ------------------ STORIES MODEL ------------------
class Story(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # --- NEW ADDITIONS ---
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)

    # Relationship back to User (Updated to match User model)
    author = db.relationship("User", back_populates="stories")


# ------------------ MOOD LOG (New) ------------------
class MoodLog(db.Model):
    __tablename__ = "mood_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mood_score = db.Column(db.Integer, nullable=False) # 1-10
    note = db.Column(db.Text, nullable=True)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)


# ------------------ APPOINTMENTS (New) ------------------
class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending") 
    notes = db.Column(db.Text, nullable=True)