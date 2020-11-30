from app import db
from app.models import Posts, Tags
from flask import Blueprint
from flask import render_template
from flask import request, url_for, session

sidebar_bp = Blueprint("sidebar_bp", __name__,
                    template_folder="templates", static_folder="static")


@sidebar_bp.route("/search", methods=["GET", "POST"])
def search():
    login = session.get("logged_in")
    user = session.get("username")
    query = request.args.get("q", type=str)
    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).filter(Posts.title.contains(query), Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)


    return render_template("sidebar/search.html", login=login, user=user, posts=posts,query=query)


@sidebar_bp.route("/tag/<name>", methods=["GET","POST"])
def tag(name):
    login = session.get("logged_in")
    user = session.get("username")
    tags = db.session.query(Tags).all()
    tags1 = tags[:len(tags)//2+1]
    tags2 = tags[len(tags)//2+1:]
    tag = name

    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).join(Tags.posts).filter(Tags.name==name, Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)

    return render_template("sidebar/tag.html", login=login, user=user,
            posts=posts, tags1=tags1, tags2=tags2, tag=tag)
