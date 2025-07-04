import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from catboost import CatBoostRegressor, Pool
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import seaborn as sns
import os
import io



# 데이터 전처리 함수 정의
def preprocess_data(df):
    """
    데이터 전처리 함수
    - 결측치 제거, 필요한 컬럼만 추출, 범주형 변수 인코딩, 중복 제거, 학습/테스트 분할, Pool 생성까지 수행
    - 반환값: train_pool, test_pool, label_encoders, X, y, df_ml
    """

    # 도로명 주소 관련 데이터 정제는 따로 진행 -> final_file_cleaned.csv 5팀 자료 공유 파일에 업로드

    # 추가 불필요한 행 삭제
    df = df[~df['VISIT_AREA_NM'].str.contains('주차장|휴게소|친척|지인|친정|터미널|매표소|어머니 집|형님 집|정류장|공항|댁', na=False)]

    # 사용할 feature 리스트 정의
    selected_features = [
        'GENDER', 'AGE_GRP',
        'TRAVEL_STYL_1', 'TRAVEL_STYL_2', 'TRAVEL_STYL_3', 'TRAVEL_STYL_4',
        'TRAVEL_STYL_5', 'TRAVEL_STYL_6', 'TRAVEL_STYL_7', 'TRAVEL_STYL_8',
        'TRAVEL_COMPANIONS_NUM', 'TRAVEL_STATUS_ACCOMPANY', 'VISIT_AREA_NM',
        'ACTIVITY_TYPE_CD', 'DGSTFN'
    ]
    # 필요한 컬럼만 복사
    df_ml = df[selected_features].copy()
    # 만족도(DGSTFN)와 활동코드(ACTIVITY_TYPE_CD) 결측치 제거
    df_ml = df_ml.dropna(subset=['DGSTFN', 'ACTIVITY_TYPE_CD'])
    # 활동코드 컬럼을 정수형으로 변환 (모델 입력을 위해)
    df_ml['ACTIVITY_TYPE_CD'] = df_ml['ACTIVITY_TYPE_CD'].astype(int)

    # 범주형 변수 인코딩 (문자열을 숫자로 변환)
    label_encoders = {}
    categorical_cols = ['GENDER', 'TRAVEL_STATUS_ACCOMPANY', 'VISIT_AREA_NM', 'ACTIVITY_TYPE_CD']
    for col in categorical_cols:
        le = LabelEncoder()
        df_ml[col] = le.fit_transform(df_ml[col])
        label_encoders[col] = le  # 나중에 역변환 및 예측 입력에 사용

    # VISIT_AREA_NM(여행지명)별 데이터가 2개 이상인 경우만 남김 (데이터 불균형 방지)
    counts = df_ml['VISIT_AREA_NM'].value_counts()
    df_ml = df_ml[df_ml['VISIT_AREA_NM'].isin(counts[counts >= 2].index)]

    # 완전히 동일한 행 중복 제거 (데이터 클린업)
    df_ml = df_ml.drop_duplicates()

    # 피처(X)와 타겟(y) 분리
    X = df_ml.drop('DGSTFN', axis=1)
    y = df_ml['DGSTFN']

    # 학습/테스트 데이터 분할 (20% 테스트)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # CatBoost에서 범주형 변수의 컬럼 인덱스 지정 (숫자가 아니라 인덱스)
    categorical_features_indices = [X.columns.get_loc(col) for col in categorical_cols if col in X.columns]

    # CatBoost Pool 객체 생성 (범주형 인덱스 포함)
    train_pool = Pool(X_train, y_train, cat_features=categorical_features_indices)
    test_pool = Pool(X_test, y_test, cat_features=categorical_features_indices)

    return train_pool, test_pool, label_encoders, X, y, df_ml, X_test, y_test

# LabelEncoder 안전 인코딩 함수
def safe_label_encode(le, value):
    """
    LabelEncoder로 변환할 때, 학습에 없던 값이 들어오면 예외 없이 안전하게 처리
    - le: LabelEncoder 객체
    - value: 변환할 값(문자열)
    """
    if value in le.classes_:
        return le.transform([value])[0]
    elif '기타' in le.classes_:
        return le.transform(['기타'])[0]
    else:
        # '기타'도 없으면 0번 인덱스로 매핑 (임시방편)
        return 0

