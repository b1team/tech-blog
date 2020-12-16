from app import db
from app.models import Posts, Tags
from flask import Blueprint
from flask import render_template
from flask import request, url_for, session
from flask import jsonify
from sqlalchemy import func, or_
from app import utils
from datetime import timedelta


sidebar_bp = Blueprint("sidebar_bp", __name__,
                    template_folder="templates", static_folder="static")


@sidebar_bp.route("/search", methods=["GET", "POST"])
def search():
    login = session.get("logged_in")
    user = session.get("username")
    query = request.args.get("q", type=str)
    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).outerjoin(Posts.tags).filter(Posts.deleted==False,or_(func.lower(Posts.title).contains(query.lower()), func.lower(Tags.name).contains(query.lower()))).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5) 
    tags = db.session.query(Tags).all()
    tags1 = tags[:len(tags)//2]
    tags2 = tags[len(tags)//2:]
    url = '/search'


    return render_template("sidebar/search.html", login=login, user=user, posts=posts,query=query, tags1=tags1, tags2=tags2, url=url)


@sidebar_bp.route("/tag/<name>", methods=["GET","POST"])
def tag(name):
    login = session.get("logged_in")
    user = session.get("username")
    tags = db.session.query(Tags).all()
    tags1 = tags[:len(tags)//2]
    tags2 = tags[len(tags)//2:]
    tag = name
    url = '/tag/{}'.format(name)

    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).join(Tags.posts).filter(Tags.name==name, Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)

    return render_template("sidebar/tag.html", login=login, user=user,
            posts=posts, tags1=tags1, tags2=tags2, tag=tag, url=url)


@sidebar_bp.route("/favorite", methods=["GET"])
def favorite():
    posts = db.session.query(Posts).join(Posts.votes).all()

    data = []
    for post in posts:
        ls = []
        for vote in post.votes:
            ls.append(vote.vote)
        up = ls.count(True)
        down = ls.count(False)
        data.append((up-down, post))
    
    data.sort(key=utils.takeFirst, reverse=True)

    ls_posts = []
    for post in data:
        ls_posts.append(post[1])

    result = []
    for post in ls_posts:
        data = utils.row2dict(post)
        data['tags'] = [tag.name for tag in data['tags']]
        data['votes'] = [vote.vote for vote in data['votes']]
        data['created_at'] = post.created_at + timedelta(hours=7)
        result.append(data)

    return jsonify(top_5=result[:5])
    
