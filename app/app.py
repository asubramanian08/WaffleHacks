from sqlite3 import dbapi2
import db
import map
from psycopg2.errors import SerializationFailure
import psycopg2
from flask import Flask, session, redirect, url_for, escape, request, render_template
app = Flask(__name__)
app.secret_key = "27eduCBA09"


@app.route('/')
def index():
    return render_template("website.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    # get user input from the html form
    t_username = request.form.get("t_Username", "")
    t_email = request.form.get("t_Email", "")
    t_password = request.form.get("t_Password", "")

    # check for blanks
    if t_email == "":
        t_message = "Please fill in your email address"
        return render_template("register.html")

    if t_password == "":
        t_message = "Please fill in your password"
        return render_template("register.html")

    # hash the password they entered
    db.addUser(db.conn, email=t_email, password=t_password)
    t_message = "Your user account has been added."
    return render_template("register.html")


@app.route("/Sign-in", methods=["POST", "GET"])
def signin():
    if request.method == 'POST':

        t_email = request.form.get("t_Email", "")
        t_password = request.form.get("t_Password", "")
        db.validate_login(db.conn, email=t_email, password=t_password)
        session['password'] = t_password
        return redirect(url_for("/"))
    return render_template("login.html")


@app.route("/restriction", methods=["POST", "GET"])
def restriction():
    if request.method == 'POST':
        restriction = request.form.get('submit_button')
        session['restriction'] = restriction
        return redirect(url_for("table"))
    
    return render_template("restriction.html")

@app.route("/search_map", methods=["POST", "GET"])
def table():
    if "restriction" in session:
        #restriction = request.args['restriction']  # counterpart for url_for()
        restriction = session['restriction']
        
    #location = form.get(whatever user puts in form)
    #use geolocation API to convert location to proper format

    places = map.get_restaurants("0")
    data = []
    for place in places: 
        rest = []
        try: 
            name = place['name']
            rest.append(name)
            #est.append(db.getRating(name, restriction))
        except: 
            #rest.append('none')
            rest.append('none')
            
        try: 
           rest.append(place['vicinity'])
        except: 
           rest.append('none')
       # try: 
        #   rest.append(place['price_level'])
        #except: 
           #rest.append('none')
        
        data.append(rest)
    
    headings = ('Name','Address')
    return render_template("maps.html", headings=headings, data=data)
    


app.run(host='0.0.0.0', port=81)
