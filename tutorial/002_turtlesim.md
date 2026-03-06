# 002. Turtlesim으로 ROS 2 체험하기

Turtlesim은 ROS 2 학습용 시뮬레이터다. 화면에 거북이를 띄우고 토픽을 통해 조종하면서 ROS 2의 동작 원리를 직관적으로 이해할 수 있다.

## 사전 조건

- devcontainer 실행 중
- 브라우저에서 http://localhost:6080 접속 → 비밀번호 `vscode` 입력 → Connect

## 1. Turtlesim 노드 실행

```bash
ros2 run turtlesim turtlesim_node
```

브라우저(noVNC)에 파란 배경과 거북이가 보이면 성공.

## 2. 키보드로 거북이 조종

새 터미널을 열고:

```bash
ros2 run turtlesim turtle_teleop_key
```

이 터미널에 포커스를 두고 방향키를 누르면 거북이가 움직인다.

- ↑ 전진
- ↓ 후진
- ← 좌회전
- → 우회전

## 3. 토픽 관찰하기

거북이를 움직이는 동안 어떤 메시지가 오가는지 확인해 보자.

### 3-1. 활성 토픽 목록

새 터미널에서:

```bash
ros2 topic list
```

`/turtle1/cmd_vel`, `/turtle1/pose` 등이 보인다.

### 3-2. 속도 명령 토픽 관찰

```bash
ros2 topic echo /turtle1/cmd_vel
```

teleop에서 방향키를 누르면 이 터미널에 `linear`, `angular` 값이 출력된다. 키보드 입력이 토픽 메시지로 변환되어 turtlesim에 전달되는 것이다.

### 3-3. 거북이 위치 확인

```bash
ros2 topic echo /turtle1/pose
```

거북이의 현재 좌표(x, y)와 방향(theta)이 실시간으로 출력된다.

## 4. 명령어로 직접 거북이 움직이기

teleop 없이 직접 토픽을 발행해서 거북이를 움직일 수 있다:

```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```

거북이가 앞으로 가면서 좌회전한다.

## 5. 노드와 토픽 관계 시각화

```bash
ros2 run rqt_graph rqt_graph
```

noVNC 화면에 노드 간 연결 그래프가 표시된다. `teleop_turtle` → `/turtle1/cmd_vel` → `turtlesim` 흐름을 확인할 수 있다.

## 정리

- `ros2 run <패키지> <노드>` — 노드 실행
- `/turtle1/cmd_vel` — 거북이 속도 명령 토픽 (Twist 메시지)
- `/turtle1/pose` — 거북이 위치 토픽 (Pose 메시지)
- 키보드 입력 → 토픽 메시지 → 노드 동작의 흐름이 ROS 2의 기본 구조
