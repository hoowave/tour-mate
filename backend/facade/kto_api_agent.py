from dotenv import load_dotenv
from datetime import datetime, timedelta
from facade.dto.kto_api_dto import KtoApiDto
import requests
import os

class KtoApiAgent:
    def __init__(self):
        load_dotenv()
        self.__API_KEY = os.getenv('KTO_API_KEY')

    def request(self, area_code):
        url = "http://apis.data.go.kr/B551011/KorService2/searchFestival2"
        start_date = (datetime.today() - timedelta(days=7)).strftime("%Y%m%d")
        end_date = (datetime.today() + timedelta(days=7)).strftime("%Y%m%d")
        print(f"{start_date}일부터 {end_date}일까지의 축제 정보를 요청합니다.")
        params = {
            "numOfRows": 10,
            "pageNo": 1,
            "MobileOS": "ETC",
            "MobileApp": "TourChat",
            "arrange": "R",
            "areaCode": area_code,
            "serviceKey": self.__API_KEY,
            "eventStartDate": start_date,
            "eventEndDate": end_date,
            "_type": "json"
        }

        response = requests.get(url, params=params)
        data = response.json()
        items = data["response"]["body"]["items"]["item"]
        dto_list = [KtoApiDto.from_dict(item) for item in items]
        return dto_list

    def get_area_codes(self, region_name, subregion_name=None):
        print(f"[DEBUG] API KEY: {self.__API_KEY}")
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
        subregion_code = None

        for region in region_list:
            if region_name in region["name"]:
                region_code = region["code"]
                break

        # Step 2: 시군구 코드 (옵션)
        if region_code and subregion_name:
            params["areaCode"] = region_code
            r2 = requests.get(base_url, params=params)
            subregion_list = r2.json()["response"]["body"]["items"]["item"]

            for sub in subregion_list:
                if subregion_name in sub["name"]:
                    subregion_code = sub["code"]
                    break

        return region_code, subregion_code