"""
�����ļ����洢API��Կ����������
"""

import os
from dotenv import load_dotenv

# ��.env�ļ��м��ػ�������
load_dotenv()

#API����
API_KEY = os.getenv("Deepseek_API_KEY","sk-de5658f5654a41788045ebc984644728")
BASE_URL = os.getenv("Deepseek_BASE_URL","https://api.deepseek.com")
MODE_NAME = os.getenv("MODE_NAME","deepseek-chat")

#Ĭ�ϲ���
DEFAULT_TEMPRATURE = 0.7
DEFAULT_MAX_TOKENS = 1000

#֧�ֵ�����
SUPPORTED_LANGUAGES = [
    "����"��"zh",
    "Ӣ��"��"en",
    "����"��"fr",
    "����"��"de",
    "��������"��"es",
    "����"��"ru",
    "����"��"ja",
    "����"��"ko",
]

# ֧�ֵ��ı����
TEXT_STYLES = {
    "formal" : "��ʽ��רҵ�����ԣ��ʺ���ҵ��ѧ������",
    "casual" : "����ʽ����������ԣ��ʺ�������罻����",
    "creative" : "���д�������ԣ��ʺ��İ��͹�泡��",
    "technical" : "�����Ե����ԣ��ʺϿƼ���רҵ����",
    "simple": "���׶������ԣ��ʺ���ͨ�û�",
}

# רҵ����
DOMAINS = {
    "general" : "ͨ��",
    "technology" : "�Ƽ�",
    "finance" : "����",
    "medical" : "ҽ��",
    "legal" : "����",
    "education" : "����",
    "news" : "����",
    "marketing" : "Ӫ��",
    "entertainment" : "����",
}