# 시도명 표준화 함수 -> 추후 API input data가 되기 때
province_map = {
    '서울특별시': '서울',
    '인천광역시': '인천',
    '대전광역시': '대전',
    '대구광역시': '대구',
    '부산광역시': '부산',
    '광주광역시': '광주',
    '울산광역시': '울산',
    '세종': '세종특별자치시',
    '경기': '경기도',
    '강원': '강원특별자치도',
    '충북': '충청북도',
    '충남': '충청남도',
    '경북': '경상북도',
    '경남': '경상남도',
    '전북': '전북특별자치도',
    '전남': '전라남도',
    '제주특별자치도': '제주도'
}

def standardize_province(addr_str):
    """
    도로명 주소에서 시도명을 추출해 표준화된 이름으로 변환
    - addr_str: 도로명 주소 문자열
    """
    for short, full in province_map.items():
        if addr_str.startswith(short):
            return full
    return addr_str  # 매칭 안 되면 원본 반환

# 예측 예외 처리 함수
def predict_with_exception_handling(model, input_df):
    """
    모델 예측 시 예외가 발생해도 전체 코드가 멈추지 않도록 처리
    - model: 학습된 모델
    - input_df: 예측할 DataFrame
    """
    try:
        preds = model.predict(input_df)
        return preds
    except Exception as e:
        print(f"예측 중 오류 발생: {e}")
        return [0] * len(input_df)

# 추천 함수
def recommend_top_areas(
    user_input_dict, model, X_columns, all_visit_area_nms, label_encoders,
    area_to_address_map, area_to_address_map2, top_n=5
):
    """
    사용자 입력값을 받아 모든 여행지 후보에 대해 만족도 예측 후 상위 N개 추천
    - user_input_dict: 사용자 입력값(딕셔너리)
    - model: 학습된 CatBoost 모델
    - X_columns: 피처 컬럼 순서
    - all_visit_area_nms: 모든 여행지 인코딩 값 리스트
    - label_encoders: 컬럼별 LabelEncoder
    - area_to_address_map: 여행지명→도로명 주소 매핑
    - area_to_address_map2: 여행지명→시군구 매핑
    - top_n: 추천 개수
    """
    # 모든 여행지 후보에 대해 사용자 입력값 + 여행지 인코딩 조합으로 feature row 생성
    all_candidate_data = []
    for area_encoded in all_visit_area_nms:
        row = user_input_dict.copy()  # 사용자 입력값 복사
        row['VISIT_AREA_NM'] = area_encoded  # 여행지 인코딩 값만 변경
        all_candidate_data.append(row)
    # DataFrame으로 변환 (컬럼 순서 반드시 일치)
    input_df = pd.DataFrame(all_candidate_data, columns=X_columns)
    # 모델로 일괄 예측 (예외 처리 포함)
    preds = predict_with_exception_handling(model, input_df)
    recommendations = []
    # 예측 결과와 주소 정보, 시도명 표준화까지 포함해 추천 리스트 작성
    for i, area_encoded in enumerate(all_visit_area_nms):
        area_original_name = label_encoders['VISIT_AREA_NM'].inverse_transform([area_encoded])[0]  # 인코딩 → 원본 여행지명
        road_nm_addr = area_to_address_map.get(area_original_name, '주소 정보 없음')  # 도로명 주소
        road_nm_addr2 = area_to_address_map2.get(area_original_name, '주소 정보 없음')  # 시군구
        province_std = standardize_province(road_nm_addr)  # 시도명 표준화
        recommendations.append({
            '여행지': area_original_name,
            '예상 만족도': preds[i],
            '주소': road_nm_addr,
            '시군구': road_nm_addr2,
            '시도명': province_std
        })
    recommendations_df = pd.DataFrame(recommendations)
    # 시도명 중복 제거 (원하면, 같은 시도 내에서 한 곳만 추천)
    recommendations_df = recommendations_df.drop_duplicates(subset=['시도명'])
    # 만족도 기준 내림차순 정렬 후 상위 N개 반환
    return recommendations_df.sort_values(by='예상 만족도', ascending=False).head(top_n)

