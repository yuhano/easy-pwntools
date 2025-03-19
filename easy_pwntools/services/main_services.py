from flask import redirect, render_template, jsonify, request, current_app
import os

# todo : json message object화 하기

def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "파일이 존재하지 않습니다."})
    
    file = request.files["file"]
    filename = file.filename

    if not filename:
        return jsonify({"success": False, "message": "파일 이름이 없습니다."})
    
    filename_extension = filename.split(".")[-1].lower()
    allowed_extension = ["exe", "c"] # todo : 허용 가능한 파일 확장자 정하기

    if filename_extension in allowed_extension:
        file_path = os.path.join(current_app.config['UPLOAD_PATH'], file.filename)
        file.save(file_path)
        return jsonify({"success": True, "message": "업로드 성공", "file": file.filename})
    
    return jsonify({"success": False, "message": "올바르지 않은 파일 형식입니다."})

def input_project_information():
    project_info = request.get_json()
    project_name = project_info.get('projectName')
    description = project_info.get('description')
    server = project_info.get('server')
    ctfName = project_info.get('ctfName')
    isDockerFile = project_info.get('isDockerFile')
    gptApiKey = project_info.get('gptApiKey')
    fullAutoExploit = project_info.get('fullAutoExploit')
    # todo : 위 데이터를 어떻게 처리할 것인가? ( todo2 : 데이터베이스를 사용할 것인가? )
    return jsonify({"success": True, "message": "프로젝트 정보 입력 완료"})

def validate_details_page():
    return render_template('main/validate_details.html')