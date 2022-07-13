import joblib
from flask import Blueprint, jsonify, render_template, request, url_for, Response
from flask_login import login_required, current_user
import sklearn
import nltk
from werkzeug.utils import redirect

from app.common import *
from app.models import *

main = Blueprint('main', __name__)

model = joblib.load('model.joblib')


@main.route(f'/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route(f'/bookmarks_group', methods=['GET'])
@login_required
def start_page():
    group = db.session.query(BookmarksGroup).join(UserGroup,
                                                  BookmarksGroup.id == UserGroup.bookmarks_group_id).filter(
        UserGroup.user_id == current_user.id).first()
    id = group.id
    return redirect(url_for('main.group_get', id=id))


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
    return render_template('group.html', groups=groups_dict, id=id, bookmarks_group=bookmarks_group,
                           elements=elements_dict)


@main.route(f'/create_group', methods=['POST'])
@login_required
def create_group():
    title = request.form['title']
    unique_url = uuid.uuid1()
    new_group = BookmarksGroup(title=title, unique_url=unique_url)
    db.session.add(new_group)
    db.session.commit()
    user_group = UserGroup(user_id=current_user.id, bookmarks_group_id=new_group.id)
    db.session.add(user_group)
    db.session.commit()
    return redirect(url_for('main.group_get', id=new_group.id))


@main.route(f'/delete_group/<int:id>', methods=['POST'])
@login_required
def delete_group(id):
    groups = db.session.query(BookmarksGroup).join(UserGroup, BookmarksGroup.id == UserGroup.bookmarks_group_id).filter(
        UserGroup.user_id == current_user.id)
    if not groups:
        return Response(response='Forbidden', status=403)
    BookmarksGroup.query.filter(BookmarksGroup.id == id).delete()
    db.session.commit()
    return redirect(url_for('main.start_page'))


@main.route(f'/bookmarks_group/<int:id>/create', methods=['POST'])
@login_required
def create_element(id):
    url = request.form['url']
    groups = db.session.query(BookmarksGroup).join(UserGroup, BookmarksGroup.id == UserGroup.bookmarks_group_id).filter(
        UserGroup.user_id == current_user.id)
    bookmarks_group = groups.filter(BookmarksGroup.id == id).first()
    element_dict = get_info_from_post(url, bookmarks_group.id, model)
    element = Element(**element_dict)
    db.session.add(element)
    db.session.commit()
    return redirect(url_for('main.group_get', id=id))


@main.route(f'/bookmarks_group/<int:id>/delete_element/<int:el_id>', methods=['POST'])
@login_required
def delete_element(id, el_id):
    Element.query.filter(Element.id == el_id).delete()
    db.session.commit()
    return redirect(url_for('main.group_get', id=id))


@main.route(f'/shared_bookmarks_group/<url>', methods=['GET'])
def get_shared_bookmarks_group(url):
    bookmarks_group = BookmarksGroup.query.filter(BookmarksGroup.unique_url == str(url)).first()
    id = bookmarks_group.id
    elements = Element.query.filter(Element.bookmarks_group_id == id)
    elements_dict = []
    for row in elements:
        elements_dict.append(row.to_dict())
    return render_template('shared.html', bookmarks_group=bookmarks_group, elements=elements_dict)


def register_blueprint(main_blueprint):
    return None
