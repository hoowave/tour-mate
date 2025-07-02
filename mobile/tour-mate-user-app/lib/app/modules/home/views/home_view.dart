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
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () {
            InfoModal.show(controller);
          },
        ),
        title: const Text('Tour Mate'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: Obx(() {
              if (controller.chatList.isEmpty) {
                return const Center(
                  child: Text(
                    '여행지를 추천받아보세요!',
                    style: TextStyle(
                      color: Colors.grey,
                      fontSize: 18,
                    ),
                  ),
                );
              }
              return ListView.builder(
                padding:
                    const EdgeInsets.symmetric(vertical: 16, horizontal: 8),
                itemCount: controller.chatList.length,
                itemBuilder: (context, index) {
                  final chat = controller.chatList[index];
                  final isUser = chat.senderId == "user";
                  return Align(
                    alignment:
                        isUser ? Alignment.centerRight : Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: isUser ? Colors.blue[100] : Colors.grey[200],
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        chat.message,
                        style: TextStyle(
                          color: isUser ? Colors.blue[900] : Colors.black87,
                          fontSize: 16,
                        ),
                      ),
                    ),
                  );
                },
              );
            }),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
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
    );
  }
}
