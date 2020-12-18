from flask import Blueprint, render_template
from flask import session, request, url_for
from src.app.models import Posts, Tags
from src.app import db
from flask import redirect


home_bp = Blueprint("home_bp", __name__, template_folder="templates", static_folder="static")


@home_bp.route("/")
@home_bp.route("/home", methods=["GET", "POST"])
def home():
    login = session.get("logged_in")
    user = session.get("username")
    page_title = 'Home'

    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).filter(Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)
    url = '/home'

    return render_template("home/blog.html", login=login, user=user,
            posts=posts, url=url, page_title=page_title)

