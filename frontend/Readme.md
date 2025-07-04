# 투어 메이트 프론트엔드

## 프로젝트 개요

투어 메이트 프론트엔드는 React 기반의 웹 애플리케이션으로, 사용자가 여행 추천 챗봇과 상호작용할 수 있는 직관적이고 반응형인 사용자 인터페이스를 제공합니다.

## 주요 기능

- 💬 **실시간 챗봇 인터페이스**: 자연스러운 대화형 여행 추천
- 🎨 **모던 UI/UX**: 깔끔하고 직관적인 사용자 인터페이스
- 📱 **반응형 디자인**: 데스크톱, 태블릿, 모바일 모든 기기 지원
- 🔍 **검색 기능**: 여행지 검색 및 필터링
- 📊 **데이터 시각화**: 여행 추천 결과를 그래프로 시각화
- ⚡ **빠른 응답**: 최적화된 성능과 빠른 로딩 속도

## 기술 스택

- **Framework**: React 18
- **Language**: JavaScript (ES6+)
- **Styling**: CSS3, CSS Modules
- **Build Tool**: Create React App
- **HTTP Client**: Fetch API / Axios
- **State Management**: React Hooks
- **Routing**: React Router (필요시)

## 프로젝트 구조

```
frontend/
├── public/                 # 정적 파일
│   ├── index.html         # 메인 HTML 파일
│   └── logo.png           # 로고 이미지
├── src/                   # 소스 코드
│   ├── components/        # 재사용 가능한 컴포넌트
│   │   ├── SearchBox.jsx  # 검색 컴포넌트
│   │   └── Sidebar.jsx    # 사이드바 컴포넌트
│   ├── pages/             # 페이지 컴포넌트
│   │   ├── graph.jsx      # 그래프 페이지
│   │   └── NotFound.jsx   # 404 페이지
│   ├── css/               # 스타일 파일
│   │   ├── graph.css      # 그래프 스타일
│   │   ├── NotFound.css   # 404 페이지 스타일
│   │   ├── SearchBox.css  # 검색 컴포넌트 스타일
│   │   └── Sidebar.css    # 사이드바 스타일
│   ├── App.js             # 메인 앱 컴포넌트
│   ├── App.css            # 앱 전체 스타일
│   └── index.js           # 앱 진입점
├── package.json           # 프로젝트 의존성 및 스크립트
└── package-lock.json      # 의존성 잠금 파일
```

## 컴포넌트 설명

### 주요 컴포넌트

#### `SearchBox.jsx`
- 사용자 입력을 받는 검색 인터페이스
- 여행 선호도, 예산, 기간 등 정보 입력
- 실시간 입력 검증 및 제안 기능

#### `Sidebar.jsx`
- 네비게이션 및 메뉴 제공
- 사용자 프로필 및 설정 접근
- 최근 검색 기록 표시

### 페이지 컴포넌트

#### `graph.jsx`
- 여행 추천 결과를 시각적으로 표현
- 차트 및 그래프를 통한 데이터 시각화
- 추천 여행지 비교 및 분석

#### `NotFound.jsx`
- 404 에러 페이지
- 사용자 친화적인 에러 메시지
- 홈으로 돌아가는 네비게이션

## 설치 및 실행 가이드

### 1. 저장소 클론

```bash
git clone <repository-url>
cd last/frontend
```

### 2. 의존성 설치

```bash
npm install
# 또는
yarn install
```

### 3. 개발 서버 실행

```bash
npm start
# 또는
yarn start
```

개발 서버가 `http://localhost:3000`에서 실행됩니다.

### 4. 프로덕션 빌드

```bash
npm run build
# 또는
yarn build
```

빌드된 파일은 `build/` 폴더에 생성됩니다.

### 5. 테스트 실행

```bash
npm test
# 또는
yarn test
```

## 개발 스크립트

```json
{
  "start": "react-scripts start",     // 개발 서버 실행
  "build": "react-scripts build",     // 프로덕션 빌드
  "test": "react-scripts test",       // 테스트 실행
  "eject": "react-scripts eject"      // CRA 설정 추출 (주의!)
}
```

## 주요 의존성

### 핵심 의존성
- `react`: React 라이브러리
- `react-dom`: React DOM 렌더링
- `react-scripts`: Create React App 스크립트

### 개발 의존성
- `@testing-library/react`: React 컴포넌트 테스트
- `@testing-library/jest-dom`: Jest DOM 매처
- `web-vitals`: 웹 성능 측정

## 브라우저 지원

- Chrome (최신 버전)
- Firefox (최신 버전)
- Safari (최신 버전)
- Edge (최신 버전)

## 개발 가이드라인

### 코드 스타일
- ES6+ 문법 사용
- 함수형 컴포넌트 및 Hooks 활용
- 의미있는 변수명과 함수명 사용
- 주석 작성으로 코드 가독성 향상

### 컴포넌트 구조
- 단일 책임 원칙 준수
- 재사용 가능한 컴포넌트 설계
- Props 타입 검증
- 적절한 폴더 구조 유지

---