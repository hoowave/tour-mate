from facade.open_ai_agent import OpenAIAgent
from facade.kto_api_agent import KtoApiAgent

class Service:
    def __init__(self):
        self.__open_ai_agent = OpenAIAgent()
        self.__kto_api_agent = KtoApiAgent()

    def request(self):
        # 머신러닝 모델을 사용하여 추천 요청


        # OpenAI Web Search 요청
        city = "부산"
        satis = "70"
        partner = "연인"
        prompt=f"장소는 {city}이고, 만족도는 {satis}이며, 여행 파트너는 {partner}인 여행지 추천을 해줘."
        web_search_response = self.__open_ai_agent.get_news(prompt=prompt)
        print("Web Search Response:", web_search_response)
        # 한국관광공사 API 요청


        # 자연어 생성