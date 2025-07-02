import 'package:http/http.dart' as http;

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

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
}
