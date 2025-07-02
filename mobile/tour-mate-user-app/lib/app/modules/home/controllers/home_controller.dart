import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:tour_mate_user_app/app/data/model/chat_model.dart';
import 'package:tour_mate_user_app/app/modules/home/views/widgets/info_modal.dart';

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
  final theme = '자연'.obs;
  final days = '1'.obs; // 1박
  final messageText = ''.obs;

  Future<void> sendMessage() async {
    if (userInput.text.trim().isEmpty) {
      chatList.add(ChatModel(
        senderId: "ai",
        message: "Ai test data",
        timestamp: DateTime.now(),
      ));
      return;
    }

    print('사용자 입력: ${userInput.text}');
    chatList.add(ChatModel(
      senderId: "user",
      message: userInput.text,
      timestamp: DateTime.now(),
    ));

    // final response = await apiService().postRequest(
    //   'https://your-api-url.com/ai',
    //   {'message': userInput.text},
    // );
    //
    // print('응답: ${response.body}');
    userInput.clear();
  }
}
