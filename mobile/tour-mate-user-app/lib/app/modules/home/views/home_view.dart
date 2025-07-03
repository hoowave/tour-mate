import 'package:flutter/material.dart';

import 'package:get/get.dart';

import '../controllers/home_controller.dart';
import 'widgets/input_box.dart';
import 'widgets/info_modal.dart';

class HomeView extends GetView<HomeController> {
  const HomeView({super.key});

  @override
  Widget build(BuildContext context) {
    Future.delayed(Duration.zero, () {
      if (controller.ageGroup.value.isEmpty) {
        InfoModal.show(controller);
      }
    });

    return Scaffold(
      extendBodyBehindAppBar: true,
      backgroundColor: Colors.transparent,
      appBar: AppBar(
        backgroundColor: Colors.white.withOpacity(0.85),
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.menu, color: Color(0xFF374151)),
          onPressed: () {
            InfoModal.show(controller);
          },
          splashRadius: 24,
        ),
        title: const Text(
          'Tour Mate',
          style: TextStyle(
            color: Color(0xFF374151),
            fontWeight: FontWeight.bold,
            fontSize: 22,
            letterSpacing: 1.2,
            shadows: [
              Shadow(
                color: Colors.white,
                blurRadius: 4,
                offset: Offset(0, 1),
              ),
            ],
          ),
        ),
        centerTitle: true,
      ),
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF667eea), Color(0xFF764ba2)],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              Expanded(
                child: Obx(() {
                  if (controller.chatList.isEmpty) {
                    return Center(
                      child: const Text(
                        '여행지를 추천받아보세요!',
                        style: TextStyle(
                          color: Colors.grey,
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    );
                  }
                  return ListView.builder(
                    padding: const EdgeInsets.symmetric(
                        vertical: 24, horizontal: 12),
                    itemCount: controller.chatList.length,
                    itemBuilder: (context, index) {
                      final chat = controller.chatList[index];
                      final isUser = chat.senderId == "user";
                      return Align(
                        alignment: isUser
                            ? Alignment.centerRight
                            : Alignment.centerLeft,
                        child: Container(
                          margin: const EdgeInsets.symmetric(vertical: 6),
                          padding: const EdgeInsets.symmetric(
                              horizontal: 16, vertical: 12),
                          constraints: const BoxConstraints(maxWidth: 320),
                          decoration: BoxDecoration(
                            color: isUser
                                ? const Color(0xFF667eea)
                                : Colors.white.withOpacity(0.95),
                            borderRadius: BorderRadius.only(
                              topLeft: const Radius.circular(18),
                              topRight: const Radius.circular(18),
                              bottomLeft: Radius.circular(isUser ? 18 : 4),
                              bottomRight: Radius.circular(isUser ? 4 : 18),
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.06),
                                blurRadius: 8,
                                offset: const Offset(0, 2),
                              ),
                            ],
                          ),
                          child: Text(
                            chat.message,
                            style: TextStyle(
                              color: isUser
                                  ? Colors.white
                                  : const Color(0xFF667eea),
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                      );
                    },
                  );
                }),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(12, 0, 12, 16),
                child: InputBox(
                  controller: controller.userInput,
                  onChanged: (value) {
                    controller.messageText.value = value;
                  },
                  onSend: controller.sendMessage,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
