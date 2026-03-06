# ROS 2 Humble Dev Environment

ROS 2 Humble 학습 및 개발을 위한 devcontainer 환경.

## 환경 구성

- **Base Image**: `osrf/ros:humble-desktop`
- **ROS Distro**: Humble Hawksbill (Ubuntu 22.04)
- **GUI 접속**: noVNC (브라우저에서 `localhost:6080`)
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

### 3. GUI 확인 (turtlesim)

컨테이너가 뜨면 noVNC가 자동 시작된다.

1. 브라우저에서 http://localhost:6080/vnc.html 접속
2. `Connect` 클릭
3. 터미널에서 실행:

```bash
ros2 run turtlesim turtlesim_node
```

브라우저에 파란 창과 거북이가 보이면 성공. 다른 터미널에서 키보드로 조종:

```bash
ros2 run turtlesim turtle_teleop_key
```

### 4. Pub/Sub 직접 테스트

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
| ros-humble-turtlesim | ROS 2 학습용 시뮬레이터 |
| xvfb, x11vnc, novnc | 브라우저 기반 GUI 표시 (noVNC) |

> 패키지 추가 시 이 표를 업데이트할 것.
