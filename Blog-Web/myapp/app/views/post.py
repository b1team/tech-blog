from flask import Blueprint, render_template
from flask import request, session, Markup, redirect, url_for, request, jsonify
from app.models import Posts, Votes, Tags, Users, Comments
from app import db
from slugify import slugify
from datetime import datetime, timedelta
from misaka import Markdown, HtmlRenderer
from datetime import timedelta
from app import utils


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
            body = request.form["body"]
            slug = "{0}-{1}".format(slugify(title),
                                    str(datetime.utcnow().timestamp()).replace('.', ''))

            vote = Votes(upvote=0, downvote=0)
            user = db.session.query(Users).filter(Users.id == user_id).first()

            post = Posts(title=title,brief=brief, slug=slug, content=body)

            tags = request.form["tags"]
            list_tag = []
            list_tag.extend("".join(tags).split(","))
            db_tags = db.session.query(Tags).filter(Tags.name.in_(list_tag)).all()
            post.tags.extend(db_tags)
            existed_tags = {tag.name for tag in db_tags}

            for tag in list_tag:
                if tag not in existed_tags:
                    # tao mot tag
                    m_tag = Tags(name=tag, slug=tag)
                    post.tags.append(m_tag)

            post.vote = vote
            post.user = user

            db.session.add(post)
            db.session.commit()

            return redirect(url_for("home_bp.home"))

    return render_template("post/create-post.html", login=login, user=username, action=action)


@post_bp.route("/posts/<slug>", methods=["GET", "POST"])
def post_content(slug):
    login = session.get("logged_in")
    post = db.session.query(Posts).filter(Posts.slug==slug).first()
    render = HtmlRenderer()
    md = Markdown(render)
    session['post_id'] = post.id
    comments = db.session.query(Comments).filter(Comments.post_id==post.id).all()
    if comments is not None:
        num_of_pages = (len(comments) // 5) + 1
    else:
        num_of_pages = 0

    user_id = session.get("user_id")
    username = session.get("username")
    post.content = Markup(md(post.content))
    
    tags = db.session.query(Tags).all()
    tags1 = tags[:len(tags)//2+1]
    tags2 = tags[len(tags)//2+1:]

    return render_template("post/post-content.html",login=login , post=post, user=username, tags1=tags1, tags2=tags2, num_of_pages=num_of_pages)



@post_bp.route("/loadcmt", methods=["GET"])
def loadcmt():
    post_id = session.get("post_id")
    comments = db.session.query(Comments).join(Users.comments).order_by(Comments.created_at.desc()).filter(Comments.post_id==post_id)
    page = request.args.get('page', 0,type=int)
    page_size = request.args.get('page_size', 5,type=int)

    if page_size:
        comments = comments.limit(page_size)
    if page:
        comments = comments.offset(page*page_size)

    result = []
    for comment in comments.all():
        data = utils.row2dict(comment)
        data['username'] = comment.user.username
        data['created_at'] = comment.created_at + timedelta(hours=7)
        result.append(data)
    return jsonify(data=result)


@post_bp.route("/addcmt", methods=["POST"])
def addcmt():
    login = session.get("logged_in")
    if login:
        post_id = session.get("post_id")
        user_id = session.get("user_id")
        post = db.session.query(Posts).filter(Posts.id==post_id).first()

        body = request.get_json(force=True)
        cmt = body.get("comment", "")
        user = db.session.query(Users).filter(Users.id == user_id).first()
        new_cm = Comments(user_id=user_id, post_id=post_id, content=cmt)
        new_cm.user = user
        new_cm.post = post

        db.session.add(new_cm)
        db.session.commit()

        return jsonify(success=True)


@post_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    action = "update"
    login = session.get("logged_in")
    if login:
        username = session.get("username")

        post_update = db.session.query(Posts).filter(Posts.id==id).first()
            
        old_tags = []
        for tag in post_update.tags:
            old_tags.append(tag.name)
        current_tags = ','.join(old_tags)

        if request.method == "POST":
            title = request.form["title"]
            brief = request.form["brief"]
            body = request.form["body"]
            slug = "{0}-{1}".format(slugify(title),
                                    str(datetime.utcnow().timestamp()).replace('.', ''))

            post_update.title = title
            post_update.slug = slug 
            post_update.brief = brief
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

    return render_template("post/update.html", login=login, user=username, action=action, up_post=post_update, up_tags=current_tags)


@post_bp.route("/delete/<int:id>")
def delete(id):
    login = session.get("logged_in")
    if login:
        delete_post = db.session.query(Posts).filter(Posts.id == id).first()
        delete_post.deleted = True
        db.session.commit()

    return redirect(url_for('home_bp.home'))

        
@post_bp.route("/myposts", methods=["GET", "POST"])
def myposts():
    login = session.get("logged_in")
    if login:
        user = session.get("username")
        user_id = session.get("user_id")
        tags = db.session.query(Tags).all()
        tags1 = tags[:len(tags)//2+1]
        tags2 = tags[len(tags)//2+1:]

        page = request.args.get('page', 1, type=int)
        posts = db.session.query(Posts).filter(Posts.user_id==user_id, Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)

    return render_template("/post/my-post.html", login=login, posts=posts, user=user, tags1=tags1, tags2=tags2)