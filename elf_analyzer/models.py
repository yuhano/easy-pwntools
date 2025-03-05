# elf_analyzer/models.py
from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ChecksecInfo:
    """
    전체 checksec 정보를 관리하는 데이터 클래스입니다.
    
    속성:
      relro (str): RELRO 상태 (예: "Partial", "Full", "None", "Unknown", "Not found")
      stack_canary (Optional[bool]): Stack Canary 상태 (True, False 또는 None)
      nx (Optional[bool]): NX 상태 (True, False 또는 None)
      pie (Optional[bool]): PIE 상태 (True, False 또는 None)
    """
    relro: str
    stack_canary: Optional[bool]
    nx: Optional[bool]
    pie: Optional[bool]

@dataclass
class ELFAnalysisResult:
    """
    ELF 파일 분석 결과를 저장하는 데이터 클래스입니다.
    
    속성:
      file_info (str): ELF 파일의 기본 파일 정보 (예: 파일 형식, 크기 등)
      checksec_info (ChecksecInfo): checksec 명령어를 통해 수집된 보안 관련 정보를 구조화된 데이터로 저장
      checksec_analysis (List[str]): checksec 정보를 기반으로 한 추가 분석 메시지 리스트
      strings_file (Optional[str]): ELF 파일에서 추출된 문자열이 저장된 파일 경로 (없으면 None)
    """
    file_info: str
    checksec_info: ChecksecInfo
    checksec_analysis: List[str] = field(default_factory=list)
    strings_file: Optional[str] = None

@dataclass
class VulnerableFunctionResult:
    function_name: str
    found: bool
    message: str
