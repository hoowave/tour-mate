import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../controllers/home_controller.dart';

class InfoModal {
  static void show(HomeController controller) {
    Get.dialog(
      Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            gradient: const LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Colors.white, Color(0xFFf8f9ff)],
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.15),
                blurRadius: 20,
                offset: const Offset(0, 10),
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // 헤더
              Container(
                padding: const EdgeInsets.all(24),
                decoration: const BoxDecoration(
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(20),
                    topRight: Radius.circular(20),
                  ),
                  gradient: LinearGradient(
                    colors: [Color(0xFF667eea), Color(0xFF764ba2)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                ),
                child: const Row(
                  children: [
                    Icon(
                      Icons.person_add_rounded,
                      color: Colors.white,
                      size: 24,
                    ),
                    SizedBox(width: 12),
                    Text(
                      '사용자 정보 입력',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              // 컨텐츠
              Padding(
                padding: const EdgeInsets.all(24),
                child: SingleChildScrollView(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      // 나이 그룹
                      Obx(() => _buildDropdownField(
                            label: '나이',
                            value: controller.ageGroup.value.isEmpty
                                ? null
                                : controller.ageGroup.value,
                            items: ['10대', '20대', '30대', '40대', '50대', '60대'],
                            onChanged: (v) =>
                                controller.ageGroup.value = v ?? '',
                          )),
                      const SizedBox(height: 20),
                      // 성별
                      Obx(() => _buildDropdownField(
                            label: '성별',
                            value: controller.gender.value.isEmpty
                                ? null
                                : controller.gender.value,
                            items: ['남성', '여성'],
                            onChanged: (v) => controller.gender.value = v ?? '',
                          )),
                      const SizedBox(height: 20),
                      // 테마
                      Obx(() => _buildDropdownField(
                            label: '여행 테마',
                            value: controller.theme.value.isEmpty
                                ? null
                                : controller.theme.value,
                            items: ['자연', '도시', '맛집', '역사', '휴양', '액티비티'],
                            onChanged: (v) => controller.theme.value = v ?? '',
                          )),
                      const SizedBox(height: 20),
                      // 여행 날짜(몇박)
                      Obx(() => _buildSliderField(
                            label: '여행 기간',
                            value: (int.tryParse(controller.days.value) ?? 1)
                                .toDouble(),
                            onChanged: (v) =>
                                controller.days.value = v.toInt().toString(),
                            days: controller.days.value.isEmpty
                                ? '1'
                                : controller.days.value,
                          )),
                    ],
                  ),
                ),
              ),
              // 액션 버튼
              Container(
                padding: const EdgeInsets.all(24),
                child: Row(
                  children: [
                    Expanded(
                      child: Container(
                        decoration: BoxDecoration(
                          gradient: const LinearGradient(
                            colors: [Color(0xFF667eea), Color(0xFF764ba2)],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                          borderRadius: BorderRadius.circular(12),
                          boxShadow: [
                            BoxShadow(
                              color: const Color(0xFF667eea).withOpacity(0.3),
                              blurRadius: 8,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        child: Material(
                          color: Colors.transparent,
                          child: InkWell(
                            borderRadius: BorderRadius.circular(12),
                            onTap: () {
                              // 필수값 체크 등 추가 가능
                              Get.back();
                            },
                            child: Container(
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              child: const Center(
                                child: Text(
                                  '확인',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      barrierDismissible: false,
    );
  }

  static Widget _buildDropdownField({
    required String label,
    required String? value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: Color(0xFF374151),
          ),
        ),
        const SizedBox(height: 8),
        Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.grey[300]!),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.05),
                blurRadius: 4,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: DropdownButtonFormField<String>(
            value: value,
            items: items
                .map((e) => DropdownMenuItem(
                    value: e,
                    child:
                        Text(e, style: const TextStyle(color: Colors.black))))
                .toList(),
            onChanged: onChanged,
            decoration: const InputDecoration(
              border: InputBorder.none,
              contentPadding:
                  EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              hintStyle: TextStyle(color: Colors.grey),
            ),
            icon:
                const Icon(Icons.keyboard_arrow_down, color: Color(0xFF667eea)),
            dropdownColor: Colors.white,
            style: const TextStyle(fontSize: 16, color: Colors.black),
          ),
        ),
      ],
    );
  }

  static Widget _buildSliderField({
    required String label,
    required double value,
    required ValueChanged<double> onChanged,
    required String days,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: Color(0xFF374151),
          ),
        ),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.grey[300]!),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.05),
                blurRadius: 4,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            children: [
              SliderTheme(
                data: SliderTheme.of(Get.context!).copyWith(
                  activeTrackColor: const Color(0xFF667eea),
                  inactiveTrackColor: Colors.grey[300],
                  thumbColor: const Color(0xFF667eea),
                  overlayColor: const Color(0xFF667eea).withOpacity(0.2),
                  valueIndicatorColor: const Color(0xFF667eea),
                  valueIndicatorTextStyle: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                child: Slider(
                  value: value,
                  min: 1,
                  max: 14,
                  divisions: 13,
                  label: '${days}박',
                  onChanged: onChanged,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                '${days}박',
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF667eea),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
