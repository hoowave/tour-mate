import 'package:get/get.dart';
import 'package:tour_mate_user_app/app/data/service/networking/api_service.dart';

import '../controllers/home_controller.dart';

class HomeBinding extends Bindings {
  @override
  void dependencies() {
    Get.put(
      HomeController(
        Get.find<ApiService>(),
      ),
    );
  }
}
