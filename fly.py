from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os
from passwords import hash_password, check_password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://kent:Capstone@thepikenet.asuscomm.com/kentairport')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------------- Models ---------------------- #

class Login(db.Model):
    __tablename__ = 'Login'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    user_role = db.Column(db.String(50))

class Flight(db.Model):
    __tablename__ = 'Flight'
    flight_id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    departure_airport = db.Column(db.String(100), nullable=False)
    arrival_airport = db.Column(db.String(100), nullable=False)
    aircraft_registration = db.Column(db.String(20), nullable=False)

# ---------------------- Routes ---------------------- #

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        form = request.form
        if Login.query.filter((Login.username == form['username']) | (Login.email == form['email'])).first():
            return "Username or Email already exists", 409
        hashed_pw, salt = hash_password(form['password'])
        new_user = Login(
            first_name=form['first_name'],
            last_name=form['last_name'],
            username=form['username'],
            password=hashed_pw + ':' + salt,
            email=form['email'],
            user_role = 'customer'
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        username = form.get('username')
        password = form.get('password')

        user = Login.query.filter_by(username=username).first()
        if user:
            if ":" in user.password:
                # Password is hashed and salted
                pw_hash, salt = user.password.split(":")
                if check_password(password, pw_hash, salt):
                    session_id = str(uuid.uuid4())
                    resp = make_response(redirect("/Home"))
                    resp.set_cookie("session_id", session_id)
                    return resp
            else:
                # none of the passwords in the database are salted, 
                # this is a security risk. This bypasses my security 
                # measures for the sake of the demo.
                if user.password == password:
                    print("⚠️ Needs changed. Password not secure.")
                    session_id = str(uuid.uuid4())
                    resp = make_response(redirect("/Home"))
                    resp.set_cookie("session_id", session_id)
                    return resp

        return "Invalid login", 401

    return render_template("index.html")

@app.route("/Home")
def home():
    session_id = request.cookies.get("session_id")
    if not session_id:
        return redirect("/login")
    return render_template("Home.html")

@app.route("/support")
def support():
    return render_template("support.html")

@app.route("/flights")
def flights():
    all_flights = Flight.query.order_by(Flight.departure_time).all()
    return render_template("flights.html", flights=all_flights)

@app.route("/employee")
def employee():
    return render_template("employee.html")

if __name__ == "__main__":
    app.run(debug=True)
