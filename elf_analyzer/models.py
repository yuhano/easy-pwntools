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
class ELFFileInfo:
    """
    ELF 파일의 파일 정보를 저장하는 데이터 클래스입니다.
    
    속성:
      bit_format (str): ELF 파일의 비트 형식 (예: "64-bit")
      endian (str): 엔디안 방식 (예: "LSB")
      is_pie (bool): PIE 실행 파일 여부 (True이면 PIE 실행 파일)
      cpu_arch (str): CPU 아키텍처 (예: "x86-64")
      version (str): ELF 파일의 버전 정보 (예: "version 1 (SYSV)")
      linking (str): 링크 방식 (예: "dynamically linked")
      interpreter (Optional[str]): 인터프리터 경로 (존재하지 않으면 None)
      build_id (Optional[str]): 빌드 ID (존재하지 않으면 None)
      target_os (Optional[str]): 대상 운영체제 (예: "GNU/Linux 3.2.0")
      is_stripped (bool): 심볼 제거 여부 (True이면 stripped)
    """
    bit_format: str
    endian: str
    is_pie: bool
    cpu_arch: str
    version: str
    linking: str
    interpreter: Optional[str]
    build_id: Optional[str]
    target_os: Optional[str]
    is_stripped: bool

@dataclass
class ELFAnalysisResult:
    """
    ELF 파일 분석 결과를 저장하는 데이터 클래스입니다.
    
    속성:
      file_info_raw (str): file 명령어로부터 추출한 순수한 문자열
      file_info (ELFFileInfo): ELF 파일의 기본 파일 정보를 저장하는 데이터 클래스
      checksec_info (ChecksecInfo): checksec 명령어를 통해 수집된 보안 관련 정보를 구조화된 데이터로 저장
      checksec_analysis (List[str]): checksec 정보를 기반으로 한 추가 분석 메시지 리스트
      strings_file (Optional[str]): ELF 파일에서 추출된 문자열이 저장된 파일 경로 (없으면 None)
      ropgadget_file (Optional[str]): ELF 파일에서 추출된 gadget 저장된 파일 경로 (없으면 None)
    """
    file_info_raw: str
    file_info: ELFFileInfo
    checksec_info: ChecksecInfo
    checksec_analysis: List[str] = field(default_factory=list)
    strings_file: Optional[str] = None
    ropgadget_file: Optional[str] = None

