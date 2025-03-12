from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__, static_folder='.')  # 현재 디렉토리에서 HTML 파일 제공
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def serve_upload():
    return send_from_directory('.', 'upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "파일이 포함되지 않았습니다."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "선택된 파일이 없습니다."}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        file.save(filepath)
        return jsonify({"message": "Upload successful", "filepath": filepath, "filename": file.filename})
    except Exception as e:
        return jsonify({"error": f"파일 저장 중 오류 발생: {str(e)}"}), 500

@app.route('/checksec', methods=['GET'])
def run_checksec():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"stdout": "파일명이 제공되지 않음"}), 400

    filepath = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))  # 절대 경로 사용

    if not os.path.exists(filepath):
        return jsonify({"stdout": f"파일이 존재하지 않음: {filepath}"}), 400

    try:
        command = ["checksec", "--file=" + filepath]
        result = subprocess.run(command, capture_output=True, text=True)
        return jsonify({"stdout": result.stdout.strip(), "stderr": result.stderr.strip()})  # 결과 데이터 정리
    except Exception as e:
        return jsonify({"stdout": f"checksec 실행 중 오류 발생: {str(e)}"}), 500

@app.route('/strings', methods=['GET'])
def get_strings():
    """strings 실행 결과를 읽어와서 반환"""
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"stdout": "❌ 파일명이 제공되지 않음"}), 400

    filepath = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))
    strings_filepath = f"{filepath}.strings"

    if not os.path.exists(filepath):
        return jsonify({"stdout": f"❌ 파일이 존재하지 않음: {filepath}"}), 400

    try:
        # strings 실행하여 결과를 저장
        command = ["strings", filepath]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if not result.stdout.strip():
            return jsonify({"stdout": "❌ strings 실행 결과 없음!"}), 400

        # 결과를 .strings 파일로 저장
        with open(strings_filepath, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        return jsonify({"stdout": result.stdout.strip()})
    except Exception as e:
        return jsonify({"stdout": f"❌ strings 실행 중 오류 발생: {str(e)}"}), 500

@app.route('/read_strings', methods=['GET'])
def read_strings_file():
    """저장된 .strings 파일을 읽어와서 반환"""
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"stdout": "❌ 파일명이 제공되지 않음"}), 400

    strings_filepath = os.path.abspath(os.path.join(UPLOAD_FOLDER, f"{filename}.strings"))

    if not os.path.exists(strings_filepath):
        return jsonify({"stdout": f"❌ .strings 파일이 존재하지 않음: {strings_filepath}"}), 400

    try:
        with open(strings_filepath, "r", encoding="utf-8") as f:
            file_contents = f.read()

        if not file_contents.strip():
            return jsonify({"stdout": "❌ .strings 파일이 비어 있음"}), 400

        return jsonify({"stdout": file_contents.strip()})
    except Exception as e:
        return jsonify({"stdout": f"❌ .strings 파일 읽기 오류 발생: {str(e)}"}), 500



# 정적 파일 제공 (detail.html 포함)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
