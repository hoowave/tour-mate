import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  // 플랫폼별 base URL 설정
  static String get baseUrl {
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000'; // Android 에뮬레이터
    } else if (Platform.isIOS) {
      return 'http://localhost:8000'; // iOS 시뮬레이터
    } else {
      return 'http://127.0.0.1:8000'; // 웹/데스크톱
    }
  }

  Future<http.Response> getRequest(String url) async {
    return await http.get(Uri.parse(url));
  }

  Future<http.Response> postRequest(
      String url, Map<String, dynamic> data) async {
    return await http.post(
      Uri.parse(url),
      body: data,
    );
  }

  // Chat API 요청 메서드
  Future<http.Response> sendChatMessage({
    required String age,
    required String gender,
    required String theme,
    required String message,
    required String duration,
  }) async {
    final url = '$baseUrl/api/chat';
    print('API 요청 URL: $url');

    final requestData = {
      'age': age,
      'gender': gender,
      'theme': theme,
      'message': message,
      'duration': duration,
    };

    print('요청 데이터: $requestData');

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode(requestData),
      );

      print('응답 상태코드: ${response.statusCode}');
      print('응답 바디: ${response.body}');
      print('응답 타입: ${response.headers['content-type']}');

      return response;
    } catch (e) {
      print('API 요청 오류: $e');
      rethrow;
    }
  }
}
