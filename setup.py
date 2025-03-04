import os
import requests
import subprocess

def create_folders():
    """
    projects와 logs 폴더를 생성합니다.
    """
    folders = ['./projects', './logs']
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)
            print(f"[+] '{folder}' 폴더 생성 완료.")
        else:
            print(f"[-] '{folder}' 폴더가 이미 존재합니다.")

def setup_virtualenv():
    """
    venv를 생성하고, requirements.txt에 명시된 패키지들을 설치합니다.
    """
    venv_dir = 'venv'
    if not os.path.exists(venv_dir):
        print("[*] 가상환경(venv) 생성 중...")
        subprocess.run(["python3", "-m", "venv", venv_dir], check=True)
    else:
        print("[*] 가상환경(venv)가 이미 존재합니다.")

    # 운영체제에 따라 pip 실행파일 경로 설정
    pip_path = os.path.join(venv_dir, "bin", "pip")
    if os.name == "nt":
        pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")

    if os.path.exists("requirements.txt"):
        print("[*] requirements.txt에 명시된 패키지 설치 중...")
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    else:
        print("[!] requirements.txt 파일이 존재하지 않습니다.")

def setup_ghidra():
    """
    최신 Ghidra를 다운로드하고 압축 해제한 후,
    필요한 폴더들을 생성합니다.
    """
    print("[*] Checking for existing ghidra folder...")
    if os.path.exists('./ghidra') and os.listdir('./ghidra'):
        print("Ghidra already exists.")
        return

    print("[*] Loading ghidra release info from GitHub...")
    api_url = "https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/latest"
    response = requests.get(api_url)
    response.raise_for_status()
    release_data = response.json()

    zip_url = next(asset["browser_download_url"]
                   for asset in release_data["assets"]
                   if asset["name"].endswith(".zip"))

    print("[*] Downloading latest released ghidra zip...")
    zip_response = requests.get(zip_url, stream=True)
    zip_response.raise_for_status()
    zip_path = './ghidra_latest.zip'
    with open(zip_path, "wb") as f:
        for chunk in zip_response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("[*] Unzipping ghidra_latest.zip...")
    extract_path = './ghidra'
    command = f"unzip {zip_path} -d {extract_path}"
    subprocess.run(command, shell=True, check=True)

    if os.path.exists(zip_path):
        os.remove(zip_path)

    create_folders()

    print("[*] Finished setup.")

if __name__ == '__main__':
    setup_ghidra()
    # setup_virtualenv()
