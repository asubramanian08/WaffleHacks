from flask import Flask, render_template, request
app = Flask(__name__)
from db import *
conn = psycopg2.connect(
    "postgresql://chantal:wafflehacks2022@free-tier6.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dwafflehacks-2805")


@app.route('/')
def index():
    return render_template("website.html")


@app.route("/register", methods=["POST","GET"])
def register():
    # get user input from the html form
    t_username = request.form.get("t_Username", "")
    t_email = request.form.get("t_Email", "")
    t_password = request.form.get("t_Password", "")

    # # check for blanks
    if t_email == "":
        t_message = "Please fill in your email address"
        return render_template("register.html")

    if t_password == "":
        t_message = "Please fill in your password"
        return render_template("register.html")

    # hash the password they entered
    db.addUser(conn, email=t_email, password=t_password)
    t_message = "Your user account has been added."
    return render_template("register.html")

app.run(host='0.0.0.0', port=81)

