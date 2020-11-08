from flask import Blueprint, render_template
from flask import request, session
from app.models import Posts, Votes
from app import db
from slugify import slugify


post_bp = Blueprint("post_bp", __name__, template_folder="templates", static_folder="static")


@post_bp.route("/createpost", methods=["GET", "POST"])
def create_post():
    user = session.get("username")

    if request.method == "POST":
        title = request.form["title"]
        brief = request.form["brief"]
        body = request.form["body"]
        user_id = session.get("user_id")
        vote = Votes(upvote=0, downvote=0)
        post = Posts(user_id=user_id, vote_id=vote.id)

    login = session.get("logged_in")

    return render_template("create-post.html", login=login, user=user)


@post_bp.route("/postcontent", methods=["GET", "POST"])
def post_content():
    return render_template("post-content.html")