# 모델 성능 평가 함수
def calculate_model_performance(y_true, y_pred):
    """
    회귀 모델의 성능을 평가하는 함수
    - y_true: 실제값 (테스트셋)
    - y_pred: 예측값 (모델 예측 결과)
    반환값: (RMSE, MAE, R2)
    """
    # RMSE (Root Mean Squared Error): 예측 오차의 제곱 평균의 제곱근, 값이 작을수록 좋음
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    # MAE (Mean Absolute Error): 예측값과 실제값의 절대 오차 평균, 값이 작을수록 좋음
    mae = mean_absolute_error(y_true, y_pred)
    # R2 (결정계수): 1에 가까울수록 모델이 데이터를 잘 설명함
    r2 = r2_score(y_true, y_pred)
    return rmse, mae, r2

def print_performance(rmse, mae, r2):
    """
    모델 성능 지표를 보기 좋게 출력하는 함수
    """
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R2: {r2:.4f}")


def run(age, gender, theme, filepath, modelpath):

# 데이터 불러오기 (CSV 파일에서 데이터프레임 생성)

    df = pd.read_csv(filepath)

    # 데이터 전처리 및 분할 (함수 호출로 처리)
    train_pool, test_pool, label_encoders, X, y, df_ml, X_test, y_test = preprocess_data(df)

    # 주소 매핑 준비
    # 여행지명별로 도로명 주소와 시군구를 뽑아서 딕셔너리로 만듦 (추천 결과에 사용)
    # mode()가 여러 개일 때 첫 번째 값만 사용하도록 안전하게 처리
    area_to_address_map = df.groupby('VISIT_AREA_NM')['ROAD_NM_ADDR'].apply(
        lambda x: ' '.join(x.mode().iloc[0].split(' ')[:1]) if len(x.mode()) > 0 else ''
    ).to_dict()

    area_to_address_map2 = df.groupby('VISIT_AREA_NM')['ROAD_NM_ADDR'].apply(
        lambda x: ' '.join(x.mode().iloc[0].split(' ')[1:2]) if len(x.mode()) > 0 else ''
    ).to_dict()
    
    if os.path.exists(modelpath) == False:

        # 모델 정의 및 학습
        # CatBoostRegressor 모델 객체를 만들고 학습시킴
        model = CatBoostRegressor(
            loss_function='RMSE',
            eval_metric='MAE',
            task_type='GPU',
            iterations=3100,
            learning_rate=0.034,
            depth=10,
            random_seed=42,
            verbose=500,
            early_stopping_rounds=100,
            l2_leaf_reg=0.002
        )

        model.fit(train_pool, eval_set=test_pool, plot=True)

        model.save_model('catboost_model.cbm')
    else:
        model = CatBoostRegressor()
        model.load_model('./catboost_model.cbm')

    # 테스트셋 예측 및 평가
    y_pred = model.predict(X_test)
    rmse, mae, r2 = calculate_model_performance(y_test, y_pred)
    print_performance(rmse, mae, r2)

    # 사용자 입력값 준비 (예시)
    # 실제 서비스에서는 챗봇 등에서 입력받아야 함
    gender_str = gender  # 예: '남' 또는 '여'
    user_gender_encoded = safe_label_encode(label_encoders['GENDER'], gender_str)  # 안전하게 인코딩
    age_grp = age
    travel_companions_num = 0
    travel_styl_1 = 4
    travel_styl_2 = 4
    travel_styl_3 = 4
    travel_styl_4 = 4
    travel_styl_5 = 4
    travel_styl_6 = 4
    travel_styl_7 = 4
    travel_styl_8 = 4
    activity_type = 4
    travel_status_accompany_str = theme  # 숫자로 입력

    # 모델 입력 포맷에 맞게 사용자 입력값 딕셔너리로 구성
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
        'TRAVEL_STATUS_ACCOMPANY': travel_status_accompany_str,
        'ACTIVITY_TYPE_CD': activity_type
    }

    # 추천 실행
    # 모델 학습에 사용된 모든 여행지 인코딩 값 리스트 추출
    all_visit_area_nms = df_ml['VISIT_AREA_NM'].unique()
    # 추천 함수 호출
    top_5_recommendations = recommend_top_areas(
        user_fixed_data, model, X.columns, all_visit_area_nms, label_encoders,
        area_to_address_map, area_to_address_map2, top_n=5
    )

    # 추천 결과 출력 (markdown 표 형태)
    print("\n--- 사용자 맞춤형 여행지 추천 (상위 5개) ---")
    print(top_5_recommendations.to_markdown(index=False))
    return model, top_5_recommendations


