from flask import Blueprint, render_template
from flask import session, request, url_for
from app.models import Posts, Tags
from app import db
from flask import redirect


home_bp = Blueprint("home_bp", __name__, template_folder="templates", static_folder="static")


@home_bp.route("/")
@home_bp.route("/home", methods=["GET", "POST"])
def home():

    login = session.get("logged_in")
    user = session.get("username")
    tags = db.session.query(Tags).all()
    tags1 = tags[:len(tags)//2+1]
    tags2 = tags[len(tags)//2+1:]

    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).filter(Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)


    return render_template("home/blog.html", login=login, user=user,
            posts=posts, tags1=tags1, tags2=tags2)

