from flask import Blueprint, render_template
from flask import request, session, Markup, redirect, url_for
from app.models import Posts, Votes, Tags, Users, Comments
from app import db
from slugify import slugify
from datetime import datetime
from misaka import Markdown, HtmlRenderer
from datetime import timedelta


post_bp = Blueprint("post_bp", __name__, template_folder="templates", static_folder="static")


@post_bp.route("/createpost", methods=["GET", "POST"])
def create_post():
    username = session.get("username")
    login = session.get("logged_in")
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

    user_id = session.get("user_id")
    username = session.get("username")
    post.content = Markup(md(post.content))
    
    tags = db.session.query(Tags).all()
    tags1 = tags[:len(tags)//2+1]
    tags2 = tags[len(tags)//2+1:]

    page = request.args.get('page', 1, type=int)
    comments = db.session.query(Comments).order_by(Comments.created_at.desc()).filter(Comments.post_id==post.id).paginate(page=page, per_page=5)

    if request.method == "POST":
        cmt = request.form["comment"]
        user = db.session.query(Users).filter(Users.id == user_id).first()
        new_cm = Comments(user_id=user_id, post_id=post.id, content=cmt)
        new_cm.user = user
        new_cm.post = post

        db.session.add(new_cm)
        db.session.commit()
        return redirect(url_for("post_bp.post_content", slug=post.slug))

    return render_template("post/post-content.html",login=login , post=post, user=username, comments=comments, tags1=tags1, tags2=tags2)


@post_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    action = "update"
    login = session.get("logged_in")
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
    delete_post = db.session.query(Posts).filter(Posts.id == id).first()
    delete_post.deleted = True
    db.session.commit()

    return redirect(url_for('home_bp.home'))

        
@post_bp.route("/myposts", methods=["GET", "POST"])
def myposts():
    login = session.get("logged_in")
    user = session.get("username")
    user_id = session.get("user_id")
    tags = db.session.query(Tags).all()
    tags1 = tags[:len(tags)//2+1]
    tags2 = tags[len(tags)//2+1:]

    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).filter(Posts.user_id==user_id, Posts.deleted==False).order_by(Posts.created_at.desc()).paginate(page=page, per_page=5)

    return render_template("/post/my-post.html", login=login, posts=posts, user=user, tags1=tags1, tags2=tags2)