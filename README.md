# ROS 2 Foxy Dev Environment (Go2 동일 환경)

Go2 Jetson 실기기와 동일한 ROS 2 Foxy 환경에서 학습 및 개발하기 위한 devcontainer 환경.

## Go2 실기기 ↔ 개발환경 대응표

| 항목 | Go2 Jetson (실기기) | 개발 컨테이너 |
|------|---------------------|---------------|
| OS | Ubuntu 20.04.5 LTS | Ubuntu 20.04 (Foxy 베이스) |
| ROS 2 | Foxy + CycloneDDS | Foxy + CycloneDDS |
| Python | 3.8.10 | 3.8.x |
| DDS | rmw_cyclonedds_cpp | rmw_cyclonedds_cpp |
| CPU | ARMv8 aarch64 (Orin Nano) | x86_64 (호스트 PC) |
| GUI | 직접 연결 | noVNC (`http://localhost:6080`) |

> ⚠️ CPU 아키텍처(aarch64 vs x86_64)만 다릅니다. ROS 2 API, Python 버전, DDS 설정은 동일합니다.

## 시작하기

1. VS Code에서 이 폴더를 열고 `Reopen in Container` 실행
2. 브라우저에서 http://localhost:6080 접속 → 비밀번호 `vscode` 입력 → Connect
3. CycloneDDS 확인: `echo $RMW_IMPLEMENTATION` → `rmw_cyclonedds_cpp` 출력되면 정상

## 설치된 패키지

| 패키지 | 용도 | Go2 상태 |
|--------|------|----------|
| ros-foxy-desktop | ROS 2 기본 + rviz2, rqt 등 GUI 도구 | ✅ |
| ros-foxy-turtlesim | ROS 2 학습용 시뮬레이터 | — |
| ros-foxy-rmw-cyclonedds-cpp | Go2 통신 미들웨어 | ✅ |
| ros-foxy-nav2-map-server | SLAM 맵 저장 도구 | ✅ |
| ros-foxy-tf2-tools | 좌표 변환(TF) 디버깅 도구 | ✅ |
| ros-foxy-slam-toolbox | 2D SLAM 맵 생성 엔진 | 설치 예정 |
| ros-foxy-pointcloud-to-laserscan | 3D→2D LiDAR 변환 | 설치 예정 |
| tmux | SSH 세션 유지 | 설치 예정 |
| desktop-lite (devcontainer feature) | 브라우저 기반 GUI 표시 (noVNC) | — |

> 패키지 추가 시 이 표를 업데이트할 것.

## Tutorial

### 1부: ROS 2 기본 개념 (CLI로 익히기)

| # | 제목 | 파일 |
|---|------|------|
| 001 | ROS 2 동작 환경 확인하기 | [001_verify_ros2_setup.md](tutorial/001_verify_ros2_setup.md) |
| 002 | Turtlesim으로 ROS 2 체험하기 | [002_turtlesim.md](tutorial/002_turtlesim.md) |
| 003 | 노드 이해하기 | [003_node.md](tutorial/003_node.md) |
| 004 | 토픽 깊이 파보기 | [004_topic.md](tutorial/004_topic.md) |
| 005 | 서비스 이해하기 | [005_service.md](tutorial/005_service.md) |
| 006 | 액션 이해하기 | [006_action.md](tutorial/006_action.md) |
| 007 | 파라미터 다루기 | [007_parameter.md](tutorial/007_parameter.md) |
| 008 | RQt 도구 활용 | [008_rqt_tools.md](tutorial/008_rqt_tools.md) |
| 009 | Bag 녹화와 재생 | [009_bag.md](tutorial/009_bag.md) |

### 2부: Python으로 ROS 2 프로그래밍

| # | 제목 | 파일 |
|---|------|------|
| 010 | 패키지 만들기 | [010_create_package.md](tutorial/010_create_package.md) |
| 011 | 토픽 Publisher 작성 | [011_topic_publisher.md](tutorial/011_topic_publisher.md) |
| 012 | 토픽 Subscriber 작성 | [012_topic_subscriber.md](tutorial/012_topic_subscriber.md) |
| 013 | 서비스 Server/Client 작성 | [013_service_server_client.md](tutorial/013_service_server_client.md) |
| 014 | 액션 Server/Client 작성 | [014_action_server_client.md](tutorial/014_action_server_client.md) |
| 015 | 커스텀 인터페이스 정의 | [015_custom_interface.md](tutorial/015_custom_interface.md) |
| 016 | 파라미터 프로그래밍 | [016_parameter_programming.md](tutorial/016_parameter_programming.md) |
| 017 | Launch 파일 작성 | [017_launch_file.md](tutorial/017_launch_file.md) |

### 3부: Unitree Go2 시뮬레이션과 제어

| # | 제목 | 파일 |
|---|------|------|
| 018 | Go2 개발 환경 구축 (unitree_mujoco + SDK) | tutorial/018_go2_dev_setup.md |
| 019 | MuJoCo 시뮬레이터 구조 이해하기 | tutorial/019_mujoco_structure.md |
| 020 | unitree_sdk2로 Go2 직접 제어 | tutorial/020_sdk2_direct_control.md |
| 021 | unitree_ros2 브릿지 설정하기 | tutorial/021_ros2_bridge_setup.md |
| 022 | ROS 2 토픽으로 Go2 상태 읽기 | tutorial/022_go2_state_topics.md |
| 023 | ROS 2로 Go2 모션 명령 보내기 | tutorial/023_go2_motion_control.md |
| 024 | Go2 센서 데이터 활용 (IMU, 카메라) | tutorial/024_go2_sensors.md |
| 025 | Go2 제어 노드 패키지 만들기 | tutorial/025_go2_control_package.md |
| 026 | Launch로 Go2 시스템 통합하기 | tutorial/026_go2_launch_system.md |
| 027 | 실기기 전환과 배포 | tutorial/027_deploy_to_real_robot.md |
