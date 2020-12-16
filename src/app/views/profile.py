from flask import Blueprint, render_template, abort
from flask import request, session
from src.app import db
from src.app.models import Users


profile_bp = Blueprint("profile_bp", __name__, template_folder="templates", static_folder="static")


@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    login = session.get("logged_in")
    if login:
        cuser = session.get("username")
        update_user = db.session.query(Users).filter(Users.username==cuser).first()

        if request.method == "POST":
            email = request.form["email"]
            username = request.form["username"]
            name = request.form["name"]
            phone_number = request.form["phone"]
            
            update_user.email = email
            update_user.username = username
            update_user.name = name
            update_user.phone_number = phone_number
            db.session.commit()
    else:
        return abort(401)

    return render_template("profile/profile.html",login=login, user=cuser, uuser=update_user)
