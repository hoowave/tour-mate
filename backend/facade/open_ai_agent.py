from dotenv import load_dotenv
from openai import OpenAI
from facade.dto.web_search_dto import WebSearchDto
import os
import json
import re

class OpenAIAgent:
    def __init__(self):
        load_dotenv()                                       # .env 파일에서 환경변수 로드
        __API_KEY = os.getenv('OPENAI_API_KEY')             # OPENAI_API_KEY 환경변수에서 API 키 읽기
        self.__client = OpenAI(api_key=__API_KEY)           # OpenAI 클라이언트 초기화 (API 키 사용)

    def request(self, prompt, kto_all, web_all):
        print("===== Last Response Request ... =====")

        final_prompt = f"""
        너는 여행 가이드 역할을 맡은 여행 전문가야. 아래 데이터를 종합해서 여행객에게 추천과 안내를 제공해줘.

        [모든 축제 데이터]
        {kto_all}

        [모든 최신 여행 뉴스]
        {web_all}
        

        - 위의 데이터를 기반으로 "{prompt}"에 맞춘 여행 안내문을 작성해줘.
        - 각 추천 장소나 축제에 대해 다음 정보를 포함해줘:
            - 장소명
            - 간략한 소개
            - 이미지가 있다면 이미지 URL
            - 자세한 정보를 볼 수 있는 링크(URL)
        - 긍정적인 정보만 포함하고, 사고나 범죄 등 부정적 이슈는 제외해.
        - 한글로 친근하고 부드러운 여행 가이드 톤으로 작성해줘.
        - 마치 현지에서 여행객에게 설명하듯이 위의 항목(장소명/소개/이미지/링크)을 놓치지 말고 꼭 표시해줘.
        - 추가 코드블록이나 태그는 붙이지 말고, 자연스러운 한글 문장으로만 답변해.

        예시 톤:
        "광안리 해수욕장에서는 매주 토요일 드론쇼가 펼쳐지며, 바로 옆 맛집과 카페에서 여유로운 시간을 보낼 수 있어요.
        - 장소명: 광안리 해수욕장
        - 이미지: https://example.com/img.jpg
        - 더보기: https://example.com
        "
        """
        
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
            input=final_prompt,
        )
        print("========== Last Response OK! ==========")
        return response.output_text
    
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
        - 아래와 같은 JSON 배열만 3개 정도만 출력해줘. 설명이나 다른 문장은 넣지 말고 반드시 JSON만 반환해.
        [
            {{
                "location": "장소명",
                "info": "장소 설명",
                "url": "출처 URL"
            }}
         ]
        - 반드시 JSON만 반환하고, 다른 텍스트는 출력하지 말아줘.
        ''',
        )
        raw = response.output_text.strip()

        # JSON 배열의 첫 [ 부터 마지막 ] 까지 잘라내기
        json_pattern = re.compile(r"\[.*\]", re.DOTALL)
        match = json_pattern.search(raw)
        print("===== Web Search OK! ... =====")
        if match:
            json_str = match.group()
            try:
                data = json.loads(json_str)
                dto_list = [WebSearchDto(**item) for item in data]
                return dto_list
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)
                print("잘라낸 JSON 문자열:\n", json_str)
                return []
        else:
            print("JSON 패턴을 찾지 못함:\n", raw)
            return []