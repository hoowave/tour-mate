from facade.open_ai_agent import OpenAIAgent
from facade.kto_api_agent import KtoApiAgent
from facade.csv_agent import CSVAgent
from facade.dto.csv_dto import CsvDto as CSVDto
from interfaces.dto.request_dto import RequestDto

class Service:
    def __init__(self):
        self.__open_ai_agent = OpenAIAgent()
        self.__kto_api_agent = KtoApiAgent()
        self.__csv_agent = CSVAgent()

    def request(self, request_dto: RequestDto):
        # 머신러닝 모델을 사용하여 추천 요청
        # csv_response = self.__csv_agent.request(1,20,3) # 남성, 20대, 활동코드 3
        csv_response = CSVDto.get_sample_data()  # 샘플 데이터 사용
        print("CSV Agent Response:", csv_response)
        kto_all = []
        web_all = []
        for csv in csv_response:
            si_kor = csv.addr2
            gu_kor = csv.addr3
            
            # 한국관광공사 API 요청
            si_code = self.__kto_api_agent.get_si_code(region_name=si_kor)
            gu_code = self.__kto_api_agent.get_gu_code(si_code=si_code, region_name=gu_kor)
            print(f"시: {si_kor}, 구: {gu_kor}")
            print(f"지역 코드: {si_code}, 구 코드: {gu_code}")
            kto_response = self.__kto_api_agent.request(si_code=si_code, gu_code=gu_code)
            kto_all.extend(kto_response)

            # OpenAI Web Search 요청
            satis = "5점 만점에 4점"
            partner = "연인"
            prompt=f"장소는 {si_kor},{gu_kor}이고, 만족도는 {satis}이며, 여행 파트너는 {partner}인 여행지 추천을 해줘."
            web_search_response = self.__open_ai_agent.get_news(prompt=prompt)
            web_all.append(web_search_response)

        satis = "5점 만점에 4점"
        partner = "연인"
        prompt=f'''

            - 만족도는 {satis}이며,
            - 여행 파트너는 {partner}라면,
            - {request_dto.duration}일 동안,
            - {request_dto.message}에 맞는 여행지를 추천해줘.
            '''
        last_response = self.__open_ai_agent.request(
            prompt=prompt,
            kto_all=kto_all,
            web_all=web_all
        )
        return last_response



    # 테스트용
    def test(self):
        # OpenAI Web Search 요청
        satis = "5점 만점에 4점"
        partner = "연인"
        prompt=f"장소는 부산,수영구이고, 만족도는 {satis}이며, 여행 파트너는 {partner}인 여행지 추천을 해줘."
        web_search_response = self.__open_ai_agent.get_news(prompt=prompt)
        print("Web Search Response:", web_search_response)