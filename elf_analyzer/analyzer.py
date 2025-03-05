# elf_analyzer/analyzer.py
import subprocess
import sys
import time
import os
from typing import List, Optional
from .models import ELFAnalysisResult, VulnerableFunctionResult, ChecksecInfo

class ELFAnalyzer:
    """
    ELF 파일을 분석하는 클래스입니다.
    ELF 파일의 파일 정보, checksec 정보, 문자열 추출, 취약 함수 확인 기능을 제공합니다.
    """
    def __init__(self, file_path: str):
        """
        생성자

        arguments:
          file_path (str): 분석할 ELF 파일의 경로
        """
        self.file_path = file_path
        self.file_info = ""

    def run_command(self, command: str) -> str:
        """
        주어진 쉘 명령어를 실행하고 결과 문자열을 반환합니다.

        arguments:
          command (str): 실행할 쉘 명령어

        return:
          str: 명령어 실행 결과 문자열
        """
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e}"

    def _parse_checksec_info(self, checksec_info: str) -> ChecksecInfo:
        """
        checksec 명령어 결과 문자열을 파싱하여 ChecksecInfo 데이터 클래스로 반환합니다.
        
        arguments:
          checksec_info (str): checksec 명령어의 출력 문자열
          
        return:
          ChecksecInfo: 각 항목(RELRO, Stack Canary, NX, PIE)의 상태를 포함하는 데이터 클래스 인스턴스
        """
        # RELRO 처리
        if "RELRO" in checksec_info:
            if "Partial RELRO" in checksec_info:
                relro_status = "Partial"
            elif "Full RELRO" in checksec_info:
                relro_status = "Full"
            elif "No RELRO" in checksec_info:
                relro_status = "None"
            else:
                relro_status = "Unknown"
        else:
            relro_status = "Not found"
        
        # Stack Canary 처리
        if "Stack" in checksec_info:
            if "No canary found" in checksec_info:
                stack_status = False
            else:
                stack_status = True
        else:
            stack_status = None
        
        # NX 처리
        if "NX" in checksec_info:
            if "NX enabled" in checksec_info:
                nx_status = True
            else:
                nx_status = False
        else:
            nx_status = None
        
        # PIE 처리
        if "PIE" in checksec_info:
            if "PIE enabled" in checksec_info:
                pie_status = True
            else:
                pie_status = False
        else:
            pie_status = None
        
        return ChecksecInfo(
            relro=relro_status,
            stack_canary=stack_status,
            nx=nx_status,
            pie=pie_status
        )
    
    def analyze(self) -> ELFAnalysisResult:
        """
        ELF 파일을 분석하고 결과를 ELFAnalysisResult 데이터 클래스 형태로 반환합니다.

        return:
          ELFAnalysisResult: 파일 정보, checksec 정보 및 분석 메시지를 포함한 분석 결과
        """
        file_info = self.run_command(f"file {self.file_path}")
        if "ELF" not in file_info:
            sys.exit("Error: This file is not ELF format.")
        self.file_info = file_info

        checksec_str = self.run_command(f"checksec {self.file_path}")
        checksec_info = self._parse_checksec_info(checksec_str)
        
        # checksec_analysis는 구조화된 정보를 기반으로 추가 메시지를 구성할 수 있습니다.
        checksec_analysis = [
            f"RELRO: {checksec_info.relro}",
            f"Stack Canary: {checksec_info.stack_canary}",
            f"NX: {checksec_info.nx}",
            f"PIE: {checksec_info.pie}"
        ]

        return ELFAnalysisResult(
            file_info=file_info,
            checksec_info=checksec_info,
            checksec_analysis=checksec_analysis
        )

    def save_strings(self) -> str:
        """
        ELF 파일의 strings 결과를 logs/<파일명>/strings 디렉토리에 저장하고,
        저장된 파일 경로를 반환합니다.

        return:
          str: 저장된 strings 파일의 경로
        """
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        output_dir = os.path.join("logs", base_name, "strings")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name}.strings")
        with open(output_file, "w") as f:
            process = subprocess.Popen(["strings", self.file_path],
                                       stdout=f,
                                       stderr=subprocess.PIPE,
                                       text=True)
            while process.poll() is None:
                time.sleep(0.05)
        return output_file

    def check_vulnerable_functions(self, function_names: Optional[List[str]] = None) -> List[VulnerableFunctionResult]:
        """
        ELF 파일 내의 취약 함수 존재 여부를 확인합니다.
        함수 이름 리스트가 주어지면 해당 함수들을 확인하고, 없으면 인터랙티브 모드로 입력을 받습니다.

        arguments:
          function_names (Optional[List[str]]): 확인할 함수 이름 리스트 (None인 경우 인터랙티브 모드)

        return:
          List[VulnerableFunctionResult]: 각 함수의 확인 결과를 담은 리스트
        """
        results: List[VulnerableFunctionResult] = []
        if self.file_info and "not stripped" in self.file_info:
            readelf_output = self.run_command(f"readelf -s {self.file_path}") or ""
            if function_names is None:
                while True:
                    func_name = input("Please enter function's name (q:quit): ").strip()
                    if func_name.lower() == "q":
                        break
                    found = func_name in readelf_output
                    message = f"Function '{func_name}' found in binary." if found else "Not found."
                    results.append(VulnerableFunctionResult(func_name, found, message))
            else:
                for func_name in function_names:
                    found = func_name in readelf_output
                    message = f"Function '{func_name}' found in binary." if found else "Not found."
                    results.append(VulnerableFunctionResult(func_name, found, message))
        else:
            results.append(VulnerableFunctionResult("", False, "Error: Stripped or no section header in this binary."))
        return results