def show_graph(model, top_5_recommendations, filepath):
    # 한글 폰트 설정
    # plt.rc('font', family='NanumBarunGothic')

    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False


    # 데이터 불러오기
    df = pd.read_csv(filepath)

    # 추천 함수 결과에서 여행지명 리스트 추출
    recommend_areas = top_5_recommendations['여행지'].tolist()

    # summary_df 생성
    def summarize_by_gender_age(df, recommend_areas):
        df_filtered = df[df['VISIT_AREA_NM'].isin(recommend_areas)]
        summary = df_filtered.groupby(['VISIT_AREA_NM', 'GENDER', 'AGE_GRP']).agg(
            avg_satisfaction=('DGSTFN', 'mean'),
            count_visits=('DGSTFN', 'count')
        ).reset_index()
        total_visits = df_filtered.groupby(['VISIT_AREA_NM']).size().reset_index(name='total_visits')
        summary = summary.merge(total_visits, on='VISIT_AREA_NM')
        summary['visit_ratio'] = summary['count_visits'] / summary['total_visits']
        return summary

    summary_df = summarize_by_gender_age(df, recommend_areas)

    # 한글 라벨 매핑
    gender_map = {'남': '남', '여': '여'}
    age_map = {20: '20대', 30: '30대', 40: '40대', 50: '50대', 60: '60대'}
    summary_df['성별'] = summary_df['GENDER'].map(gender_map)
    summary_df['연령대'] = summary_df['AGE_GRP'].map(age_map)

    # subplot으로 5개 여행지 한 번에 시각화
    fig, axes = plt.subplots(5, 1, figsize=(6, 40), sharey=True)
    sns.set_style('whitegrid')

    for i, area in enumerate(recommend_areas):
        ax = axes[i]
        data = summary_df[summary_df['VISIT_AREA_NM'] == area]
        sns.barplot(x='연령대', y='avg_satisfaction', hue='성별', data=data, ax=ax, palette='pastel')
        ax.set_title(area)
        ax.set_ylim(3, 6)
        ax.set_xlabel('')
        if i == 0:
            ax.set_ylabel('평균 만족도')
        else:
            ax.set_ylabel('')
        # 범례는 마지막 subplot에만 표시
        if i == len(recommend_areas) - 1:
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles=handles, labels=labels, title='성별', loc='upper right')
        else:
            ax.get_legend().remove()
        # 막대 위에 값 표시
        for p in ax.patches:
            height = p.get_height()
            if not np.isnan(height):
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2, height),
                            ha='center', va='bottom', fontsize=10, color='black', rotation=0)

    plt.suptitle('추천 여행지별 성별·연령대별 평균 만족도', fontproperties="Malgun Gothic", fontsize=18)
    #plt.tight_layout()
    plt.subplots_adjust(top=0.92, hspace=0.1)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    #model.get_feature_importance(prettified=True)
    return buf  # 이미지 버퍼 반환

if __name__ == "__main__":
    filepath = 'final_file_cleaned.csv'
    modelpath = 'catboost_model.cbm'
    model, top_5 = run(20, '남', 1, filepath, modelpath)
    show_graph(model, top_5, filepath)