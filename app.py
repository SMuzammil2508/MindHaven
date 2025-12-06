from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from models import db, User, Therapist, Story  # import from models.py

app = Flask(__name__)

# ------------------ CONFIG ------------------
app.config['SECRET_KEY'] = 'vnjnsojvnvhjvn7837438@#@#fdjg'  # replace with env var in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindhaven.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# ---------- USER AUTH ----------
@app.route("/get-started", methods=["GET", "POST"])
def get_started():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User already exists. Please log in."

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
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

        existing_therapist = Therapist.query.filter_by(email=email).first()
        if existing_therapist:
            return "Therapist already registered."

        therapist = Therapist(name=name, email=email, specialization=specialization)
        therapist.set_password(password)
        db.session.add(therapist)
        db.session.commit()
        return "Thank you for registering as a therapist!"
    return render_template("help.html")

# ------------------ MAIN ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # ensures tables exist
    app.run(debug=True)