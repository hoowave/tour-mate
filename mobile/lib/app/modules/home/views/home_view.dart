import 'package:flutter/material.dart';
import 'package:flutter/gestures.dart';
import 'package:get/get.dart';

import '../controllers/home_controller.dart';
import '../../../data/model/chat_model.dart';
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
        actions: [
          IconButton(
            icon: const Icon(Icons.auto_graph, color: Color(0xFF374151)),
            tooltip: '그래프 보기',
            onPressed: () {
              Get.toNamed('/graph');
            },
          ),
        ],
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
                          child: _buildMessageContent(chat, isUser),
                        ),
                      );
                    },
                  );
                }),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(12, 0, 12, 16),
                child: Obx(() => InputBox(
                      controller: controller.userInput,
                      onChanged: (value) {
                        controller.messageText.value = value;
                      },
                      onSend: controller.sendMessage,
                      isLoading: controller.isLoading.value,
                    )),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMessageContent(ChatModel chat, bool isUser) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (chat.message.isNotEmpty) _buildRichText(chat.message, isUser),
        if (chat.hasLinks) ...[
          if (chat.message.isNotEmpty) const SizedBox(height: 8),
          ...chat.links!.map((link) => _buildLinkButton(link, isUser)),
        ],
      ],
    );
  }

  Widget _buildRichText(String text, bool isUser) {
    final urlPattern = RegExp(r'https?://[^\s<>"]+');
    final matches = urlPattern.allMatches(text);

    if (matches.isEmpty) {
      return Text(
        text,
        style: TextStyle(
          color: isUser ? Colors.white : const Color(0xFF667eea),
          fontSize: 16,
          fontWeight: FontWeight.w500,
        ),
      );
    }

    final spans = <TextSpan>[];
    int lastIndex = 0;

    for (final match in matches) {
      // URL 이전 텍스트
      if (match.start > lastIndex) {
        spans.add(TextSpan(
          text: text.substring(lastIndex, match.start),
          style: TextStyle(
            color: isUser ? Colors.white : const Color(0xFF667eea),
            fontSize: 16,
            fontWeight: FontWeight.w500,
          ),
        ));
      }

      // URL 링크
      final url = match.group(0)!;
      spans.add(TextSpan(
        text: url,
        style: TextStyle(
          color: isUser ? Colors.white : Colors.blue,
          fontSize: 16,
          fontWeight: FontWeight.w500,
          decoration: TextDecoration.underline,
        ),
        recognizer: TapGestureRecognizer()..onTap = () => _launchUrl(url),
      ));

      lastIndex = match.end;
    }

    // 마지막 텍스트
    if (lastIndex < text.length) {
      spans.add(TextSpan(
        text: text.substring(lastIndex),
        style: TextStyle(
          color: isUser ? Colors.white : const Color(0xFF667eea),
          fontSize: 16,
          fontWeight: FontWeight.w500,
        ),
      ));
    }

    return RichText(
      text: TextSpan(children: spans),
    );
  }

  Widget _buildLinkButton(String link, bool isUser) {
    return Container(
      margin: const EdgeInsets.only(bottom: 4),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(8),
          onTap: () => _launchUrl(link),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: isUser
                  ? Colors.white.withOpacity(0.2)
                  : const Color(0xFF667eea).withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(
                color: isUser
                    ? Colors.white.withOpacity(0.3)
                    : const Color(0xFF667eea).withOpacity(0.3),
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  Icons.link,
                  size: 16,
                  color: isUser ? Colors.white : const Color(0xFF667eea),
                ),
                const SizedBox(width: 8),
                Flexible(
                  child: Text(
                    link,
                    style: TextStyle(
                      color: isUser ? Colors.white : const Color(0xFF667eea),
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                      decoration: TextDecoration.underline,
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _launchUrl(String url) async {
    try {
      // url_launcher 패키지가 필요하지만 일단 print로 대체
      print('링크 클릭: $url');
      // 실제로는 url_launcher를 사용하여 브라우저에서 열어야 합니다
    } catch (e) {
      print('링크 열기 실패: $e');
    }
  }
}
