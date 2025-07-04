# 투어 메이트 백엔드 서버

## 프로젝트 개요

투어 메이트 백엔드는 FastAPI 기반의 AI 여행 추천 시스템으로, 사용자 입력을 받아 머신러닝 모델과 외부 API를 활용하여 맞춤형 여행지를 추천하는 서버입니다.

## 아키텍처

### 계층형 아키텍처 (Layered Architecture)

```
┌─────────────────────────────────────┐
│           Controller Layer          │  ← API 엔드포인트 처리
├─────────────────────────────────────┤
│            Service Layer            │  ← 비즈니스 로직 처리
├─────────────────────────────────────┤
│           Facade Layer              │  ← 외부 서비스 통합
├─────────────────────────────────────┤
│            Model Layer              │  ← 데이터 모델 및 ML 모델
└─────────────────────────────────────┘
```

## 폴더 구조 및 역할

```
backend/
├── main.py                    # FastAPI 애플리케이션 진입점
├── interfaces/                # 인터페이스 계층
│   ├── controller.py         # API 컨트롤러
│   └── dto/                  # 데이터 전송 객체
│       ├── request_dto.py    # 요청 DTO
│       └── response_dto.py   # 응답 DTO
├── service/                   # 서비스 계층
│   └── service.py            # 비즈니스 로직 처리
├── facade/                    # 퍼사드 계층
│   ├── catboost_agent/       # CatBoost ML 모델 관련
│   │   ├── model_catboost.py # ML 모델 로직
│   │   └── recommend_travel_places.py # 여행지 추천 로직
│   ├── open_ai_agent.py      # OpenAI GPT 통합
│   ├── kto_api_agent.py      # 한국관광공사 API 통합
│   └── dto/                  # 외부 API DTO
└── model_catboost.py         # ML 모델 정의
```

### 폴더별 상세 역할

#### `interfaces/` - 인터페이스 계층
- **controller.py**: HTTP 요청/응답 처리, API 엔드포인트 정의
- **dto/**: 클라이언트와 서버 간 데이터 전송 객체 정의

#### `service/` - 서비스 계층  
- **service.py**: 핵심 비즈니스 로직 처리, 전체 추천 플로우 조율

#### `facade/` - 퍼사드 계층
- **catboost_agent/**: 머신러닝 추천 모델 관련 기능
- **open_ai_agent.py**: OpenAI GPT API 통합
- **kto_api_agent.py**: 한국관광공사 관광정보 API 통합
- **dto/**: 외부 API 응답 데이터 구조 정의

## 데이터 흐름

```
1. 사용자 입력
   ↓
2. 머신러닝 추천모델 (CatBoost)
   ↓
3. 추천 여행지 5개 선정
   ↓
4. 추천 여행지 기준 웹 서치
   ↓
5. 한국관광공사 관광정보 API 조회
   ↓
6. GPT 자연어 응답 생성
   ↓
7. 사용자에게 최종 답변 전달
```

### 상세 플로우 설명

1. **사용자 입력**: 사용자의 선호도, 예산, 기간 등 정보 수집
2. **ML 추천모델**: CatBoost 모델을 사용하여 사용자 특성에 맞는 여행지 추천
3. **여행지 선정**: 추천 점수 상위 5개 여행지 선별
4. **웹 서치**: 선정된 여행지에 대한 최신 정보 수집
5. **관광정보 API**: 한국관광공사 API를 통한 상세 관광정보 조회
6. **GPT 응답**: 수집된 정보를 바탕으로 자연스러운 추천 답변 생성
7. **최종 답변**: 사용자에게 맞춤형 여행 추천 정보 제공

## 설치 및 실행 가이드

### 1. 저장소 클론

```bash
git clone <repository-url>
cd last/backend
```

### 2. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
RESOURCE_PATH=./resources
MODEL_PATH=catboost_model.cbm
OPENAI_API_KEY=your_openai_api_key
KTO_API_KEY=your_kto_api_key
```

### 5. 서버 실행

```bash
# 개발 모드로 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드로 실행
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 6. API 문서 확인

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 주요 API 엔드포인트

- `POST /recommend`: 여행지 추천 요청
- `GET /health`: 서버 상태 확인

## 기술 스택

- **Framework**: FastAPI
- **ML Model**: CatBoost
- **AI Service**: OpenAI GPT
- **External API**: 한국관광공사 API
- **Language**: Python 3.8+

## 개발 환경

- Python 3.8 이상
- FastAPI
- uvicorn
- catboost
- openai
- requests
- python-dotenv

---