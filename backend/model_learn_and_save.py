import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from catboost import CatBoostRegressor, Pool
import matplotlib.pyplot as plt
import joblib
import json

df = pd.read_csv('backend/final_file_cleaned.csv')

# 결측치 처리
df.dropna(subset=['ROAD_NM_ADDR'], inplace=True)


# df = df[~df['VISIT_AREA_NM'].astype(str).str.startswith('(')].copy()
# df = df[~df['VISIT_AREA_NM'].astype(str).str.match(r'^\d')].copy()

selected_features = [
    'GENDER',
    'AGE_GRP',
    'TRAVEL_STYL_1', 'TRAVEL_STYL_2', 'TRAVEL_STYL_3', 'TRAVEL_STYL_4',
    'TRAVEL_STYL_5', 'TRAVEL_STYL_6', 'TRAVEL_STYL_7', 'TRAVEL_STYL_8',
    'TRAVEL_COMPANIONS_NUM',
    'TRAVEL_STATUS_ACCOMPANY',
    'VISIT_AREA_NM',
    'ACTIVITY_TYPE_CD',
    'DGSTFN'
]

df_ml = df[selected_features].copy()
df_ml.dropna(subset=['DGSTFN', 'ACTIVITY_TYPE_CD'], inplace=True)

# ACTIVITY_TYPE_CD 타입 일관성 유지 (학습/예측 모두 동일하게)
df_ml['ACTIVITY_TYPE_CD'] = df_ml['ACTIVITY_TYPE_CD'].astype(int)

# VISIT_AREA_NM 매핑 정보는 인코딩 전에 저장
area_to_sido_map_raw = df.groupby('VISIT_AREA_NM')['ROAD_NM_ADDR'].apply(
    lambda x: x.mode()[0].split(' ')[0] if not x.mode().empty and len(x.mode()[0].split(' ')) > 0 else '정보 없음'
).to_dict()
area_to_sigungu_map_raw = df.groupby('VISIT_AREA_NM')['ROAD_NM_ADDR'].apply(
    lambda x: x.mode()[0].split(' ')[1] if not x.mode().empty and len(x.mode()[0].split(' ')) > 1 else '정보 없음'
).to_dict()

# LabelEncoder 적용
label_encoders = {}
categorical_cols_to_encode = ['GENDER', 'TRAVEL_STATUS_ACCOMPANY', 'VISIT_AREA_NM', 'ACTIVITY_TYPE_CD']
for col in categorical_cols_to_encode:
    le = LabelEncoder()
    df_ml[col] = le.fit_transform(df_ml[col])
    label_encoders[col] = le

# VISIT_AREA_NM 클래스 수가 2개 미만인 항목 제거
counts = df_ml["VISIT_AREA_NM"].value_counts()
df_ml = df_ml[df_ml["VISIT_AREA_NM"].isin(counts[counts >= 2].index)]

X = df_ml.drop('DGSTFN', axis=1)
y = df_ml['DGSTFN']

print(X.shape)
print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_features_indices = [
    X.columns.get_loc(col) for col in categorical_cols_to_encode if col in X.columns
]

train_pool = Pool(
    X_train,
    y_train,
    cat_features=categorical_features_indices
)
test_pool = Pool(
    X_test,
    y_test,
    cat_features=categorical_features_indices
)

model = CatBoostRegressor(
    loss_function='RMSE',
    eval_metric='MAE',
    task_type='CPU',
    iterations=3100,
    learning_rate=0.034,
    depth=10,
    random_seed=42,
    verbose=500,
    early_stopping_rounds=100,
    l2_leaf_reg=0.002
)

model.fit(
    train_pool,
    eval_set=test_pool,
    plot=True
)

# 모델 및 부가 정보 저장
joblib.dump(model, 'catboost_travel_satisfaction_model.joblib')
joblib.dump(label_encoders, 'label_encoders_for_catboost.joblib')
joblib.dump(area_to_sido_map_raw, 'area_to_sido_map.joblib')
joblib.dump(area_to_sigungu_map_raw, 'area_to_sigungu_map.joblib')

sido_change_names = {
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
with open('sido_change_names.json', 'w', encoding='utf-8') as f:
    json.dump(sido_change_names, f, ensure_ascii=False, indent=4)

joblib.dump(X.columns.tolist(), 'model_feature_columns.joblib')
print("모델, 인코더, 매핑 정보, 컬럼 순서가 저장되었습니다.")
