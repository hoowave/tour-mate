from catboost import CatBoostClassifier
from dotenv import load_dotenv

import os
import pandas as pd


class CatboostAgent:
    def __init__(self):
        load_dotenv()
        __RESOURCE_PATH = os.getenv('RESOURCE_PATH')
        __MODEL_PATH = os.getenv('MODEL_PATH')
        self.__MODEL_FILE_PATH = os.path.join(__RESOURCE_PATH, __MODEL_PATH)
        self.__model = CatBoostClassifier()
        self.__model.load_model(self.__MODEL_FILE_PATH)
        print(self.__MODEL_FILE_PATH)
        # 1. 모델
        #self.__loaded_model = load(self.__MODEL_FILE_PATH)

    def request(self):
        print("===== Catboost Request ... =====")
        data = pd.DataFrame({
            "age": 20,
            "gender": '남',
            "theme": ["맛집"],
            "days": [4]
        })
        pred = self.__model.predict(data)
        print("예측 결과:", pred)
        print("===== Catboost OK! =====")
        # 6. 리스트로 반환
        # return list(top5_places)