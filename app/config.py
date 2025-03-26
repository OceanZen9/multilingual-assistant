"""
配置文件，存储API密钥和其他设置
"""

import os
from dotenv import load_dotenv

# 从.env文件中加载环境变量
load_dotenv()

#API设置
API_KEY = os.getenv("Deepseek_API_KEY","sk-de5658f5654a41788045ebc984644728")
BASE_URL = os.getenv("Deepseek_BASE_URL","https://api.deepseek.com")
MODE_NAME = os.getenv("MODE_NAME","deepseek-chat")

#默认参数
DEFAULT_TEMPRATURE = 0.7
DEFAULT_MAX_TOKENS = 1000

#支持的语言
SUPPORTED_LANGUAGES = [
    "中文"："zh",
    "英文"："en",
    "法文"："fr",
    "德文"："de",
    "西班牙文"："es",
    "俄文"："ru",
    "日文"："ja",
    "韩文"："ko",
]

# 支持的文本风格
TEXT_STYLES = {
    "formal" : "正式、专业的语言，适合商业和学术场景",
    "casual" : "非正式、随意的语言，适合聊天和社交场景",
    "creative" : "富有创意的语言，适合文案和广告场景",
    "technical" : "技术性的语言，适合科技和专业场景",
    "simple": "简单易懂的语言，适合普通用户",
}

# 专业领域
DOMAINS = {
    "general" : "通用",
    "technology" : "科技",
    "finance" : "金融",
    "medical" : "医疗",
    "legal" : "法律",
    "education" : "教育",
    "news" : "新闻",
    "marketing" : "营销",
    "entertainment" : "娱乐",
}

