from flask import Blueprint, render_template, abort
from flask import request, session, Markup, redirect, url_for, request, jsonify
from src.app.models import Posts, Votes, Tags, Users, Comments
from src.app import db
from slugify import slugify
from datetime import datetime, timedelta
from misaka import Markdown, HtmlRenderer
from datetime import timedelta
from src.app import utils
from math import ceil


post_bp = Blueprint("post_bp", __name__, template_folder="templates", static_folder="static")


@post_bp.route("/createpost", methods=["GET", "POST"])
def create_post():
    username = session.get("username")
    login = session.get("logged_in")
    if login:
        user_id = session.get("user_id")
        action = "create post"

        if request.method == "POST":
            title = request.form["title"]
            brief = request.form["brief"]
            thumbnail = request.form["thumbnail"]
            body = request.form["body"]
            slug = "{0}-{1}".format(slugify(title),
                                    str(datetime.utcnow().timestamp()).replace('.', ''))

            user = db.session.query(Users).filter(Users.id == user_id).first()

            post = Posts(title=title,brief=brief, thumbnail=thumbnail, slug=slug, content=body)

            tags = request.form["tags"].strip()
            list_tag = []
            list_tag.extend(tag for tag in map(lambda x: x.strip(), tags.split(",")) if tag !="")
            db_tags = db.session.query(Tags).filter(Tags.name.in_(list_tag)).all()
            post.tags.extend(db_tags)
            existed_tags = {tag.name for tag in db_tags}

            for tag in list_tag:
                if tag not in existed_tags:
                    # tao mot tag
                    m_tag = Tags(name=tag, slug=tag)
                    post.tags.append(m_tag)

            post.user = user

            db.session.add(post)
            db.session.commit()

            return redirect(url_for("home_bp.home"))
    else:
        return abort(401)

    return render_template("post/create-post.html", login=login, user=username, action=action)


@post_bp.route("/posts/<slug>", methods=["GET", "POST"])
def post_content(slug):
    login = session.get("logged_in")
    post = db.session.query(Posts).filter(Posts.slug==slug).first()
    if not post:
        return abort(404)
    render = HtmlRenderer()
    md = Markdown(render)
    session['post_id'] = post.id

    user_id = session.get("user_id")
    username = session.get("username")
    post.content = Markup(md(post.content))
    
    return render_template("post/post-content.html",login=login , post=post, user=username)



@post_bp.route("/loadcmt", methods=["GET"])
def loadcmt():
    post_id = session.get("post_id")
    comments = db.session.query(Comments).join(Users.comments).order_by(Comments.created_at.desc()).filter(Comments.post_id==post_id)
    page = request.args.get('page', 0, type=int)
    page_size = request.args.get('page_size', 5, type=int)
    total = comments.count()
    if page_size:
        comments = comments.limit(page_size)
    if page:
        comments = comments.offset(page*page_size)
    num_of_page = ceil(total / page_size)
    result = []
    for comment in comments.all():
        data = utils.row2dict(comment)
        user = db.session.query(Users.avatar_url).filter(Users.id==comment.user_id).first()
        data['avatar_url'] = user.avatar_url
        data['username'] = comment.user.username
        data['created_at'] = comment.created_at + timedelta(hours=7)
        result.append(data)

    return jsonify(data=result, total=total, current_page=page + 1, page_size=page_size, num_of_page=num_of_page)


@post_bp.route("/addcmt", methods=["POST"])
def addcmt():
    login = session.get("logged_in")
    if login:
        post_id = session.get("post_id")
        user_id = session.get("user_id")
        post = db.session.query(Posts).filter(Posts.id==post_id).first()
        if not post:
            return jsonify(success=False), 404

        body = request.get_json(force=True)
        cmt = body.get("comment", "").strip()
        user = db.session.query(Users).filter(Users.id == user_id).first()
        if not post:
            return jsonify(success=False), 403
        new_cm = Comments(user_id=user_id, post_id=post_id, content=cmt)
        new_cm.user = user
        new_cm.post = post

        db.session.add(new_cm)
        db.session.commit()

        return jsonify(login=True, success=True)
    else:
        return jsonify(login=False)


