import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from joblib import dump, load

# 뭔가 뜨긴 하지만.. 성능은 장담을 못합니다..!!



# 1. 데이터 불러오기
df = pd.read_csv('./resources/final_file.csv')
print(df.shape)
print(df.isnull().sum())

# 2. 필요한 컬럼만
df = df[["GENDER", "AGE_GRP", "ACTIVITY_TYPE_CD", "VISIT_AREA_NM"]].dropna()

# 3. 성별 숫자화
df["GENDER"] = df["GENDER"].map({"남": 1, "여": 0})

# 4. 클래스가 너무 적은 장소 제거
counts = df["VISIT_AREA_NM"].value_counts()
df = df[df["VISIT_AREA_NM"].isin(counts[counts >= 2].index)]

# 5. 라벨 인코딩
le = LabelEncoder()
df["VISIT_AREA_NM_ENC"] = le.fit_transform(df["VISIT_AREA_NM"])

# 6. 학습용 데이터
X = df[["GENDER", "AGE_GRP", "ACTIVITY_TYPE_CD"]]
y = df["VISIT_AREA_NM_ENC"]

# 7. train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# 8. 모델 학습
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 모델 저장
dump(model, "travel_rf_model.joblib")
# LabelEncoder 저장
dump(le, "travel_label_encoder.joblib")

# # 9. 평가
# y_pred = model.predict(X_test)
# labels = np.unique(y_test)
# target_names = le.inverse_transform(labels)

# print(classification_report(
#     y_test, y_pred, labels=labels, target_names=target_names, zero_division=0
# ))

# # 10. 사용자 추천
# test_input = pd.DataFrame([{
#     "GENDER": 1,
#     "AGE_GRP": 20,
#     "ACTIVITY_TYPE_CD": 3
# }])

# probas = model.predict_proba(test_input)[0]
# top10_indices = probas.argsort()[::-1][:10]
# top10_places = le.inverse_transform(top10_indices)

# print("추천 여행지 10개")
# for rank, place in enumerate(top10_places, 1):
#     print(f"{rank}. {place}")