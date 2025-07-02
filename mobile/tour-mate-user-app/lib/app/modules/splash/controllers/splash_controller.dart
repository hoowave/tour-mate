import 'dart:async';
import 'package:get/get.dart';

import '../../../routes/app_pages.dart';

class SplashController extends GetxController {

  @override
  void onInit() {
    super.onInit();
  }

  @override
  void onReady() {
    super.onReady();
    Timer(const Duration(seconds: 3), () {
      Get.offNamed(Routes.HOME);
    });
  }

  @override
  void onClose() {
    super.onClose();
  }
}
