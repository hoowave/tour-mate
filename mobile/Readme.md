# 투어 메이트 모바일 앱

## 프로젝트 개요

투어 메이트 모바일 앱은 Flutter와 GetX를 기반으로 한 크로스 플랫폼 애플리케이션으로, 사용자가 언제 어디서나 AI 여행 추천 챗봇과 상호작용할 수 있는 모바일 최적화된 인터페이스를 제공합니다.

## 주요 기능

- 📱 **크로스 플랫폼**: iOS와 Android 모두 지원
- 💬 **실시간 챗봇**: 자연스러운 대화형 여행 추천
- 🎨 **네이티브 UI**: 각 플랫폼의 디자인 가이드라인 준수
- 📊 **데이터 시각화**: 여행 추천 결과를 그래프로 표시
- 🔄 **상태 관리**: GetX를 활용한 효율적인 상태 관리
- ⚡ **빠른 성능**: 최적화된 렌더링과 메모리 관리
- 🌐 **오프라인 지원**: 기본 기능의 오프라인 동작

## 기술 스택

- **Framework**: Flutter 3.x
- **Language**: Dart
- **State Management**: GetX
- **Architecture**: GetX Pattern (MVVM)
- **HTTP Client**: Dio / HTTP
- **Local Storage**: SharedPreferences / Hive
- **Build System**: Gradle (Android) / Xcode (iOS)

## 아키텍처 (GetX Pattern)

### MVVM 아키텍처 구조

```
┌─────────────────────────────────────┐
│              View Layer             │  ← UI 컴포넌트
├─────────────────────────────────────┤
│           Controller Layer          │  ← 비즈니스 로직
├─────────────────────────────────────┤
│             Model Layer             │  ← 데이터 모델
├─────────────────────────────────────┤
│           Service Layer             │  ← API 통신
└─────────────────────────────────────┘
```

### GetX 핵심 구성요소

- **Controller**: 상태 관리 및 비즈니스 로직
- **Binding**: 의존성 주입 및 라우트 관리
- **View**: UI 컴포넌트
- **Model**: 데이터 구조 정의
- **Service**: 외부 API 통신

## 프로젝트 구조

```
mobile/tour-mate-user-app/
├── lib/
│   ├── app/                          # 앱 전체 구조
│   │   ├── data/                     # 데이터 계층
│   │   │   ├── model/               # 데이터 모델
│   │   │   │   └── chat_model.dart  # 채팅 모델
│   │   │   └── service/             # 서비스 계층
│   │   │       └── networking/      # 네트워킹
│   │   │           └── api_service.dart # API 서비스
│   │   ├── modules/                  # 기능별 모듈
│   │   │   ├── home/                # 홈 모듈
│   │   │   │   ├── bindings/        # 의존성 주입
│   │   │   │   │   └── home_binding.dart
│   │   │   │   ├── controllers/     # 컨트롤러
│   │   │   │   │   └── home_controller.dart
│   │   │   │   ├── views/           # 뷰
│   │   │   │   │   ├── home_view.dart
│   │   │   │   │   └── widgets/     # 위젯
│   │   │   │   │       ├── info_modal.dart
│   │   │   │   │       └── input_box.dart
│   │   │   ├── graph/               # 그래프 모듈
│   │   │   │   ├── bindings/
│   │   │   │   │   └── graph_binding.dart
│   │   │   │   ├── controllers/
│   │   │   │   │   └── graph_controller.dart
│   │   │   │   └── views/
│   │   │   │       └── graph_view.dart
│   │   │   └── splash/              # 스플래시 모듈
│   │   │       ├── bindings/
│   │   │       │   └── splash_binding.dart
│   │   │       ├── controllers/
│   │   │       │   └── splash_controller.dart
│   │   │       └── views/
│   │   │           └── splash_view.dart
│   │   └── routes/                   # 라우팅
│   │       ├── app_pages.dart       # 페이지 정의
│   │       └── app_routes.dart      # 라우트 상수
│   ├── app_binding.dart              # 앱 바인딩
│   ├── env.dart                      # 환경 설정
│   └── main.dart                     # 앱 진입점
├── android/                          # Android 플랫폼
├── ios/                              # iOS 플랫폼
├── pubspec.yaml                      # 의존성 관리
└── analysis_options.yaml             # 코드 분석 설정
```

