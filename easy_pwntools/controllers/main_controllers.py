from flask import Blueprint, redirect, render_template
import easy_pwntools.controllers.menu_controller as menu_controller
import easy_pwntools.services.main_services as main_services

bp = Blueprint(name = 'main',
               import_name = __name__, 
               url_prefix='/')

# todo : render_template 경로 설정 바꾸기

@bp.route('/', methods=['GET'])
def index():
    # todo : 향후에, 데이터베이스를 추가하면 정보에 따라 다른 페이지를 띄워줌
    return redirect('/upload')

@bp.route('/upload', methods=['GET'])
def upload():
    return render_template('main/upload.html')

@bp.route('/upload', methods=['POST'])
def upload_file():
    return main_services.upload_file()

@bp.route('/details', methods=['GET'])
def details():
    return render_template('main/details.html')

@bp.route('/details', methods=['POST'])
def input_project_information():
    return main_services.input_project_information()

@bp.route('/validate_details', methods=['GET'])
def validate_details():
    return main_services.validate_details_page()

@bp.route('/validate_details2', methods=['GET'])
def validate_details2():
    return render_template('main/validate_details2.html')