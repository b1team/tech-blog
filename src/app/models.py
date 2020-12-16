from src.app import db
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
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone_number = db.Column(db.Integer)
    avatar_url = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.username


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    name = db.Column(db.String(80), nullable=False, unique=True)
    slug = db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        return '<Tags %r>' % self.name


class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    vote = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    post = db.relationship("Posts", uselist=False, back_populates="votes")
    user = db.relationship('Users', backref=db.backref('votes', lazy=True))

    def __repr__(self):
        return '<Vote %r>' % self.vote


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    thumbnail = db.Column(db.Text)
    slug = db.Column(db.String(200),nullable=False, unique=True)
    brief = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    last_edited_at = db.Column(db.DateTime)

    user = db.relationship('Users', backref=db.backref('posts', lazy=True))
    votes = db.relationship("Votes", back_populates="post")
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
    content = db.Column(db.Text, nullable=False)

    post = db.relationship('Posts', backref=db.backref('comments', lazy=True))
    user = db.relationship('Users', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return '<Comment %r>' % self.content
