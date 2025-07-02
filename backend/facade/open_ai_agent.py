from dotenv import load_dotenv
from openai import OpenAI
import os

class OpenAIAgent:
    def __init__(self):
        load_dotenv()                                       # .env 파일에서 환경변수 로드
        __API_KEY = os.getenv('OPENAI_API_KEY')             # OPENAI_API_KEY 환경변수에서 API 키 읽기
        self.__client = OpenAI(api_key=__API_KEY)           # OpenAI 클라이언트 초기화 (API 키 사용)

    def request(self, messages, tools):
        print("===== Request ... =====")
        response = self.__client.responses.create(
            model="gpt-4.1",
            input=messages,
            tools=tools,
        )
        print("========== OK!==========")
        return response
    
    def get_news(self, prompt):
        print("===== Web Search Request ... =====")
        response = self.__client.responses.create(
        model="gpt-4o",
        tools=[{
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "KR",
                "city": "Seoul",
                "region": "Seoul",
            }
        }],
        input=f'''
        - {prompt} 다음 주제를 기반으로,
        - 사고, 재난, 범죄, 화재 등의 부정적 이슈는 제외하고
        - 여행지에 긍정적으로 도움이 될 만한 행사나 소식만 요약해줘.
        - 뉴스 목록을 한글로 3~5줄 이내로 요약해줘.
        ''',
        )
        print("========== Web Search OK!==========")
        return response.output_text