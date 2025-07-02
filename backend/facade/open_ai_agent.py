from dotenv import load_dotenv
from openai import OpenAI
import os

class OpenAIAgent:
    def __init__(self):
        load_dotenv()                                       # .env 파일에서 환경변수 로드
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')        # OPENAI_API_KEY 환경변수에서 API 키 읽기
        self.__client = OpenAI(api_key=OPENAI_API_KEY)        # OpenAI 클라이언트 초기화 (API 키 사용)

    def request(self, messages, tools):
        print("===== Request ... =====")
        response = self.__client.responses.create(
            model="gpt-4.1",
            input=messages,
            tools=tools,
        )
        print("========== OK!==========")
        return response