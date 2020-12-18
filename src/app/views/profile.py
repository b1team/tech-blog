from flask import Blueprint, render_template, abort
from flask import request, session
from src.app import db
from src.app.models import Users


profile_bp = Blueprint("profile_bp", __name__, template_folder="templates", static_folder="static")


@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    login = session.get("logged_in")
    if login:
        username = session.get("username")
        user = db.session.query(Users).filter(Users.username==username).first()

        if request.method == "POST":
            f_email = request.form["email"]
            f_username = request.form["username"]
            f_name = request.form["name"]
            f_phone_number = request.form["phone"]
            
            update_user.email = f_email
            update_user.username = f_username
            update_user.name = f_name
            update_user.phone_number = f_phone_number
            db.session.commit()
        return render_template("profile/profile.html",login=login, user=username, uuser=user)
    else:
        return abort(401)

