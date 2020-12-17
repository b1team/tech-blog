from src.app import db
from src.app.models import Posts, Tags
from flask import Blueprint, abort
from flask import render_template
from flask import request, url_for, session
from flask import jsonify
from sqlalchemy import func, or_
from src.app import utils
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
    url = '/search'

    return render_template("sidebar/search.html", login=login, user=user, posts=posts, query=query, url=url)


@sidebar_bp.route("/tag/<slug>", methods=["GET","POST"])
def get_tag(slug):
    login = session.get("logged_in")
    user = session.get("username")
    tag = db.session.query(Tags.name).filter(Tags.slug == slug).first()
    if not tag:
        return abort(404)
    url = '/tag/{}'.format(slug)

    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).join(Tags.posts).filter(Tags.slug==slug, Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)

    return render_template("sidebar/tag.html", login=login, user=user,
            posts=posts, tag=tag.name, url=url)


@sidebar_bp.route("/favorite", methods=["GET"])
def favorite():
    posts = db.session.query(Posts).outerjoin(Posts.votes)
    default_num_of_posts = 5
    try:
        num_of_posts = int(request.args.get("top", default_num_of_posts))
    except ValueError:
        return [], 400
    num_of_posts = num_of_posts if num_of_posts > 0 else default_num_of_posts
    data = []
    for post in posts:
        ls = []
        for vote in post.votes:
            ls.append(vote.vote)
        up = ls.count(True)
        down = ls.count(False)
        data.append((up-down, post))
    
    data.sort(key=utils.takeFirst, reverse=True)

    result = []
    for _, post in data:
        data = utils.row2dict(post)
        data.pop('tags')
        data.pop('votes')
        data['created_at'] = post.created_at + timedelta(hours=7)
        result.append(data)

    return jsonify(posts=result[:num_of_posts])
    

@sidebar_bp.route("/tags", methods=["GET"])
def get_top_tags():
    num_of_tags = request.args.get("num_of_tags")
    if not num_of_tags or num_of_tags < 0:
        num_of_tags = 5
    top_tags = db.session.query(Tags.name, Tags.slug, func.count("*").label("count")).join(Posts.tags).group_by(Tags.name, Tags.slug).order_by(func.count("*").desc()).limit(num_of_tags)
    
    return jsonify(tags=[dict(name=tag.name, slug=tag.slug, count=tag.count) for tag in top_tags])