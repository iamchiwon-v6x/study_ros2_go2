# 003. 노드 이해하기

ROS 2 시스템은 **노드(Node)**의 집합이다. 이 튜토리얼에서는 노드의 개념을 깊이 이해하고,
CLI로 노드를 조회·관리하는 방법을 배운다.

## 노드란?

노드는 **하나의 책임을 가진 독립 프로세스**다.
로봇 시스템을 하나의 거대한 프로그램으로 만드는 대신, 기능별로 쪼개서 각각을 노드로 구현한다.

예를 들어 자율주행 로봇은 이런 식으로 나뉜다:

| 노드 | 역할 |
|------|------|
| camera_node | 카메라에서 이미지 수집 |
| lidar_node | 라이다에서 포인트 클라우드 수집 |
| perception_node | 센서 데이터로 장애물 인식 |
| planner_node | 경로 계획 |
| motor_node | 모터에 속도 명령 전달 |

이렇게 나누는 이유:

- **독립 개발**: 각 노드를 다른 사람이, 다른 언어로 개발할 수 있다
- **독립 실행**: 하나가 죽어도 나머지는 계속 동작한다
- **재사용**: camera_node를 다른 로봇에서도 그대로 쓸 수 있다
- **교체 용이**: lidar_node를 다른 센서 노드로 바꿔도 나머지 코드는 그대로다

## 사전 조건

- devcontainer 실행 중

## 1. Turtlesim 노드 실행

```bash
ros2 run turtlesim turtlesim_node
```

별도 터미널에서:

```bash
ros2 run turtlesim turtle_teleop_key
```

## 2. 노드 목록 확인

새 터미널에서:

```bash
ros2 node list
```

```
/turtlesim
/teleop_turtle
```

현재 실행 중인 모든 노드가 표시된다. 앞의 `/`는 **네임스페이스**를 나타낸다.
네임스페이스는 여러 로봇을 같은 시스템에서 운영할 때 이름 충돌을 방지하는 역할을 한다.

## 3. 노드 상세 정보 확인

```bash
ros2 node info /turtlesim
```

```
/turtlesim
  Subscribers:
    /turtle1/cmd_vel: geometry_msgs/msg/Twist
  Publishers:
    /turtle1/color_sensor: turtlesim/msg/Color
    /turtle1/pose: turtlesim/msg/Pose
  Service Servers:
    /turtle1/set_pen: turtlesim/srv/SetPen
    /turtle1/teleport_absolute: turtlesim/srv/TeleportAbsolute
    ...
```

한 노드가 **어떤 토픽을 발행/구독**하고, **어떤 서비스를 제공**하는지 한눈에 볼 수 있다.
새로운 노드를 처음 접할 때 가장 먼저 실행하는 명령어다.

## 4. 노드 이름 변경 (Remapping)

같은 노드를 두 개 실행하면 이름이 충돌한다.
`--ros-args -r __node:=새이름` 으로 이름을 바꿔서 실행할 수 있다:

```bash
ros2 run turtlesim turtlesim_node --ros-args -r __node:=my_turtle
```

확인:

```bash
ros2 node list
```

```
/turtlesim
/teleop_turtle
/my_turtle
```

Remapping은 이름뿐 아니라 토픽 이름도 바꿀 수 있다.
같은 프로그램을 다른 설정으로 여러 번 실행할 때 핵심적인 기능이다.

## 5. 실행 중인 노드 확인 (실습)

다음 명령으로 현재 시스템의 전체 모습을 파악해보자:

```bash
# 모든 노드
ros2 node list

# 각 노드의 상세 정보
ros2 node info /turtlesim
ros2 node info /teleop_turtle
```

`/teleop_turtle`은 **Publisher만** 가지고 있고, `/turtlesim`은 **Subscriber와 Publisher 모두** 가지고 있다는 점을 확인하자. teleop은 명령만 보내는 역할이고, turtlesim은 명령을 받으면서 동시에 상태(위치)를 발행하는 역할이다.

## 정리

| 명령어 | 역할 |
|--------|------|
| `ros2 node list` | 실행 중인 노드 목록 |
| `ros2 node info <노드>` | 노드의 토픽/서비스/액션 정보 |
| `--ros-args -r __node:=이름` | 노드 이름 변경 (remapping) |

**이 튜토리얼에서 배운 것:**

- 노드는 하나의 책임을 가진 독립 프로세스다
- `ros2 node info`로 노드가 사용하는 토픽과 서비스를 파악할 수 있다
- Remapping으로 같은 프로그램을 다른 이름/설정으로 동시에 실행할 수 있다

다음 튜토리얼에서는 노드 사이를 연결하는 **토픽**을 더 깊이 살펴본다.
