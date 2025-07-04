import pandas as pd
import joblib
import json
import numpy as np

def recommend_travel_places(
    gender_str: str,
    age_grp: int,
    travel_companions_num: int,
    travel_styl_1: int,
    travel_styl_2: int,
    travel_styl_3: int,
    travel_styl_4: int,
    travel_styl_5: int,
    travel_styl_6: int,
    travel_styl_7: int,
    travel_styl_8: int,
    activity_type: int, # ACTIVITY_TYPE_CD
    travel_status_accompany_str: str, # TRAVEL_STATUS_ACCOMPANY (문자열)
    # 모델 및 인코더 파일 경로 (기본값으로 설정)
    model_path: str = 'catboost_travel_satisfaction_model.joblib',
    encoders_path: str = 'label_encoders_for_catboost.joblib',
    sido_map_path: str = 'area_to_sido_map.joblib',
    sigungu_map_path: str = 'area_to_sigungu_map.joblib',
    sido_names_path: str = 'sido_change_names.json',
    feature_cols_path: str = 'model_feature_columns.joblib'
) -> pd.DataFrame:
    
    # 1. 저장된 모델 및 인코더 로드
    try:
        model = joblib.load(model_path)
        label_encoders = joblib.load(encoders_path)
        area_to_sido_map_raw = joblib.load(sido_map_path)
        area_to_sigungu_map_raw = joblib.load(sigungu_map_path)
        with open(sido_names_path, 'r', encoding='utf-8') as f:
            sido_change_names = json.load(f)
        model_feature_columns = joblib.load(feature_cols_path)
    except FileNotFoundError as e:
        print(f"Error: 필요한 파일을 찾을 수 없습니다. 경로를 확인해주세요: {e}")
        return pd.DataFrame() # 빈 DataFrame 반환
    except Exception as e:
        print(f"Error loading files: {e}")
        return pd.DataFrame()

    # 2. 사용자 입력 변환
    try:
        user_gender_encoded = label_encoders['GENDER'].transform([gender_str])[0]
        user_travel_status_accompany_encoded = label_encoders['TRAVEL_STATUS_ACCOMPANY'].transform([travel_status_accompany_str])[0]
        # ACTIVITY_TYPE_CD가 학습시 int로 인코딩됐으면 int, str로 인코딩됐으면 str로 변환 필요
        activity_type_for_encoder = activity_type
        # 아래 한 줄을 주석 해제해서 학습시 str로 인코딩했다면 사용
        # activity_type_for_encoder = str(activity_type)
        user_activity_type_encoded = label_encoders['ACTIVITY_TYPE_CD'].transform([activity_type_for_encoder])[0] 
    except ValueError as e:
        print(f"Error: 사용자 입력 중 인코딩할 수 없는 값이 있습니다. {e}")
        return pd.DataFrame()

    # 3. 사용자 고정 특성 데이터 구성
    user_fixed_data = {
        'GENDER': user_gender_encoded,
        'AGE_GRP': age_grp,
        'TRAVEL_STYL_1': travel_styl_1,
        'TRAVEL_STYL_2': travel_styl_2,
        'TRAVEL_STYL_3': travel_styl_3,
        'TRAVEL_STYL_4': travel_styl_4,
        'TRAVEL_STYL_5': travel_styl_5,
        'TRAVEL_STYL_6': travel_styl_6,
        'TRAVEL_STYL_7': travel_styl_7,
        'TRAVEL_STYL_8': travel_styl_8,
        'TRAVEL_COMPANIONS_NUM': travel_companions_num,
        'TRAVEL_STATUS_ACCOMPANY': user_travel_status_accompany_encoded,
        'ACTIVITY_TYPE_CD': user_activity_type_encoded
    }

    # 4. 모든 VISIT_AREA_NM 후보에 대한 배치 예측 준비
    # LabelEncoder의 클래스 개수만큼 인코딩 숫자 리스트 생성
    n_areas = len(label_encoders['VISIT_AREA_NM'].classes_)
    all_visit_area_nms_encoded = list(range(n_areas))
    all_candidate_data = []

    for area_encoded in all_visit_area_nms_encoded:
        row = user_fixed_data.copy()
        row['VISIT_AREA_NM'] = area_encoded
        all_candidate_data.append(row)

    # DataFrame으로 변환 (모델 학습 시 사용된 컬럼 순서 유지 중요)
    input_df_for_batch_prediction = pd.DataFrame(all_candidate_data, columns=model_feature_columns)

    # 5. 모델에 한 번에 예측 요청
    all_predicted_scores = model.predict(input_df_for_batch_prediction)

    # 6. 결과 취합 및 정렬
    recommendations = []
    for i, area_encoded in enumerate(all_visit_area_nms_encoded):
        # area_encoded는 숫자, 역변환 필요
        area_original_name = label_encoders['VISIT_AREA_NM'].inverse_transform([area_encoded])[0]

        sido_abbr = area_to_sido_map_raw.get(area_original_name, '정보 없음')
        full_sido_name = sido_change_names.get(sido_abbr, sido_abbr)

        sigungu_name = area_to_sigungu_map_raw.get(area_original_name, '정보 없음')

        recommendations.append({
            '여행지': area_original_name,
            '예상 만족도': all_predicted_scores[i],
            '시도': full_sido_name,
            '시군구': sigungu_name
        })

    recommendations_df = pd.DataFrame(recommendations)
    top_5_recommendations = recommendations_df.sort_values(by='예상 만족도', ascending=False).head(5)

    return top_5_recommendations

if __name__ == '__main__':
    # 함수 호출 예시
    user_recommendations = recommend_travel_places(
        gender_str='남',
        age_grp=20,
        travel_companions_num=0,
        travel_styl_1=4,
        travel_styl_2=4,
        travel_styl_3=4,
        travel_styl_4=4,
        travel_styl_5=4,
        travel_styl_6=4,
        travel_styl_7=4,
        travel_styl_8=4,
        activity_type=4,
        travel_status_accompany_str='나홀로 여행' # 자녀 동반 여행, 부모 동반 여행, 2인 여행(가족 외), 3인 이상 여행(가족 외), 3대 동반 여행(친척 포함)





    )

    if not user_recommendations.empty:
        print("\n--- 사용자 맞춤형 여행지 추천 결과 ---")
        print(user_recommendations.to_markdown(index=False))
    else:
        print("여행지 추천에 실패했습니다. 입력 값 또는 시스템 설정을 확인해주세요.")
