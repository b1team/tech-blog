from app import db
import datetime

post_tags = db.Table('post_tags',
                     db.Column('tag_id', db.Integer, db.ForeignKey(
                         'tags.id'), primary_key=True),
                     db.Column('post_id', db.Integer, db.ForeignKey(
                         'posts.id'), primary_key=True)
                     )

                     
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone_number = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Tags %r>' % self.name


class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)

    post = db.relationship("Posts", uselist=False, back_populates="vote")

    def __repr__(self):
        return '<Vote %r>' % (self.upvote - self.downvote)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote_id = db.Column(db.Integer, db.ForeignKey('votes.id'), nullable=False)
    title = db.Column(db.String(200))
    slug = db.Column(db.String(200))
    brief = db.Column(db.Text)
    content = db.Column(db.Text)
    last_edited_at = db.Column(db.DateTime)

    users = db.relationship('Users', backref=db.backref('posts', lazy=True))
    vote = db.relationship("Votes", back_populates="post")
    tags = db.relationship('Tags', secondary=post_tags, lazy='subquery',
                           backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Posts %r>' % self.title


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.Text)

    post = db.relationship('Posts', backref=db.backref('comment', lazy=True))
    user = db.relationship('Users', backref=db.backref('comment', lazy=True))

    def __repr__(self):
        return '<Comment %r>' % self.content