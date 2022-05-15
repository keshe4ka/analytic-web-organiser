import os
from flask import Blueprint, request, jsonify, render_template, send_file
from flask_login import login_required, current_user
import os
import psycopg2

from app import db
from app import models

main = Blueprint('main', __name__)


@main.route(f'/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route(f'/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', email=current_user.email)


# @app.route(f"/sign-img/<unique_sign_url>", methods=["GET"])
# def sign_image(unique_sign_url):
#     # html_code = generate_template(unique_sign_url)
#     filename_jpg = f'{os.path.abspath(os.getcwd())}/static/{unique_sign_url}.jpg'
#     options = {'width': 800, 'disable-smart-width': ''}
#     return send_file(filename_jpg, mimetype='image/gif')

# def generate_template(unique_sign_url) -> str:
#     url = unique_sign_url
#     employee = Employee.query.filter(Employee.url == url).first()
#     employee_dict = employee.to_dict()
#     template = Template.query.get(employee.template_id)
#     html_code = template.html_code
#     return render_template_string(html_code, employee=employee_dict)
def register_blueprint(main_blueprint):
    return None
