from flask import Blueprint, render_template
from flask import request, redirect, url_for, session, flash
from app import db
from app.models import Users


login_bp = Blueprint("login_bp", __name__, template_folder="templates", static_folder="static")


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        logged_in = db.session.query(Users).filter(Users.email==email, Users.password==password).first()
        if logged_in is not None:
            flash("Login success")
            session["logged_in"] = True
            session["user_id"] = logged_in.id
            session["username"] = logged_in.username
            return redirect(url_for('home_bp.home'))
        else:
            flash("login false")

    return render_template("login.html")


@login_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session["logged_in"] = False
    return redirect("/")
