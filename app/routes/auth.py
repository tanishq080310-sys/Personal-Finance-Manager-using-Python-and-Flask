from flask import render_template, redirect, url_for, request
from models import db, User
from flask import Blueprint
from flask_login import login_user, login_required, logout_user



auth_bp = Blueprint("auth", __name__)



@auth_bp.route("/")
def home():
    return render_template("home.html")

@auth_bp.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        existing_user = User.query.filter_by(Email = email).first()

        if existing_user:
            return "User already exists. Please Login"  
        else:
            new_user = User(Name = name, Email = email, Password = password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        
    return render_template("register.html")


@auth_bp.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(Email = email, Password = password).first()

        if existing_user:
            login_user(existing_user)
            return redirect(url_for("dashboard.dashboard"))
        else:
            return "Invalid Credentials. Please try again with correct email and password."
        
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.home"))
