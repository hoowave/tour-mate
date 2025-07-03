import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# 뭔가 뜨긴 하지만.. 성능은 장담을 못합니다..!!



df = pd.read_csv('./final_file.csv')

print(df.shape)
print(df.isnull().sum())

df = df[["GENDER", "AGE_GRP", "ACTIVITY_TYPE_CD", "VISIT_AREA_NM"]].dropna()

df["GENDER"] = df["GENDER"].map({"남": 1, "여": 0})

# 클래스 수가 너무 적은 VISIT_AREA_NM 제거 (2개 이상만 남기기)
counts = df["VISIT_AREA_NM"].value_counts()
df = df[df["VISIT_AREA_NM"].isin(counts[counts >= 2].index)]


X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 평가
y_pred = model.predict(X_test)
print("📊 Classification Report")
print(classification_report(y_test, y_pred))


test_input = pd.DataFrame([{
    "GENDER": 1,
    "AGE_GRP": 20,
    "ACTIVITY_TYPE_CD": 3
}])

probas = model.predict_proba(test_input)[0]
top10_indices = probas.argsort()[::-1][:10]
top10_places = le.inverse_transform(top10_indices)

print("추천 여행지 10개")
for rank, place in enumerate(top10_places, 1):
    print(f"{rank}. {place}")

