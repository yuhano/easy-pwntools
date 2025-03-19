## 설치 및 실행

### 1. 가상환경 설치

python -m venv .venv

### 2. 가상환경 실행

.\.venv\Scripts\activate ( Window일 경우 )

source .venv/bin/activate ( Mac/Linux일 경우 )

### 3. 라이브러리 다운로드

pip install -r requirement.txt

python -m pip install --upgrade pip ( 혹은 pip -m pip install --upgrade pip )

### 4. flask 실행

flask run

## 환경 세팅

### 포트 수정

FLASK_RUN_PORT 값을 원하는 포트로 변경 ( default : 5001 )

### 웹사이트 주소

http://localhost:5001