from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def signin():
    return render_template("sign-in.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/sign-up")
def signup():
    return render_template("sign-up.html")

