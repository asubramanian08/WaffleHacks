from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("website.html")

@app.route('/register')
def index():
    return render_template("register.html")


app.run(host='0.0.0.0', port=81)

