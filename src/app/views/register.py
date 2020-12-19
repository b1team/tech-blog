from flask import Blueprint, render_template, redirect, url_for
from flask import request
from sqlalchemy import or_
from src.app import db
from src.app.models import Users

register_bp = Blueprint("register_bp", __name__, template_folder="templates", static_folder="static")


@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmPassword = request.form["ConfirmPassword"]

        db_user = db.session.query(Users).filter(or_(Users.username==username, Users.email==email)).first()

        if db_user is None:
            if password is confirmPassword:
                new_user = Users(username=username, password=password, email=email)
                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for("login_bp.login"))
        else:
            return render_template("register/register.html", register_error=True)
            
    return render_template("register/register.html")