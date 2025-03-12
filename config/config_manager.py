# config/config_manager.py
import os
import configparser

"""
사용 예제:
-----------
# elf_analyzer/analyzer.py
from config_manager import config
option2 = config.get('elf_analyzer', 'option2', fallback='default_value')
"""

# 프로젝트 루트 기준으로 config 폴더 및 설정 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'config.ini')

# 기본 설정 값 (필요에 따라 수정 가능)
DEFAULT_CONFIG = {
    'DEFAULT': {
        # 예: 'log_dir': 'logs/',
        # 예: 'debug': 'True'
    },
    'decompile': {
        'ghidra_decompile_script': 'decompile/decompile_script.py'
    },
    'elf_analyzer': {
        # 추가 옵션 가능
    },
    'ai': {
        'chatgpt_api': ''
    }, 
}

def ensure_config():
    """
    설정 파일이 존재하는지 확인하고,
    존재하지 않을 경우 기본 설정으로 생성합니다.
    """
    if not os.path.isfile(CONFIG_FILE):
        config = configparser.ConfigParser()
        for section, options in DEFAULT_CONFIG.items():
            config[section] = options
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        print(f"Default config file created: {CONFIG_FILE}")
    else:
        print("config.ini file already exists.")

def update_config():
    """
    기본 설정값에 새 항목이 추가되었을 경우,
    기존 ini 파일에 누락된 섹션이나 옵션을 추가합니다.
    "DEFAULT" 섹션은 예약되어 있으므로 별도 처리가 필요합니다.
    """
    config_obj = configparser.ConfigParser()
    config_obj.read(CONFIG_FILE)
    updated = False
    for section, options in DEFAULT_CONFIG.items():
        if section == 'DEFAULT':
            # DEFAULT 섹션은 예약되어 있으므로 옵션만 추가
            for key, value in options.items():
                if key not in config_obj['DEFAULT']:
                    config_obj['DEFAULT'][key] = value
                    updated = True
        else:
            # 해당 섹션이 없으면 추가
            if not config_obj.has_section(section):
                config_obj.add_section(section)
                updated = True
            # 옵션이 없으면 추가
            for key, value in options.items():
                if not config_obj.has_option(section, key):
                    config_obj.set(section, key, value)
                    updated = True
    if updated:
        with open(CONFIG_FILE, 'w') as configfile:
            config_obj.write(configfile)
        print(f"Config file updated with new default values: {CONFIG_FILE}")
    else:
        print("Config file is already up-to-date.")

def load_config():
    """
    설정 파일을 로드하여 configparser 객체로 반환합니다.
    설정 파일이 없으면 ensure_config()를 호출하여 기본 파일을 생성하고,
    기본 설정값에 새 항목이 추가되었을 경우 update_config()를 호출하여 자동으로 추가합니다.
    """
    ensure_config()
    update_config()
    config_obj = configparser.ConfigParser()
    config_obj.read(CONFIG_FILE)
    return config_obj

# 전역에서 사용할 config 객체
config = load_config()