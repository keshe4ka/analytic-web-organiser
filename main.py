import joblib
from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
import sklearn
import nltk

from app.common import *
from app.models import *

main = Blueprint('main', __name__)
model = joblib.load('model.joblib')


@main.route(f'/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route(f'/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', email=current_user.email)


@main.route(f'/bookmarks_group/<int:id>', methods=['GET'])
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
    print(elements_dict, groups_dict)
    return jsonify(elements_dict), 200


@main.route(f'/bookmarks_group/<int:id>/create/<url>', methods=['POST'])
@login_required
def create_element(id, url):
    groups = db.session.query(BookmarksGroup).join(UserGroup, BookmarksGroup.id == UserGroup.bookmarks_group_id).filter(
        UserGroup.user_id == current_user.id)
    bookmarks_group = groups.filter(BookmarksGroup.id == id).first()
    element_dict = get_info_from_post(url, bookmarks_group.id, model)
    element = Element(**element_dict)
    db.session.add(element)
    db.session.commit()
    return 200


@main.route(f'/bookmarks_group/<int:id>/share', methods=['POST'])
@login_required
def share_bookmarks_group(id):
    unique_url = uuid.uuid1()
    groups = db.session.query(BookmarksGroup).join(UserGroup, BookmarksGroup.id == UserGroup.bookmarks_group_id).filter(
        UserGroup.user_id == current_user.id)
    bookmarks_group = groups.filter(BookmarksGroup.id == id).first()
    bookmarks_group.unique_url = unique_url
    db.session.add(bookmarks_group)
    db.session.commit()
    url = f'/shared_bookmarks_group/{unique_url}'
    return jsonify(url), 200


@main.route(f'/shared_bookmarks_group/<url>', methods=['GET'])
def get_shared_bookmarks_group(url):
    bookmarks_group = BookmarksGroup.query.filter(BookmarksGroup.unique_url == url).first()
    elements = Element.query.filter(Element.bookmarks_group_id == bookmarks_group.id)
    elements_dict = []
    for row in elements:
        elements_dict.append(row.to_dict())
    return jsonify(elements_dict), 200


def register_blueprint(main_blueprint):
    return None
