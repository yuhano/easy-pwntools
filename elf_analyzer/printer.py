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
    print(f"{RED}[File Information]{RESET}")
    print(result.file_info)
    print()
    print(f"{BLUE}[checksec Information]{RESET}")
    print(result.checksec_info)
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
