from flask import Blueprint, redirect, render_template, request, jsonify, current_app
import os


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return redirect('/upload')

@bp.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@bp.route('/upload', methods=['POST'])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "파일이 존재하지 않습니다."})
    
    file = request.files["file"]
    filename = file.filename

    if not filename:
        return jsonify({"success": False, "message": "파일 이름이 없습니다."})
    
    filename_extension = filename.split(".")[-1].lower()
    allowed_extension = ["exe", "elf"]

    if filename_extension in allowed_extension:
        file_path = os.path.join(current_app.config['UPLOAD_PATH'], file.filename)
        file.save(file_path)
        return jsonify({"success": True, "message": "업로드 성공!", "file": file.filename})
    
    return jsonify({"success": False, "message": "올바르지 않은 파일 형식입니다."})

@bp.route('/detail', methods=['GET'])
def detail():
    return render_template('detail.html')

@bp.route('/main', methods=['GET'])
def main():
    return render_template('main.html')

@bp.route('/real_main', methods=['GET'])
def real_main():
    return render_template('real_main.html')