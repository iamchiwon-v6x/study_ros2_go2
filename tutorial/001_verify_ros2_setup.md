# 001. ROS 2 동작 환경 확인하기

devcontainer를 열고 ROS 2가 정상적으로 설치되어 동작하는지 확인한다.

## 사전 조건

- VS Code에서 `Reopen in Container` 실행 완료

## 1. 환경변수 확인

```bash
echo $ROS_DISTRO
```

`humble`이 출력되면 정상.

## 2. ROS 2 CLI 확인

```bash
ros2 doctor --report | head -10
```

네트워크 정보가 출력되면 ros2 명령어가 정상 동작하는 것이다.

## 3. 토픽 리스트 확인

```bash
ros2 topic list
```

아래 두 토픽이 보이면 ROS 2 데몬이 정상 기동된 것이다:

```
/parameter_events
/rosout
```

## 4. Pub/Sub 테스트

ROS 2의 핵심 통신 방식인 토픽 발행(publish)과 구독(subscribe)을 직접 테스트한다.

### 4-1. 터미널 1: 구독자 실행

```bash
ros2 topic echo /chatter std_msgs/msg/String
```

실행하면 메시지를 기다리며 대기한다.

### 4-2. 터미널 2: 발행자 실행

새 터미널을 열고:

```bash
ros2 topic pub /chatter std_msgs/msg/String "data: 'hello ros2'" --once
```

### 4-3. 결과 확인

터미널 1에 아래와 같이 출력되면 성공:

```
data: hello ros2
---
```

## 5. 자동 테스트 스크립트

위 과정을 한번에 확인하려면:

```bash
./test_ros2.sh
```

## 정리

- `ros2 topic list` — 현재 활성화된 토픽 목록
- `ros2 topic pub` — 토픽에 메시지 발행
- `ros2 topic echo` — 토픽의 메시지 구독
