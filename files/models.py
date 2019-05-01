from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from files import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm


db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    postzz = db.relationship('Post', backref=("userPOST"), foreign_keys=('post.c.user_id'), lazy=True)
    user1 = db.relationship('Relationship', backref=("user_ID1RELAT"), foreign_keys=('relationship.c.userID_1'), lazy=True)
    user2 = db.relationship('Relationship', backref=("user_ID2RELAT"), foreign_keys=('relationship.c.userID_2'), lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.Column(db.String(20),unique=True,nullable=False)
    commentz = db.relationship('Comment', backref=("comment_IDPOST"), foreign_keys=('comment.c.post_id'), lazy=True)


    def __repr__(self):
        return '<Post {}>'.format(self.id)

class Relationship(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'relationship'
    relation_id = db.Column(db.Integer, primary_key=True)
    userID_1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userID_2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Relationship {}>'.format(self.relation_id)

class Comment(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'comment'
    commentID = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return '<Comment {}>'.format(self.commentID)
