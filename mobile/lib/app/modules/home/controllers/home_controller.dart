import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'dart:convert';
import 'package:tour_mate_user_app/app/data/model/chat_model.dart';
import 'package:tour_mate_user_app/app/modules/home/views/widgets/info_modal.dart';
import 'package:tour_mate_user_app/app/routes/app_pages.dart';

import '../../../data/service/networking/api_service.dart';

class HomeController extends GetxController {
  final ApiService apiService;

  HomeController(this.apiService);

  @override
  void onInit() {
    super.onInit();
  }

  @override
  void onReady() {
    super.onReady();
    InfoModal.show(this);
  }

  @override
  void onClose() {
    userInput.dispose();
    super.onClose();
  }

  final RxList<ChatModel> chatList = <ChatModel>[].obs;
  final userInput = TextEditingController();
  final ageGroup = '10대'.obs;
  final gender = '남성'.obs;
  final theme = '취식'.obs;
  final days = '1'.obs;
  final messageText = ''.obs;
  final isLoading = false.obs; // 로딩 상태 추가

  // 나이 그룹을 API 요청용 값으로 변환
  String _convertAgeGroup(String displayValue) {
    switch (displayValue) {
      case '10대':
        return '10';
      case '20대':
        return '20';
      case '30대':
        return '30';
      case '40대':
        return '40';
      case '50대':
        return '50';
      case '60대':
        return '60';
      default:
        return '20';
    }
  }

  // 성별을 API 요청용 값으로 변환
  String _convertGender(String displayValue) {
    switch (displayValue) {
      case '남성':
        return '남';
      case '여성':
        return '여';
      default:
        return '남';
    }
  }

  // 테마를 API 요청용 값으로 변환
  String _convertTheme(String displayValue) {
    switch (displayValue) {
      case '취식':
        return '1';
      case '쇼핑':
        return '2';
      case '체험':
        return '3';
      case '단순구경':
        return '4';
      case '휴식':
        return '5';
      case '기타활동':
        return '6';
      default:
        return '1';
    }
  }

  Future<void> sendMessage() async {
    if (userInput.text.trim().isEmpty) {
      chatList.add(ChatModel(
        senderId: "ai",
        message: "메시지를 입력해주세요.",
        timestamp: DateTime.now(),
      ));
      return;
    }

    // 이미 로딩 중이면 중복 요청 방지
    if (isLoading.value) return;

    print('사용자 입력: ${userInput.text}');

    // 사용자 메시지 추가
    chatList.add(ChatModel(
      senderId: "user",
      message: userInput.text,
      timestamp: DateTime.now(),
    ));

    // 로딩 상태 시작
    isLoading.value = true;

    // 입력 텍스트 저장 후 클리어
    final userMessage = userInput.text;
    userInput.clear();

    // AI 로딩 메시지 추가
    chatList.add(ChatModel(
      senderId: "ai",
      message: "여행지 찾아보는 중... 🗺️",
      timestamp: DateTime.now(),
    ));

    // duration 계산 (days가 "1"이면 "1박2일", "2"면 "2박3일" 등)
    final duration = "${days.value}박${int.parse(days.value) + 1}일";

    try {
      // API 요청 시 변환된 값 사용
      final convertedAge = _convertAgeGroup(ageGroup.value);
      final convertedGender = _convertGender(gender.value);
      final convertedTheme = _convertTheme(theme.value);

      print(
          'UI 표시 값 - 나이: ${ageGroup.value}, 성별: ${gender.value}, 테마: ${theme.value}');
      print(
          'API 전송 값 - 나이: $convertedAge, 성별: $convertedGender, 테마: $convertedTheme');

      final response = await apiService.sendChatMessage(
        age: convertedAge,
        gender: convertedGender,
        theme: convertedTheme,
        message: userMessage,
        duration: duration,
      );

      print('API 응답 상태코드: ${response.statusCode}');
      print('API 응답: ${response.body}');

      if (response.statusCode == 200) {
        // 성공적인 응답 처리
        final responseData = jsonDecode(response.body);
        final chatResponse = ChatResponse.fromJson(responseData);
        final aiMessage = chatResponse.reply.isNotEmpty
            ? chatResponse.reply
            : '응답을 받지 못했습니다.';

        // 로딩 메시지를 실제 응답으로 교체
        if (chatList.isNotEmpty &&
            chatList.last.senderId == "ai" &&
            chatList.last.message == "여행지 찾아보는 중... 🗺️") {
          chatList.removeLast();
        }

        // ChatModel.fromAI 팩토리를 사용하여 이미지 URL 자동 처리
        chatList.add(ChatModel.fromAI(aiMessage));
      } else {
        // 에러 응답 처리
        // 로딩 메시지를 에러 메시지로 교체
        if (chatList.isNotEmpty &&
            chatList.last.senderId == "ai" &&
            chatList.last.message == "여행지 찾아보는 중... 🗺️") {
          chatList.removeLast();
        }
        chatList
            .add(ChatModel.fromAI("서버 오류가 발생했습니다. (${response.statusCode})"));
      }
    } catch (e) {
      // 네트워크 에러 처리
      print('네트워크 오류: $e');
      // 로딩 메시지를 에러 메시지로 교체
      if (chatList.isNotEmpty &&
          chatList.last.senderId == "ai" &&
          chatList.last.message == "여행지 찾아보는 중... 🗺️") {
        chatList.removeLast();
      }
      chatList.add(ChatModel(
        senderId: "ai",
        message: "네트워크 오류가 발생했습니다: $e",
        timestamp: DateTime.now(),
      ));
    } finally {
      // 로딩 상태 해제
      isLoading.value = false;
    }
  }
}
