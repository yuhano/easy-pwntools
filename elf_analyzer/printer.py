# elf_analyzer/printer.py
from typing import List
from .models import ELFAnalysisResult, VulnerableFunctionResult

def print_analysis_result(result: ELFAnalysisResult):
    """
    ELF 분석 결과를 출력합니다.

    arguments:
      result (ELFAnalysisResult): ELF 파일 분석 결과 데이터 클래스 인스턴스
    """
    RED = "\033[91m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(f"{RED}[File Information Raw]{RESET}")
    print(result.file_info_raw)
    print()
    print(f"{BLUE}[Parsed File Information]{RESET}")
    print(f"Bit Format: {result.file_info.bit_format}")
    print(f"Endian: {result.file_info.endian}")
    print(f"PIE: {result.file_info.is_pie}")
    print(f"CPU Architecture: {result.file_info.cpu_arch}")
    print(f"Version: {result.file_info.version}")
    print(f"Linking: {result.file_info.linking}")
    print(f"Interpreter: {result.file_info.interpreter}")
    print(f"Build ID: {result.file_info.build_id}")
    print(f"Target OS: {result.file_info.target_os}")
    print(f"Is Stripped: {result.file_info.is_stripped}")
    print()
    print(f"{GREEN}[checksec Information]{RESET}")
    print(f"RELRO: {result.checksec_info.relro}")
    print(f"Stack Canary: {result.checksec_info.stack_canary}")
    print(f"NX: {result.checksec_info.nx}")
    print(f"PIE: {result.checksec_info.pie}")
    print()
    print(f"{GREEN}[checksec Analysis]{RESET}")
    for msg in result.checksec_analysis:
        print(msg)
    print()
    if result.strings_file:
        print(f"Strings saved to: {result.strings_file}")
    print()

def print_vulnerable_functions(results: List[VulnerableFunctionResult]):
    """
    취약 함수 분석 결과를 출력합니다.

    arguments:
      results (List[VulnerableFunctionResult]): 취약 함수 결과 데이터 클래스 리스트
    """
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"
    print("Vulnerable Function Analysis:")
    for res in results:
        if res.function_name:
            if res.found:
                print(f"{GREEN}{res.message}{RESET}")
            else:
                print(f"{RED}{res.message}{RESET}")
        else:
            print(f"{RED}{res.message}{RESET}")
