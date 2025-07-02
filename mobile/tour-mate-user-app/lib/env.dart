import 'package:flutter/material.dart';
import 'package:get/get_navigation/src/root/get_material_app.dart';

import 'app/routes/app_pages.dart';
import 'app_binding.dart';

enum BuildType { windows, mac }

class Env {
  static Env? _instance;

  static get instance => _instance;

  static bool get isWindows => _instance!._buildType == BuildType.windows;

  static bool get isMac => _instance!._buildType == BuildType.mac;

  static Size get appSize => const Size(400, 600);

  late BuildType _buildType;

  Env(BuildType buildType) {
    _buildType = buildType;
  }

  factory Env.newInstance(BuildType buildType) {
    _instance ??= Env(buildType);
    return _instance!;
  }

  void run() async{
    runApp(const Init());
  }
}

class Init extends StatelessWidget {
  const Init({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: "Tour Mate User App",
      initialRoute: AppPages.INITIAL,
      getPages: AppPages.routes,
      themeMode: ThemeMode.light,
      theme: ThemeData.light(),
      initialBinding: AppBinding(),
    );
  }

}