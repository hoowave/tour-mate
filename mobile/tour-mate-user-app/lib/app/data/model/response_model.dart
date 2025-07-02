class ResponseModel{
  ResponseModel({
    required this.status,
    required this.message,
    this.data,
  });
  final bool status;
  final String message;
  final dynamic data;

  factory ResponseModel.fromJson(Map<String, dynamic> json) {
    return ResponseModel(
      status: json['status'] ?? false,
      message: json['message'] ?? '',
      data: json['data'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status,
      'message': message,
      'data': data,
    };
  }
}

