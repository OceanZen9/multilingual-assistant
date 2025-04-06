"""
应用程序配置模块
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基本配置类"""
    #Flask配置
    SECRET_KEY = os.getenv("SECRET_KEY","dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG","False").lower() in ("true","1","t")

    #Deepseek API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE","https://api.deepseek.com")

    #应用程序配置
    MAX_CONTENT_LENGTH = 10 *1024 *1024
    SUPPORTED_LANGUAGES = ["zh","en","ja","ko","fr","de","es","ru"]

    #日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")

class DevelopmentConfig(Config):
    "开发环境配置"
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False

#配置映射
config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
}

def get_config():
    env = os.getenv("FLASK_ENV","dev")
    return config_by_name[env]