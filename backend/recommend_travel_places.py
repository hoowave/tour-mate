import pandas as pd
import joblib
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

def recommend_travel_places(
    gender_str: str,
    age_grp: int,
    activity_type: int,
    
    # 디폴트 값 설정
    travel_companions_num: int = 0,
    travel_styl_1: int = 4,
    travel_styl_2: int = 4,
    travel_styl_3: int = 4,
    travel_styl_4: int = 4,
    travel_styl_5: int = 4,
    travel_styl_6: int = 4,
    travel_styl_7: int = 4,
    travel_styl_8: int = 4,
    travel_status_accompany_str: str = '나홀로 여행',

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
    'ACTIVITY_TYPE_CD': user_activity_type_encoded}


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



def show_graph(top_5_recommendations, filepath):
    # 한글 폰트 및 마이너스 깨짐 방지 설정
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    # CSV 파일에서 데이터프레임 불러오기
    df = pd.read_csv(filepath)
    # 추천 결과에서 여행지명 리스트 추출
    recommend_areas = top_5_recommendations['여행지'].tolist()

    # 성별/연령대별 여행지 만족도 요약 함수
    def summarize_by_gender_age(df, recommend_areas):
        # 추천 여행지에 해당하는 데이터만 필터링
        df_filtered = df[df['VISIT_AREA_NM'].isin(recommend_areas)]
        # 여행지, 성별, 연령대별 평균 만족도와 방문 횟수 집계
        summary = df_filtered.groupby(['VISIT_AREA_NM', 'GENDER', 'AGE_GRP']).agg(
            avg_satisfaction=('DGSTFN', 'mean'),
            count_visits=('DGSTFN', 'count')
        ).reset_index()
        # 여행지별 전체 방문 횟수 집계
        total_visits = df_filtered.groupby(['VISIT_AREA_NM']).size().reset_index(name='total_visits')
        # 요약 데이터에 전체 방문 횟수 결합
        summary = summary.merge(total_visits, on='VISIT_AREA_NM')
        # 성별/연령대별 방문 비율 계산
        summary['visit_ratio'] = summary['count_visits'] / summary['total_visits']
        return summary

    # 요약 데이터프레임 생성
    summary_df = summarize_by_gender_age(df, recommend_areas)
    # 성별, 연령대 한글 라벨로 변환
    gender_map = {'남': '남', '여': '여'}
    age_map = {20: '20대', 30: '30대', 40: '40대', 50: '50대', 60: '60대'}
    summary_df['성별'] = summary_df['GENDER'].map(gender_map)
    summary_df['연령대'] = summary_df['AGE_GRP'].map(age_map)

    # 5개 여행지별 subplot 생성 (세로로 5개)
    fig, axes = plt.subplots(5, 1, figsize=(6, 40), sharey=True)
    sns.set_style('whitegrid')

    # 각 추천 여행지별로 바플롯 그리기
    for i, area in enumerate(recommend_areas):
        ax = axes[i]
        # 해당 여행지 데이터만 선택
        data = summary_df[summary_df['VISIT_AREA_NM'] == area]
        # 연령대별, 성별 평균 만족도 바플롯
        sns.barplot(x='연령대', y='avg_satisfaction', hue='성별', data=data, ax=ax, palette='pastel')
        ax.set_title(area)         # 여행지명 타이틀
        ax.set_ylim(3, 6)          # y축 범위 고정
        ax.set_xlabel('')          # x축 라벨 제거
        if i == 0:
            ax.set_ylabel('평균 만족도')
        else:
            ax.set_ylabel('')
        # 마지막 subplot에만 범례 표시
        if i == len(recommend_areas) - 1:
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles=handles, labels=labels, title='성별', loc='upper right')
        else:
            ax.get_legend().remove()
        # 각 막대 위에 값(평균 만족도) 표시
        for p in ax.patches:
            height = p.get_height()
            if not np.isnan(height):
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2, height),
                            ha='center', va='bottom', fontsize=10, color='black', rotation=0)

    # 전체 그래프 제목 설정
    plt.suptitle('추천 여행지별 성별·연령대별 평균 만족도', fontproperties="Malgun Gothic", fontsize=18)
    # subplot 간격 조정
    plt.subplots_adjust(top=0.92, hspace=0.1)

    # 이미지를 버퍼에 저장 (웹에서 활용 가능)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf


if __name__ == '__main__':
    # 1. 추천 실행
    user_recommendations = recommend_travel_places(
        gender_str='남',
        age_grp=20,
        activity_type=4,
    )

    if not user_recommendations.empty:
        print("\n--- 사용자 맞춤형 여행지 추천 결과 ---")
        print(user_recommendations.to_markdown(index=False))

        # 2. 시각화 실행 (csv 파일 경로 입력)
        csv_path = 'backend/final_file_cleaned.csv' 
        img_buf = show_graph(user_recommendations, csv_path)

    else:
        print("여행지 추천에 실패했습니다. 입력 값 또는 시스템 설정을 확인해 주세요.")