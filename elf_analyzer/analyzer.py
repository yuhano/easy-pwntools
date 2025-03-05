# elf_analyzer/analyzer.py
import subprocess
import sys
import time
import os
from typing import List, Optional
from .models import ELFAnalysisResult, ChecksecInfo, ELFFileInfo

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
        self.analysis_result = None

    def _run_command(self, command: str) -> str:
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

    def _parse_file_info(self, file_info_str: str) -> ELFFileInfo:
        """
        file 명령어의 출력 문자열을 파싱하여 ELFFileInfo 데이터 클래스로 반환합니다.
        
        매개변수:
          file_info_str (str): file 명령어의 출력 문자열
          
        반환값:
          ELFFileInfo: 파싱된 파일 정보 데이터 클래스 인스턴스
        """
        try:
            _, info = file_info_str.split(":", 1)
        except ValueError:
            info = file_info_str
        info = info.strip()
        tokens = [token.strip() for token in info.split(",")]
        
        # 토큰 0: "ELF 64-bit LSB pie executable" 등을 파싱
        first_token = tokens[0]  # 예: "ELF 64-bit LSB pie executable"
        parts = first_token.split()
        bit_format = parts[1] if len(parts) > 1 else ""
        endian = parts[2] if len(parts) > 2 else ""
        is_pie = "pie" in first_token.lower()
        
        # 토큰 1: CPU 아키텍처
        cpu_arch = tokens[1] if len(tokens) > 1 else ""
        
        # 토큰 2: 버전 정보
        version = tokens[2] if len(tokens) > 2 else ""
        
        # 토큰 3: 링크 방식
        linking = tokens[3] if len(tokens) > 3 else ""
        
        # 토큰 4: 인터프리터 (존재하면)
        interpreter = None
        if len(tokens) > 4 and tokens[4].startswith("interpreter"):
            interpreter = tokens[4][len("interpreter"):].strip()
        
        # 토큰 5: BuildID (존재하면)
        build_id = None
        if len(tokens) > 5 and tokens[5].startswith("BuildID"):
            parts_build = tokens[5].split("=", 1)
            if len(parts_build) == 2:
                build_id = parts_build[1].strip()
        
        # 토큰 6: 대상 운영체제 (존재하면, "for ..."로 시작)
        target_os = None
        if len(tokens) > 6 and tokens[6].lower().startswith("for"):
            target_os = tokens[6][len("for"):].strip()
        
        # 토큰 7: 심볼 제거 여부 (존재하면)
        is_stripped = True
        if len(tokens) > 7:
            token7 = tokens[7].lower()
            if "not stripped" in token7:
                is_stripped = False
            elif "stripped" in token7:
                is_stripped = True
        
        return ELFFileInfo(
            bit_format=bit_format,
            endian=endian,
            is_pie=is_pie,
            cpu_arch=cpu_arch,
            version=version,
            linking=linking,
            interpreter=interpreter,
            build_id=build_id,
            target_os=target_os,
            is_stripped=is_stripped
        )
    
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
        if self.analysis_result is None:
            raw_file_info = self._run_command(f"file {self.file_path}")
            file_info_data = self._parse_file_info(raw_file_info)

            checksec_str = self._run_command(f"checksec {self.file_path}")
            checksec_info = self._parse_checksec_info(checksec_str)

            checksec_analysis = [
                f"RELRO: {checksec_info.relro}",
                f"Stack Canary: {checksec_info.stack_canary}",
                f"NX: {checksec_info.nx}",
                f"PIE: {checksec_info.pie}"
            ]

            strings_file = self._save_strings()
            
            self.analysis_result = ELFAnalysisResult(
                file_info_raw=raw_file_info,
                file_info=file_info_data,
                checksec_info=checksec_info,
                checksec_analysis=checksec_analysis,
                strings_file=strings_file
            )
        return self.analysis_result

    def _save_strings(self) -> str:
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
