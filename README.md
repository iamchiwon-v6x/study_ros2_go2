# ROS 2 Humble Dev Environment

ROS 2 Humble 학습 및 개발을 위한 devcontainer 환경.

## 환경 구성

| 항목 | 내용 |
|------|------|
| Base Image | `osrf/ros:humble-desktop` |
| ROS Distro | Humble Hawksbill (Ubuntu 22.04) |
| GUI 접속 | noVNC — 브라우저에서 `http://localhost:6080` |
| 기본 도구 | python3-pip, git, vim |

## 시작하기

1. VS Code에서 이 폴더를 열고 `Reopen in Container` 실행
2. 브라우저에서 http://localhost:6080 접속 → 비밀번호 `vscode` 입력 → Connect

## 설치된 패키지

| 패키지 | 용도 |
|--------|------|
| ros-humble-desktop | ROS 2 기본 + rviz2, rqt 등 GUI 도구 |
| ros-humble-turtlesim | ROS 2 학습용 시뮬레이터 |
| desktop-lite (devcontainer feature) | 브라우저 기반 GUI 표시 (noVNC) |

> 패키지 추가 시 이 표를 업데이트할 것.

## Tutorial

### 1부: ROS 2 기본 개념 (CLI로 익히기)

| # | 제목 | 파일 |
|---|------|------|
| 001 | ROS 2 동작 환경 확인하기 | [001_verify_ros2_setup.md](tutorial/001_verify_ros2_setup.md) |
| 002 | Turtlesim으로 ROS 2 체험하기 | [002_turtlesim.md](tutorial/002_turtlesim.md) |
| 003 | 노드 이해하기 | tutorial/003_node.md |
| 004 | 토픽 깊이 파보기 | tutorial/004_topic.md |
| 005 | 서비스 이해하기 | tutorial/005_service.md |
| 006 | 액션 이해하기 | tutorial/006_action.md |
| 007 | 파라미터 다루기 | tutorial/007_parameter.md |
| 008 | RQt 도구 활용 | tutorial/008_rqt_tools.md |
| 009 | Bag 녹화와 재생 | tutorial/009_bag.md |

### 2부: Python으로 ROS 2 프로그래밍

| # | 제목 | 파일 |
|---|------|------|
| 010 | 패키지 만들기 | tutorial/010_create_package.md |
| 011 | 토픽 Publisher 작성 | tutorial/011_topic_publisher.md |
| 012 | 토픽 Subscriber 작성 | tutorial/012_topic_subscriber.md |
| 013 | 서비스 Server/Client 작성 | tutorial/013_service_server_client.md |
| 014 | 액션 Server/Client 작성 | tutorial/014_action_server_client.md |
| 015 | 커스텀 인터페이스 정의 | tutorial/015_custom_interface.md |
| 016 | 파라미터 프로그래밍 | tutorial/016_parameter_programming.md |
| 017 | Launch 파일 작성 | tutorial/017_launch_file.md |

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
