# NAV2-Yahboom

LMS 전용 템플릿 저장소입니다. 설치 폴더: `[lms-nav2-yahboom-vehicle]yahboom_vehicle_v1.0.0_ws`

- 패키지: `yahboom_vehicle`
- 런치: `vehicle.launch.py`
- 이미지: `future-nav2:humble-yahboom` (실차 기본)
- 로컬 시뮬레이션: 빌드 전에 `sim_mode:=true`를 설정하면 LMS가
  `future-nav2-gazebo:humble`을 사용합니다. 기본값은 `true`이며 실차에서는 `sim_mode:=false`를 명시합니다.
- 시뮬레이션에서는 기존 NAV2-Gazebo에 `platform:=yahboom`을 설정하고
  NAV2-Yahboom 차량 모듈을 함께 실행합니다. 실차 Agent/Camera는 실행하지 않습니다.
- 앱의 야붐 실행기 지원이 반영되어야 합니다.
- 서버 과정의 야붐 전용 환경에 이 모듈과 이미지 아티팩트를 등록한 후
  LMS에서 설치 -> 빌드 -> 실행합니다.
- ROS_DOMAIN_ID는 ESP32 설정과 일치시킵니다. GPU 가속은 끕니다.
- 컨테이너 장치: 없음
- SLAM과 Localization은 동시에 실행하지 않습니다.
- `/vehicle_config`를 발행합니다 (`robot=yahboom`, `level=2d`, `sim_mode`).
  야붐 설정이 추가된 공통 NAV2-SLAM, NAV2-Map, NAV2-Localization,
  NAV2-Planning, NAV2-Control을 사용합니다. 전용 Yahboom 주행 모듈과 중복 실행하지 않습니다.
- 실차 검증 전 소스입니다. 바퀴를 띄우고 비상정지와 명령 타임아웃을 확인하세요.

원본 소스: https://github.com/KingKiser/hkit_yahboom_ws
작성자 박승휘, 원본 package.xml 저작자 Leo Cho, 원본 라이선스 표기 Apache 2.0.
재배포 전 자산 라이선스를 확인하세요.
