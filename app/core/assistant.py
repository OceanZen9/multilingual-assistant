"""
���������ֵĺ����࣬������API�Ľ���
"""

from openai import OpenAI
from app.config import API_KEY, BASE_URL, MODE_NAME, DEFAULT_TEMPRATURE, DEFAULT_MAX_TOKENS

class MultilingualAssistant:
    """���������ֺ����࣬�������ģ�͵Ľ���"""

    def __init__(self,api_key = API_KEY,base_url = BASE_URL,model = MODE_NAME):
        """��ʼ�����������֣�����OpenAIʵ��"""
        self.client = OpenAI(api_key=api_key,base_url=base_url)
        self.model = model
        self.conversation_history = []
        self.init_system_message()

    def init_system_message(self):
        """��ʼ��ϵͳ��Ϣ"""
        self.conversation_history = [{
            "role": "system",
            "content": """����һ��רҵ�Ķ������������֣���ͨ��������
            �ܹ��ṩ�������ķ��룬ժҪ��У�Ժ����Է��ת������
            ������Ӧ����Ȼ����������Ŀ�����Եı��ϰ��"""
        }]
    
    def set_system_message(self,content):
        """���û����ϵͳ��Ϣ"""
        if self.conversation_history and self.conversation_history[0]["role"] == "system":
            self.conversation_history[0]["content"] = content
        else:
            self.conversation_history.insert(0,{
                "role": "system",
                "content": content
            })

    def add_message(self,role,content):
        """�����Ϣ���Ի���ʷ"""
        self.conversation_history.append({"role": role,"content": content})

    def get_response(self,temperature=DEFAULT_TEMPRATURE,max_tokens=DEFAULT_MAX_TOKENS):
        """��ȡģ����Ӧ"""
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
            return f"��������{str(e)}"
        
    def clear_history(self,keep_system=True):
        """��նԻ���ʷ����ѡ����ϵͳ��Ϣ"""
        if keep_system and self.comversation_history:
            system_message = self.conversation_history[0]
            self.conversdation_history = [system_message]
        else:
            self.conversation_history = []

    def get_streaming_response(self,temperature=DEFAULT_TEMPRATURE,max_tokens=DEFAULT_MAX_TOKENS):
        """��ȡ��ʽ��Ӧ"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            #�ֻ�������Ӧ����
            full_content = ""

            #����������
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content_chunk = chunk.choices[0].delta.content
                    full_content += content_chunk
                    yield content_chunk

            #��������Ӧ��ӵ���ʷ��¼
            self.add_message("assistant",full_content)

        except Exception as e:
            yield f"��������{str(e)}"
            