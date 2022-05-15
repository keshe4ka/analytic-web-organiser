from app import db
from flask_login import UserMixin


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


class Group(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=True)
    is_public = db.Column(db.Boolean(), nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'is_public': self.is_public
        }


class UserGroup(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('web_user.id', onupdate='CASCADE'), nullable=True)
    group_id = db.Column(db.Integer(), db.ForeignKey('group.id', onupdate='CASCADE'), nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id
        }


class Element(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=True)
    img_src = db.Column(db.String(), nullable=True)
    tags = db.Column(db.String(), nullable=True)
    source = db.Column(db.String(), nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'img_src': self.img_src,
            'tags': self.tags,
            'source': self.source
        }


class ElementGroup(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    element_id = db.Column(db.Integer(), db.ForeignKey('element.id', onupdate='CASCADE'), nullable=True)
    group_id = db.Column(db.Integer(), db.ForeignKey('group.id', onupdate='CASCADE'), nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'element_id': self.element_id,
            'group_id': self.group_id
        }
