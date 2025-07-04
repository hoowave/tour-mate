from facade.open_ai_agent import OpenAIAgent
from facade.kto_api_agent import KtoApiAgent
from facade.catboost_agent.recommend_travel_places import recommend_travel_places
from facade.catboost_agent.recommend_travel_places import show_graph
from facade.dto.recommandtion_dto import RecommendationDto
from interfaces.dto.request_dto import RequestDto
import time
import os

class Service:
    def __init__(self):
        self.__open_ai_agent = OpenAIAgent()
        self.__kto_api_agent = KtoApiAgent()
        self.__df = None

    def request(self, request_dto: RequestDto):
        start_total = time.time()
        # 머신러닝 모델을 사용하여 추천 요청
        start_model = time.time()
        recommend_response = self.__get_recommendation(request_dto.gender,request_dto.age,request_dto.theme)
        end_model = time.time()
        print(f"[소요시간] 추천 모델: {end_model - start_model:.3f}초")
        print(f"====={request_dto.age}대 {request_dto.gender}의 =====")
        for recommend in recommend_response:
            print(f"추천 여행지:{recommend.place_name}, 예상 만족도: {recommend.expected_satisfaction}, 시도: {recommend.sido}, 시군구: {recommend.sigungu}")
        # ------------------------------------------------------

        kto_all = []
        web_all = []
        start_external = time.time()
        for recommend in recommend_response:
            si_kor = recommend.sido
            gu_kor = recommend.sigungu
            
            # 한국관광공사 API 요청
            si_code = self.__kto_api_agent.get_si_code(region_name=si_kor)
            gu_code = self.__kto_api_agent.get_gu_code(si_code=si_code, region_name=gu_kor)
            print(f"시: {si_kor}, 구: {gu_kor}")
            print(f"지역 코드: {si_code}, 구 코드: {gu_code}")
            kto_response = self.__kto_api_agent.request(si_code=si_code, gu_code=gu_code)
            kto_all.extend(kto_response)

            # OpenAI Web Search 요청
            prompt=f"장소는 {si_kor},{gu_kor}이고, 예상 만족도는 {recommend.expected_satisfaction}인 여행지 추천을 해줘."
            web_search_response = self.__open_ai_agent.get_news(prompt=prompt)
            web_all.append(web_search_response)
        end_external = time.time()
        print(f"[소요시간] 한국관광공사+웹검색: {end_external - start_external:.3f}초")
        start_final = time.time()
        prompt=f'''
            - {request_dto.duration}일 동안,
            - {request_dto.message}에 맞는 여행지를 추천해줘.
            '''
        last_response = self.__open_ai_agent.request(
            prompt=prompt,
            kto_all=kto_all,
            web_all=web_all
        )
        end_final = time.time()
        print(f"[소요시간] 최종 OpenAI 요청: {end_final - start_final:.3f}초")

        # 4) 총 소요
        end_total = time.time()
        print(f"[소요시간] 총합: {end_total - start_total:.3f}초")
        return last_response

    def __get_recommendation(self, gender, age, activity_type):
        df = recommend_travel_places(
            gender_str=gender,
            age_grp=age,
            activity_type=activity_type,
        )
        self.__df = df
        dto_list = [
            RecommendationDto(
                place_name=row["여행지"],
                expected_satisfaction=row["예상 만족도"],
                sido=row["시도"],
                sigungu=row["시군구"]
            )
            for _, row in df.iterrows()
        ]
        return dto_list

    # 테스트용
    def graph(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "final_file_cleaned.csv")
        print(f"CSV Path: {csv_path}")
        if(self.__df is None):
            print("최초 추천을 먼저 요청해주세요.")
            return None
        img_buf = show_graph(self.__df, csv_path)
        return img_buf