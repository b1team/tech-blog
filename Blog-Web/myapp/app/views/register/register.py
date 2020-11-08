from flask import Blueprint, render_template, redirect, url_for
from flask import request, flash
from app import db
from app.models import Users

register_bp = Blueprint("register_bp", __name__, template_folder="templates", static_folder="static")


@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmPassword = request.form["ConfirmPassword"]

        db_user = db.session.query(Users).filter(Users.username==username, Users.email==email).first()

        if password is confirmPassword and db_user is None:
            new_user = Users(username=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for("login_bp.login"))
    
    return render_template("register.html")
