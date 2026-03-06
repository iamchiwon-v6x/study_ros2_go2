# ROS 2 Humble Dev Environment

ROS 2 Humble 학습 및 개발을 위한 devcontainer 환경.

## 환경 구성

- **Base Image**: `osrf/ros:humble-desktop`
- **ROS Distro**: Humble Hawksbill (Ubuntu 22.04)
- **포함 도구**: python3-pip, git, vim

## 시작하기

### 1. devcontainer 열기

VS Code에서 이 폴더를 열고 `Reopen in Container` 실행.

### 2. ROS 2 동작 확인

```bash
./test_ros2.sh
```

정상이면 아래 항목이 모두 통과한다:

- `ROS_DISTRO: humble`
- `ros2 doctor` 리포트 출력
- `ros2 topic list`에서 `/rosout`, `/parameter_events` 출력

### 3. Pub/Sub 직접 테스트

터미널 2개를 열고:

```bash
# 터미널 1: 구독
ros2 topic echo /chatter std_msgs/msg/String

# 터미널 2: 발행
ros2 topic pub /chatter std_msgs/msg/String "data: 'hello ros2'" --once
```

터미널 1에서 `data: 'hello ros2'`가 출력되면 정상.

## 설치된 패키지

| 패키지 | 용도 |
|--------|------|
| ros-humble-desktop | ROS 2 기본 + rviz2, rqt 등 GUI 도구 |

> 패키지 추가 시 이 표를 업데이트할 것.
