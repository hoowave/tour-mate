import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'dart:typed_data';
import '../../../data/service/networking/api_service.dart';

class GraphController extends GetxController {
  final graphImageBytes = Rx<Uint8List?>(null);
  final isLoading = false.obs;
  final error = ''.obs;

  @override
  void onInit() {
    super.onInit();
    fetchGraph();
  }

  Future<void> fetchGraph() async {
    isLoading.value = true;
    error.value = '';

    try {
      final url = '${ApiService.baseUrl}/api/graph';
      print('그래프 API 요청 URL: $url');

      final response = await http.get(Uri.parse(url));

      print('그래프 응답 상태코드: ${response.statusCode}');
      print('그래프 응답 타입: ${response.headers['content-type']}');

      if (response.statusCode == 200) {
        // 이미지 데이터를 바이트로 저장
        graphImageBytes.value = response.bodyBytes;
        print('그래프 이미지 데이터 수신 완료 (${response.bodyBytes.length} bytes)');
      } else {
        error.value = '서버 오류: ${response.statusCode}';
        print('그래프 API 오류: ${response.body}');
      }
    } catch (e) {
      error.value = '네트워크 오류: $e';
      print('그래프 API 요청 오류: $e');
    } finally {
      isLoading.value = false;
    }
  }

  @override
  void onReady() {
    super.onReady();
  }

  @override
  void onClose() {
    super.onClose();
  }
}
