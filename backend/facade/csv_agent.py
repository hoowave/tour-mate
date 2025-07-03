from dotenv import load_dotenv
from joblib import load

import os
import pandas as pd


class CSVAgent:
    def __init__(self):
        load_dotenv()
        __RESOURCE_PATH = os.getenv('RESOURCE_PATH')
        __MODEL_PATH = os.getenv('MODEL_PATH')
        __LABEL_ENCODER_PATH = os.getenv('LABEL_ENCODER_PATH')
        self.__MODEL_FILE_PATH = os.path.join(__RESOURCE_PATH, __MODEL_PATH)
        self.__LABEL_ENCODER_FILE_PATH = os.path.join(__RESOURCE_PATH, __LABEL_ENCODER_PATH)
        # 1. 모델 & LabelEncoder 불러오기
        self.__loaded_model = load(self.__MODEL_FILE_PATH)
        self.__le = load(self.__LABEL_ENCODER_FILE_PATH)

    def request(self, gender, age_grp, activity_type_cd):
        print("===== CSV Request ... =====")
        # 2. 사용자 입력 데이터 (예: 20대 남성, 활동코드 3)
        test_input = pd.DataFrame([{
            "GENDER": gender,
            "AGE_GRP": age_grp,
            "ACTIVITY_TYPE_CD": activity_type_cd
        }])
        # 3. 확률 예측
        probas = self.__loaded_model.predict_proba(test_input)[0]
        
        # 4. 상위 5개 인덱스 추출
        top5_indices = probas.argsort()[::-1][:5]
        
        # 5. 인덱스를 실제 여행지 이름으로 변환
        top5_places = self.__le.inverse_transform(top5_indices)
        print("===== CSV OK! =====")
        # 6. 리스트로 반환
        return list(top5_places)