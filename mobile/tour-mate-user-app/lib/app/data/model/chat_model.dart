class ChatModel{
  ChatModel({
    required this.senderId,
    required this.message,
    required this.timestamp,
  });

  final String senderId;
  final String message;
  final DateTime timestamp;

  factory ChatModel.fromUser(String message) {
    return ChatModel(
      senderId: "user",
      message: message,
      timestamp: DateTime.now(),
    );
  }

  factory ChatModel.fromAI(String message) {
    return ChatModel(
      senderId: "ai",
      message: message,
      timestamp: DateTime.now(),
    );
  }

}