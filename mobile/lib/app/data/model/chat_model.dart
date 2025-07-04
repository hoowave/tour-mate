class ChatModel {
  ChatModel({
    required this.senderId,
    required this.message,
    required this.timestamp,
    this.links,
  });

  final String senderId;
  final String message;
  final DateTime timestamp;
  final List<String>? links;

  factory ChatModel.fromUser(String message) {
    return ChatModel(
      senderId: "user",
      message: message,
      timestamp: DateTime.now(),
    );
  }

  factory ChatModel.fromAI(String message) {
    // 메시지에서 웹 링크 추출
    final links = _extractLinks(message);

    return ChatModel(
      senderId: "ai",
      message: message,
      timestamp: DateTime.now(),
      links: links.isNotEmpty ? links : null,
    );
  }

  // 웹 링크 추출 메서드 (이미지 제외)
  static List<String> _extractLinks(String message) {
    final urlPattern = RegExp(
      r'https?://[^\s<>"]+',
      caseSensitive: false,
    );

    final matches = urlPattern.allMatches(message);
    final links = <String>[];

    for (final match in matches) {
      final url = match.group(0)!;
      // 이미지 파일 확장자 제외
      if (!RegExp(r'\.(jpg|jpeg|png|gif|webp|svg)(\?[^\s<>"]*)?$',
              caseSensitive: false)
          .hasMatch(url)) {
        links.add(url);
      }
    }

    print('원본 메시지: $message');
    print('추출된 링크: $links');

    return links;
  }

  // 링크가 있는지 확인
  bool get hasLinks => links != null && links!.isNotEmpty;
}

// API 응답용 모델
class ChatResponse {
  final String reply;

  ChatResponse({required this.reply});

  factory ChatResponse.fromJson(Map<String, dynamic> json) {
    return ChatResponse(
      reply: json['reply'] ?? '',
    );
  }
}
