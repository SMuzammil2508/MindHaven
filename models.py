from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# Initialize extensions (they will be bound to the app in app.py)
db = SQLAlchemy()
bcrypt = Bcrypt()

# ------------------ USER MODEL ------------------
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password: str) -> None:
        """Hashes and sets the user's password."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verifies the user's password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)


# ------------------ THERAPIST MODEL (optional for 'Do you want to help?') ------------------
class Therapist(db.Model, UserMixin):
    __tablename__ = "therapists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    specialization = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password: str) -> None:
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)


# ------------------ STORIES MODEL (optional for user submissions) ------------------
class Story(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationship back to User
    user = db.relationship("User", backref=db.backref("stories", lazy=True))