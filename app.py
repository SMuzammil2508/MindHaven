from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template("stories.html")

@app.route("/get-started")
def get_started():
    return render_template("get_started.html")

@app.route("/help")
def help():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=True)