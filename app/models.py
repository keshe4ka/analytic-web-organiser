from app import db
from flask_login import UserMixin
import uuid


class WebUser(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=True, unique=True)
    password = db.Column(db.String(), nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password
        }


class BookmarksGroup(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=True)
    unique_url = db.Column(db.String(), nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'unique_url': self.unique_url
        }


class UserGroup(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('web_user.id', onupdate='CASCADE'), nullable=True)
    bookmarks_group_id = db.Column(db.Integer(), db.ForeignKey('bookmarks_group.id', onupdate='CASCADE'), nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bookmarks_group_id': self.bookmarks_group_id
        }


class Element(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=True)
    img_src = db.Column(db.String(), nullable=True)
    tags = db.Column(db.String(), nullable=True)
    source = db.Column(db.String(), nullable=True)
    bookmarks_group_id = db.Column(db.Integer(), db.ForeignKey('bookmarks_group.id', onupdate='CASCADE'), nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'img_src': self.img_src,
            'tags': self.tags,
            'source': self.source,
            'bookmarks_group_id': self.bookmarks_group_id
        }
