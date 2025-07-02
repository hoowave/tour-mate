import 'package:get/get.dart';
import 'package:tour_mate_user_app/app/data/service/networking/api_service.dart';

class AppBinding extends Bindings {
  @override
  void dependencies() {
    Get.put<ApiService>(ApiService(), permanent: true);
  }
}