from flask import Blueprint, redirect, render_template
import easy_pwntools.services.main_services as main_services

bp = Blueprint(name = 'main',
               import_name = __name__, 
               url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return redirect('/upload')

@bp.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@bp.route('/upload', methods=['POST'])
def upload_file():
    return main_services.upload_file()

@bp.route('/details', methods=['GET'])
def detail():
    return render_template('details.html')

@bp.route('/main', methods=['GET'])
def main():
    return render_template('main.html')

@bp.route('/real_main', methods=['GET'])
def real_main():
    return render_template('real_main.html')