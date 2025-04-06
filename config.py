"""
Ӧ�ó�������ģ��
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """����������"""
    #Flask����
    SECRET_KEY = os.getenv("SECRET_KEY","dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG","False").lower() in ("true","1","t")

    #Deepseek API����
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE","https://api.deepseek.com")

    #Ӧ�ó�������
    MAX_CONTENT_LENGTH = 10 *1024 *1024
    SUPPORTED_LANGUAGES = ["zh","en","ja","ko","fr","de","es","ru"]

    #��־����
    LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")

class DevelopmentConfig(Config):
    "������������"
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """���Ի�������"""
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """������������"""
    DEBUG = False
    TESTING = False

#����ӳ��
config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
}

def get_config():
    env = os.getenv("FLASK_ENV","dev")
    return config_by_name[env]