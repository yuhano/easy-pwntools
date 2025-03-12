#!/usr/bin/env python3

import sys
import glob
import subprocess
import os
from config.config_manager import config

def run_decompile(input_file):
    script_path = config.get('decompile', 'ghidra_decompile_script')

    if not os.path.exists(script_path):
        print(f"Error: {script_path} not exist")
        sys.exit(1)
    
    # ghidra 디렉토리 내의 analyzeHeadless 실행 파일 찾기
    matches = glob.glob('./ghidra/*/support/analyzeHeadless')
    if not matches:
        print("Cannot find the analyzeHeadless file.")
        sys.exit(1)
    analyze_headless = matches[0]
    
    # 실행할 명령어 구성
    command = [
        analyze_headless,
        "./projects",
        "decompile",
        "-import", input_file,
        "-deleteProject",
        "-overwrite",
        "-postScript", script_path
    ]
    
    # 명령어 실행
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)
        sys.exit(e.returncode)

def main():
    # 명령행 인자 확인
    if len(sys.argv) < 2:
        print("Usage: {} <input file>".format(sys.argv[0]))
        sys.exit(1)
    input_file = sys.argv[1]
    
    # 분리된 함수 호출
    run_decompile(input_file)

if __name__ == '__main__':
    main()