## 모듈별 설명

### 🏠 Home Module
- **기능**: 메인 챗봇 인터페이스
- **컴포넌트**: 
  - `home_view.dart`: 메인 화면
  - `input_box.dart`: 사용자 입력 위젯
  - `info_modal.dart`: 정보 모달

### 📊 Graph Module
- **기능**: 여행 추천 결과 시각화
- **컴포넌트**:
  - `graph_view.dart`: 그래프 화면
  - `graph_controller.dart`: 그래프 데이터 관리

### ⚡ Splash Module
- **기능**: 앱 시작 화면
- **컴포넌트**:
  - `splash_view.dart`: 스플래시 화면
  - `splash_controller.dart`: 초기화 로직

## 설치 및 실행 가이드

### 1. Flutter 환경 설정

```bash
# Flutter SDK 설치 확인
flutter doctor

# 필요한 의존성 설치
flutter pub get
```

### 2. 저장소 클론

```bash
git clone <repository-url>
cd last/mobile/tour-mate-user-app
```

### 3. 의존성 설치

```bash
flutter pub get
```

### 4. 환경 변수 설정

`lib/env.dart` 파일에서 API URL을 설정하세요:

```dart
class Env {
  static const String apiUrl = 'http://localhost:8000';
  static const String environment = 'development';
}
```

### 5. 앱 실행

```bash
# Android 에뮬레이터에서 실행
flutter run

# iOS 시뮬레이터에서 실행
flutter run -d ios

# 특정 디바이스에서 실행
flutter devices
flutter run -d <device-id>
```

### 6. 빌드

```bash
# Android APK 빌드
flutter build apk

# Android App Bundle 빌드
flutter build appbundle

# iOS 빌드
flutter build ios
```

## 주요 의존성

### 핵심 의존성
```yaml
dependencies:
  flutter:
    sdk: flutter
  get: ^4.6.5                    # 상태 관리 및 라우팅
  dio: ^5.3.2                    # HTTP 클라이언트
  shared_preferences: ^2.2.2     # 로컬 저장소
  flutter_chart: ^0.0.1          # 차트 라이브러리
```

### 개발 의존성
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0          # 코드 린팅
```

## 플랫폼별 설정

### Android 설정
- `android/app/build.gradle`: 앱 버전 및 권한 설정
- `android/app/src/main/AndroidManifest.xml`: 앱 권한 및 설정

### iOS 설정
- `ios/Runner/Info.plist`: 앱 정보 및 권한 설정
- `ios/Runner.xcodeproj`: Xcode 프로젝트 설정

## 성능 최적화

- **위젯 최적화**: `const` 생성자 사용
- **메모리 관리**: `dispose()` 메서드 활용
- **이미지 최적화**: 적절한 이미지 포맷 및 크기 사용
- **네트워크 최적화**: 캐싱 및 압축 활용

## 테스트

```bash
# 단위 테스트 실행
flutter test

# 위젯 테스트 실행
flutter test test/widget_test.dart

# 통합 테스트 실행
flutter drive --target=test_driver/app.dart
```

## 배포

### Android 배포
1. `flutter build appbundle` 실행
2. Google Play Console에 업로드

### iOS 배포
1. `flutter build ios` 실행
2. Xcode에서 Archive 및 App Store Connect 업로드

## 개발 가이드라인

### 코드 스타일
- Dart 언어 가이드라인 준수
- 의미있는 변수명과 함수명 사용
- 주석 작성으로 코드 가독성 향상

### GetX 패턴
- Controller는 단일 책임 원칙 준수
- Binding을 통한 의존성 주입 활용
- Reactive 상태 관리 적극 활용

### 위젯 구조
- 재사용 가능한 위젯 설계
- 적절한 폴더 구조 유지
- 성능 최적화 고려

---