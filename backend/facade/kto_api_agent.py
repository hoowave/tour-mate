from dotenv import load_dotenv
from datetime import datetime, timedelta
from facade.dto.kto_api_dto import KtoApiDto
import requests
import os

class KtoApiAgent:
    def __init__(self):
        load_dotenv()
        self.__API_KEY = os.getenv('KTO_API_KEY')

    def request(self, si_code, gu_code=None):
        url = "http://apis.data.go.kr/B551011/KorService2/searchFestival2"
        start_date = (datetime.today() - timedelta(days=7)).strftime("%Y%m%d")
        end_date = (datetime.today() + timedelta(days=7)).strftime("%Y%m%d")
        print(f"{start_date}일부터 {end_date}일까지의 축제 정보를 요청합니다.")
        print("===== KTO Request ... =====")
        params = {
            "numOfRows": 10,
            "pageNo": 1,
            "MobileOS": "ETC",
            "MobileApp": "TourChat",
            "arrange": "R",
            "areaCode": si_code,
            "sigunguCode": gu_code,
            "serviceKey": self.__API_KEY,
            "eventStartDate": start_date,
            "eventEndDate": end_date,
            "_type": "json"
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            items = data["response"]["body"]["items"]["item"]
            if isinstance(items, dict):
                items = [items]
        except Exception as e:
            print(f"API 요청 오류 또는 데이터 없음: {e}")
            items = []

        dto_list = [KtoApiDto.from_dict(item) for item in items]
        print("===== KTO OK! ... =====")
        return dto_list

    def get_si_code(self, region_name):
        base_url = "http://apis.data.go.kr/B551011/KorService2/areaCode2"

        params = {
            "serviceKey": self.__API_KEY,
            "MobileOS": "ETC",
            "MobileApp": "TourChat",
            "_type": "json"
        }

        r = requests.get(base_url, params=params)

        region_list = r.json()["response"]["body"]["items"]["item"]

        region_code = None

        for region in region_list:
            if region_name in region["name"]:
                region_code = region["code"]
                break

        return region_code
    
    def get_gu_code(self, si_code, region_name):
        base_url = "http://apis.data.go.kr/B551011/KorService2/areaCode2"

        params = {
            "serviceKey": self.__API_KEY,
            "MobileOS": "ETC",
            "MobileApp": "TourChat",
            "numOfRows": 25,
            "areaCode": si_code,
            "_type": "json"
        }

        response = requests.get(base_url, params=params)
        response_json = response.json()
        region_list = response_json["response"]["body"]["items"]["item"]

        region_code = None
        for region in region_list:
            if region_name.strip() == region["name"].strip():
                region_code = region["code"]
        return region_code