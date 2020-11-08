from flask import Blueprint, render_template
from flask import session

home_bp = Blueprint("home_bp", __name__, template_folder="templates", static_folder="static")


@home_bp.route("/")
@home_bp.route("/home", methods=["GET", "POST"])
def home():
    login = session.get("logged_in")
    user = session.get("username")

    return render_template("blog.html", login=login, user=user)
