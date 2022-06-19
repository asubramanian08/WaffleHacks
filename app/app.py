import db
import map
from psycopg2.errors import SerializationFailure
import psycopg2
from flask import Flask, session, redirect, url_for, escape, request, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("website.html")


@app.route("/register", methods=["POST", "GET"])
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


@app.route("/Sign-in", methods=["POST", "GET"])
def signin():
    if request.method == 'POST':

        t_email = request.form.get("t_Email", "")
        t_password = request.form.get("t_Password", "")
        db.validate_login(conn, email=t_email, password=t_password)
        session['password'] = t_password
        return redirect(url_for("/"))
    return render_template("login.html")

@app.route("/restriction", methods=["POST", "GET"])
def restriction():
    restriction = form.get('restriction')
    if restriction != " ":
        return restriction
    return render_template("restriction.html")




@app.route("/search_map", methods=["POST", "GET"])
def placeholder():
    location = form.get(whatever user puts in form)
    #use geolocation API to convert location to proper format
    query_info = maps.get_restaurants(location)
    names_list = query_info[for name in name return query_info[0]]
    addresses_list =
    ratings = 
    reviews = db.getReviews(restaurant, dietary_rest)

    return render_template("maps.html", query_info)


    





app.run(host='0.0.0.0', port=81)
