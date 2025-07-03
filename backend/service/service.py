from facade.open_ai_agent import OpenAIAgent
from facade.kto_api_agent import KtoApiAgent
from facade.csv_agent import CSVAgent
from facade.dto.csv_dto import CsvDto as CSVDto

class Service:
    def __init__(self):
        self.__open_ai_agent = OpenAIAgent()
        self.__kto_api_agent = KtoApiAgent()
        self.__csv_agent = CSVAgent()

    def request(self):
        # 머신러닝 모델을 사용하여 추천 요청
        # csv_response = self.__csv_agent.request(1,20,3) # 남성, 20대, 활동코드 3
        csv_response = CSVDto.get_sample_data()  # 샘플 데이터 사용
        print("CSV Agent Response:", csv_response)
        for csv in csv_response:
            si_kor = csv.addr2
            gu_kor = csv.addr3
            
            # 한국관광공사 API 요청
            si_code = self.__kto_api_agent.get_si_code(region_name=si_kor)
            gu_code = self.__kto_api_agent.get_gu_code(si_code=si_code, region_name=gu_kor)
            print(f"지역 코드: {si_code}, 구 코드: {gu_code}")
            kto_response = self.__kto_api_agent.request(si_code=si_code, gu_code=gu_code)
            for i, dto in enumerate(kto_response, 1):
                print(f"""
            📌 {i}번 축제
            - 이름: {dto.title}
            - 주소: {dto.addr1}
            - 연락처: {dto.tel or '정보 없음'}
            - 이미지: {dto.firstimage or '이미지 없음'}
                """)

            # OpenAI Web Search 요청
            satis = "5점 만점에 4점"
            partner = "연인"
            prompt=f"장소는 {si_kor},{gu_kor}이고, 만족도는 {satis}이며, 여행 파트너는 {partner}인 여행지 추천을 해줘."
            web_search_response = self.__open_ai_agent.get_news(prompt=prompt)
            print("Web Search Response:", web_search_response)

        # 자연어 생성

    def kto_api_test(self):
        si_code = self.__kto_api_agent.get_si_code(region_name="서울")
        gu_code = self.__kto_api_agent.get_gu_code(si_code=si_code, region_name="종로구")
        kto_response = self.__kto_api_agent.request(si_code)
        print("KTO API Response:" + str(kto_response))
        for i, dto in enumerate(kto_response, 1):
            print(f"""
        📌 {i}번 축제
        - 이름: {dto.title}
        - 주소: {dto.addr1}
        - 연락처: {dto.tel or '정보 없음'}
        - 이미지: {dto.firstimage or '이미지 없음'}
            """)