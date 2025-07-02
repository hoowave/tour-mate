import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../controllers/home_controller.dart';

class InfoModal {
  static void show(HomeController controller) {
    Get.dialog(
      AlertDialog(
        title: const Text('사용자 정보 입력'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // 나이 그룹
              Obx(() => DropdownButtonFormField<String>(
                    value: controller.ageGroup.value.isEmpty
                        ? null
                        : controller.ageGroup.value,
                    items: ['10대', '20대', '30대', '40대', '50대', '60대']
                        .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                        .toList(),
                    onChanged: (v) => controller.ageGroup.value = v ?? '',
                    decoration: const InputDecoration(labelText: '나이 그룹'),
                  )),
              const SizedBox(height: 12),
              // 성별
              Obx(() => DropdownButtonFormField<String>(
                    value: controller.gender.value.isEmpty
                        ? null
                        : controller.gender.value,
                    items: ['남성', '여성']
                        .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                        .toList(),
                    onChanged: (v) => controller.gender.value = v ?? '',
                    decoration: const InputDecoration(labelText: '성별'),
                  )),
              const SizedBox(height: 12),
              // 테마
              Obx(() => DropdownButtonFormField<String>(
                    value: controller.theme.value.isEmpty
                        ? null
                        : controller.theme.value,
                    items: ['자연', '도시', '맛집', '역사', '휴양', '액티비티']
                        .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                        .toList(),
                    onChanged: (v) => controller.theme.value = v ?? '',
                    decoration: const InputDecoration(labelText: '여행 테마'),
                  )),
              const SizedBox(height: 12),
              // 여행 날짜(몇박)
              Obx(() => Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('여행 기간(몇박)', style: TextStyle(fontSize: 16)),
                      Slider(
                        value: (int.tryParse(controller.days.value) ?? 1)
                            .toDouble(),
                        min: 1,
                        max: 14,
                        divisions: 13,
                        label:
                            '${controller.days.value.isEmpty ? 1 : controller.days.value}박',
                        onChanged: (v) {
                          controller.days.value = v.toInt().toString();
                        },
                      ),
                      Text(
                        '${controller.days.value.isEmpty ? 1 : controller.days.value}박',
                        style: const TextStyle(fontSize: 14),
                      ),
                    ],
                  )),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () {
              // 필수값 체크 등 추가 가능
              Get.back();
            },
            child: const Text('확인'),
          ),
        ],
      ),
      barrierDismissible: false,
    );
  }
}
