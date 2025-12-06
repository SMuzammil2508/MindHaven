
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from models import db, User, TherapistProfile, Story , bcrypt # import from models.py
from datetime import datetime   


# --- Add this dummy data list near the top of app.py ---
therapists_data = [
    {
        "id": 1,
        "name": "Dr. Sarah Jenkins",
        "specialty": "Anxiety & Depression",
        "location": "Mumbai, India (Online Available)",
        "rating": 4.9,
        "reviews": 120,
        "price": "₹1500/hr",
        "image": "https://randomuser.me/api/portraits/women/44.jpg"
    },
    {
        "id": 2,
        "name": "Dr. Aravind Mehta",
        "specialty": "Couples Therapy",
        "location": "Delhi, India",
        "rating": 4.7,
        "reviews": 85,
        "price": "₹2000/hr",
        "image": "https://randomuser.me/api/portraits/men/32.jpg"
    },
    {
        "id": 3,
        "name": "Ms. Emily Chen",
        "specialty": "Child Psychology",
        "location": "Bangalore, India",
        "rating": 4.8,
        "reviews": 200,
        "price": "₹1800/hr",
        "image": "https://randomuser.me/api/portraits/women/68.jpg"
    }
]





app = Flask(__name__)

# Add this to your imports
from models import User, TherapistProfile, db

@app.route("/take-quiz", methods=["GET", "POST"])
@login_required
def take_quiz():
    if request.method == "POST":
        # 1. Save Profile Details
        current_user.full_name = request.form.get("full_name")
        current_user.contact = request.form.get("contact")
        current_user.location = request.form.get("location")
        current_user.qualification = request.form.get("qualification")

        # 2. Calculate Quiz Score (The Grading System)
        # We assume 5 questions, values 1 (Low) to 5 (High)
        q1 = int(request.form.get("q1")) # Stress
        q2 = int(request.form.get("q2")) # Sleep
        q3 = int(request.form.get("q3")) # Anxiety
        q4 = int(request.form.get("q4")) # Mood
        
        total_score = q1 + q2 + q3 + q4
        current_user.mental_health_score = total_score

        # 3. The Matching Algorithm
        category = ""
        if total_score <= 8:
            category = "Wellness Coach" # Low stress
        elif total_score <= 14:
            category = "Anxiety Specialist" # Moderate
        else:
            category = "Trauma Specialist" # High stress/Crisis

        current_user.recommended_category = category
        db.session.commit()

        # 4. Find the Perfect Match in DB
        # This looks for a therapist whose specialization matches the category
        matched_therapist = TherapistProfile.query.filter(TherapistProfile.specialization.contains(category)).first()

        return render_template("results.html", score=total_score, category=category, therapist=matched_therapist)

    return render_template("quiz.html")

# ------------------ CONFIG ------------------
app.config['SECRET_KEY'] = 'vnjnsojvnvhjvn7837438@#@#fdjg'  # replace with env var in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindhaven.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bookings = []  # In-memory storage for bookings

# --- Add this new route ---
@app.route('/services')
def book_session():
    return render_template('services.html', therapists=therapists_data)

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    therapist_id = int(request.form.get('therapist_id'))
    date_str = request.form.get('date') # Format: 2025-12-10
    time = request.form.get('time')
    
    # Find therapist name based on ID
    therapist = next((t for t in therapists_data if t["id"] == therapist_id), None)
    
    if therapist:
        # Convert date "2025-12-10" to "10 Dec" for display
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        new_booking = {
            "therapist_name": therapist['name'],
            "date_day": date_obj.strftime("%d"),   # e.g., "10"
            "date_month": date_obj.strftime("%b"), # e.g., "Dec"
            "time": time,
            "status": "Upcoming"
        }
        
        # Add to our list
        bookings.append(new_booking)

    return redirect(url_for('sessions'))


# ------------------ INIT EXTENSIONS ------------------
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/stories")
def stories():
    # Show all stories
    all_stories = Story.query.all()
    return render_template("stories.html", stories=all_stories)


# PROFILE OF USER --------------
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


# PREVIOUS SERSSIONS --------------

@app.route("/sessions")
@login_required
def sessions():
    # We pass 'sessions=bookings' so the HTML can read the list
    return render_template("sessions.html", sessions=bookings)

# ---------- USER AUTH ----------

@app.route("/get-started", methods=["GET", "POST"])
def get_started():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Better to use flash messages, but plain text works for now
            return "User already exists. Please log in."

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)  # assuming you have a set_password method
        db.session.add(user)
        db.session.commit()

        # Redirect to login after successful signup
        return redirect(url_for("login"))

    # GET request → show signup form
    return render_template("get_started.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ---------- THERAPIST HELP ----------
@app.route("/help", methods=["GET", "POST"])
def help():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        specialization = request.form.get("specialization", "")
        password = request.form["password"]

        existing_therapist = TherapistProfile.query.filter_by(email=email).first()
        if existing_therapist:
            return "Therapist already registered."

        therapist = TherapistProfile(name=name, email=email, specialization=specialization)
        TherapistProfile.set_password(password)
        db.session.add(therapist)
        db.session.commit()
        return "Thank you for registering as a therapist!"
    return render_template("help.html")

# ------------------ MAIN ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # ensures tables exist
    app.run(debug=True)