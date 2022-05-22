import os

from flask import Blueprint, request, jsonify, render_template, send_file
from flask_login import login_required, current_user
from sqlalchemy import and_
import psycopg2

from app import db
from app.models import *
from app.common import *

main = Blueprint('main', __name__)


@main.route(f'/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route(f'/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', email=current_user.email)


@main.route(f'/bookmarks_group/<id>', methods=['GET'])
@login_required
def group_get(id):
    groups = db.session.query(BookmarksGroup).join(UserGroup, BookmarksGroup.id == UserGroup.bookmarks_group_id).filter(
        UserGroup.user_id == current_user.id)
    bookmarks_group = groups.filter(BookmarksGroup.id == id).first()
    elements = Element.query.filter(Element.bookmarks_group_id == bookmarks_group.id)
    groups_dict = []
    elements_dict = []
    for row in groups:
        groups_dict.append(row.to_dict())
    for row in elements:
        elements_dict.append(row.to_dict())
    print(elements_dict)
    return jsonify(elements_dict), 200


@main.route(f'/bookmarks_group/<id>/create/<url>', methods=['POST'])
@login_required
def create_element(id, url):
    groups = db.session.query(BookmarksGroup).join(UserGroup, BookmarksGroup.id == UserGroup.bookmarks_group_id).filter(
        UserGroup.user_id == current_user.id)
    bookmarks_group = groups.filter(BookmarksGroup.id == id).first()
    element_dict = get_info_from_post(url, bookmarks_group.id)
    element = Element(**element_dict)
    db.session.add(element)
    db.session.commit()
    return 200


def register_blueprint(main_blueprint):
    return None
