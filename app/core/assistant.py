"""
多语言助手的核心类，处理与API的交互
"""

from openai import OpenAI
from app.config import API_KEY, BASE_URL, MODE_NAME, DEFAULT_TEMPRATURE, DEFAULT_MAX_TOKENS

class MultilingualAssistant:
    """多语言助手核心类，管理与大模型的交互"""

    def __init__(self,api_key = API_KEY,base_url = BASE_URL,model = MODE_NAME):
        """初始化多语言助手，创建OpenAI实例"""
        self.client = OpenAI(api_key=api_key,base_url=base_url)
        self.model = model
        self.conversation_history = []
        self.init_system_message()

    def init_system_message(self):
        """初始化系统消息"""
        self.conversation_history = [{
            "role": "system",
            "content": """你是一个专业的多语言内容助手，精通多种语言
            能够提供高质量的翻译，摘要，校对和语言风格转换服务。
            你的输出应当自然流畅，符合目标语言的表达习惯"""
        }]
    
    def set_system_message(self,content):
        """设置或更新系统消息"""
        if self.conversation_history and self.conversation_history[0]["role"] == "system":
            self.conversation_history[0]["content"] = content
        else:
            self.conversation_history.insert(0,{
                "role": "system",
                "content": content
            })

    def add_message(self,role,content):
        """添加消息到对话历史"""
        self.conversation_history.append({"role": role,"content": content})

    def get_response(self,temperature=DEFAULT_TEMPRATURE,max_tokens=DEFAULT_MAX_TOKENS):
        """获取模型响应"""
        try:

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            self.add_message("assistant", content)
            return content
    
        except Exception as e:
            return f"发生错误：{str(e)}"
        
    def clear_history(self,keep_system=True):
        """清空对话历史，可选保留系统消息"""
        if keep_system and self.comversation_history:
            system_message = self.conversation_history[0]
            self.conversdation_history = [system_message]
        else:
            self.conversation_history = []

    def get_streaming_response(self,temperature=DEFAULT_TEMPRATURE,max_tokens=DEFAULT_MAX_TOKENS):
        """获取流式响应"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            #手机完整响应内容
            full_content = ""

            #返回生成器
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content_chunk = chunk.choices[0].delta.content
                    full_content += content_chunk
                    yield content_chunk

            #将完整响应添加到历史记录
            self.add_message("assistant",full_content)

        except Exception as e:
            yield f"发生错误：{str(e)}"
            