@post_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    action = "update"
    login = session.get("logged_in")
    if login:
        username = session.get("username")
        user_id = session.get("user_id")
        post_update = db.session.query(Posts).filter(Posts.id==id).first()
        if not post_update:
            return abort(404)
        if post_update.user_id != user_id:
            return abort(403)
            
        old_tags = []
        for tag in post_update.tags:
            old_tags.append(tag.name)
        current_tags = ','.join(old_tags)

        if request.method == "POST":
            title = request.form["title"]
            brief = request.form["brief"]
            thumbnail = request.form["thumbnail"]
            body = request.form["body"]

            post_update.title = title
            post_update.brief = brief
            post_update.thumbnail = thumbnail
            post_update.content = body
            post_update.tags = []
        
            tags = request.form["tags"]
            list_tag = []
            list_tag.extend("".join(tags).split(","))
            db_tags = db.session.query(Tags).filter(Tags.name.in_(list_tag)).all()
            post_update.tags.extend(db_tags)
            existed_tags = {tag.name for tag in db_tags}

            for tag in list_tag:
                if tag not in existed_tags:
                    # tao mot tag
                    m_tag = Tags(name=tag, slug=tag)
                    post_update.tags.append(m_tag)

            db.session.commit()

            return redirect(url_for('home_bp.home'))
    else:
        return abort(401)

    return render_template("post/update.html", login=login, user=username, action=action, up_post=post_update, up_tags=current_tags)


@post_bp.route("/delete/<int:id>")
def delete(id):
    login = session.get("logged_in")
    if login:
        user_id = session.get("user_id")
        delete_post = db.session.query(Posts).filter(Posts.id == id).first()
        if not delete_post:
            return abort(404)
        if delete_post.user_id != user_id:
            return abort(403)

        delete_post.deleted = True
        db.session.commit()
    else:
        return abort(401)

    return redirect(url_for("post_bp.myposts"))

        
@post_bp.route("/myposts", methods=["GET", "POST"])
def myposts():
    login = session.get("logged_in")
    url = '/myposts'
    page_title = 'My posts'

    if login:
        user = session.get("username")
        user_id = session.get("user_id")

        page = request.args.get('page', 1, type=int)
        posts = db.session.query(Posts).filter(Posts.user_id==user_id, Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)
    else:
        return abort(401)

    return render_template("/post/my-post.html", login=login, posts=posts, user=user, url=url, page_title=page_title)


@post_bp.route("/user/<username>/posts", methods=["GET", "POST"])
def get_user_posts(username):
    login = session.get("logged_in")
    url = f'/user/{username}/posts'
    user = db.session.query(Users.username, Users.id).filter(Users.username == username).first()

    if user:
        page_title = f'{user.username} posts'
        page = request.args.get('page', 1, type=int)
        posts = db.session.query(Posts).filter(Posts.user_id == user.id, Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)
        return render_template("/sidebar/search.html", login=login, posts=posts, user=user.username, url=url, page_title=page_title)
    else:
        return abort(404)


@post_bp.route("/addvote", methods=["POST"])
def addvote():
    post_id = session.get('post_id')
    login = session.get("logged_in")
    if login is not True:
        return jsonify(login=False)

    user_id = session.get('user_id')
    user_vote = request.args.get('vote', 'up')
    user_vote = True if user_vote == 'up' else False
    try:
        v = db.session.query(Votes).filter(Votes.user_id==user_id, Votes.post_id==post_id).first()
        if v:
            if (user_vote and v.vote) or (not user_vote and not v.vote):
                db.session.delete(v)
            else:
                v.vote = not v.vote
        else:
            vote = Votes(vote=user_vote, post_id=post_id, user_id=user_id)
            db.session.add(vote)
        db.session.commit()
    except Exception as e:
        print(e)
        return {"status": "error", "message": str(e)}, 500
    else:
        return {"login": True,"status": "success", "message": "voted"}, 200


@post_bp.route("/loadvote", methods=["GET"])
def loadvote():
    post_id = session.get('post_id')
    current_user = session.get('user_id')
    if not post_id:
        return {"status": "error", "message": "post_id is not found"}, 404
    votes = db.session.query(Votes).filter(Votes.post_id==post_id).all()

    return jsonify(votes=[utils.row2dict(v) for v in votes], current_user=current_user)