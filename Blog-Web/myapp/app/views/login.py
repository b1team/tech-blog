from flask import Blueprint, render_template
from flask import request, redirect, url_for, session, flash
from app import db
from app.models import Users


login_bp = Blueprint("login_bp", __name__, template_folder="templates", static_folder="static")


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    state = {
        "status": "success",
        "message": ""
    }
    
    login = session.get("logged_in")
    if login:
        return redirect(url_for('home_bp.home'))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        logged_in = db.session.query(Users).filter(Users.email==email, Users.password==password).first()
        if logged_in is not None:
            session["logged_in"] = True
            session["user_id"] = logged_in.id
            session["username"] = logged_in.username
            session["count"] = 0
            session["login_success"] = {"status": True, 'message': "Đăng nhập thành công", 'alerted': False}

            return redirect(url_for('home_bp.home'))
        else:
            state["status"] = "error"
            state["message"] = "Đăng nhập thất bại"

    return render_template("login/login.html", state=state)


@login_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session["logged_in"] = False
    session["user_id"] = ""
    session["username"] = ""

    return redirect("/")
