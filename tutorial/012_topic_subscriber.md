# 012. 토픽 Subscriber 작성

앞에서 Publisher를 만들어 메시지를 발행했다.
이번에는 **Subscriber 노드**를 만들어 토픽 메시지를 수신하고 처리하는 법을 배운다.

## Subscriber의 구조

Subscriber는 특정 토픽을 구독하고, 메시지가 도착하면 **콜백 함수**가 호출된다.

1. 노드 생성 → 2. Subscription 객체 생성 → 3. spin으로 대기 → 4. 메시지 도착 시 콜백 실행

Publisher가 타이머로 능동적으로 발행하는 것과 달리, Subscriber는 **수동적으로 메시지를 기다린다**.

## 사전 조건

- [011. 토픽 Publisher 작성](011_topic_publisher.md)에서 만든 `simple_publisher` 노드
- 워크스페이스: `~/ros2_ws`

## 1. Subscriber 노드 작성

```bash
cat << 'PYEOF' > ~/ros2_ws/src/my_first_pkg/my_first_pkg/simple_subscriber.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__('simple_subscriber')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = SimpleSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

### 코드 해설

| 코드 | 설명 |
|------|------|
| `create_subscription(String, 'chatter', callback, 10)` | `chatter` 토픽 구독, 메시지 도착 시 `callback` 호출 |
| `listener_callback(self, msg)` | 콜백 함수, `msg`에 수신된 메시지가 들어온다 |
| `msg.data` | `String` 메시지의 내용 필드 |

Publisher의 `create_publisher`와 비교하면:

| Publisher | Subscriber |
|-----------|------------|
| `create_publisher(타입, 토픽, 큐)` | `create_subscription(타입, 토픽, 콜백, 큐)` |
| `create_timer`로 발행 시점 결정 | 메시지 도착 시 자동 호출 |
| 능동적 | 수동적 (이벤트 기반) |

## 2. entry_points 등록

`setup.py`에 추가:

```python
entry_points={
    'console_scripts': [
        'hello = my_first_pkg.hello_node:main',
        'simple_pub = my_first_pkg.simple_publisher:main',
        'simple_sub = my_first_pkg.simple_subscriber:main',
        'turtle_circle = my_first_pkg.turtle_circle:main',
    ],
},
```

## 3. 빌드와 실행

```bash
cd ~/ros2_ws
colcon build --packages-select my_first_pkg --symlink-install
source install/setup.bash
```

터미널 1 — Publisher:
```bash
ros2 run my_first_pkg simple_pub
```

터미널 2 — Subscriber:
```bash
ros2 run my_first_pkg simple_sub
```

```
[INFO] [simple_subscriber]: Received: "Hello ROS 2: 0"
[INFO] [simple_subscriber]: Received: "Hello ROS 2: 1"
[INFO] [simple_subscriber]: Received: "Hello ROS 2: 2"
```

## 4. 터틀 위치 모니터링 Subscriber

turtlesim의 위치 데이터를 구독하여 화면에 표시하는 실용적인 예제를 만들어보자.

```bash
cat << 'PYEOF' > ~/ros2_ws/src/my_first_pkg/my_first_pkg/turtle_monitor.py
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


class TurtleMonitor(Node):
    def __init__(self):
        super().__init__('turtle_monitor')
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

    def pose_callback(self, msg):
        self.get_logger().info(
            f'Position: ({msg.x:.2f}, {msg.y:.2f}), '
            f'Angle: {msg.theta:.2f} rad, '
            f'Speed: {msg.linear_velocity:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TurtleMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

`turtlesim.msg.Pose` 메시지의 필드:

| 필드 | 타입 | 의미 |
|------|------|------|
| `x` | float | X 좌표 |
| `y` | float | Y 좌표 |
| `theta` | float | 방향 (라디안) |
| `linear_velocity` | float | 선속도 |
| `angular_velocity` | float | 각속도 |

`setup.py`에 추가:

```python
'turtle_monitor = my_first_pkg.turtle_monitor:main',
```

### 실행

터미널 1:
```bash
ros2 run turtlesim turtlesim_node
```

터미널 2:
```bash
ros2 run turtlesim turtle_teleop_key
```

터미널 3:
```bash
cd ~/ros2_ws && colcon build --packages-select my_first_pkg --symlink-install
source install/setup.bash
ros2 run my_first_pkg turtle_monitor
```

키보드로 터틀을 움직이면 실시간으로 위치가 출력된다.

## 5. Pub/Sub 조합 — 자율 회피 노드

Publisher와 Subscriber를 **하나의 노드**에 결합할 수 있다. 위치를 구독하면서 벽에 가까워지면 방향을 바꾸는 노드를 만들어보자.

```bash
cat << 'PYEOF' > ~/ros2_ws/src/my_first_pkg/my_first_pkg/turtle_boundary.py
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class TurtleBoundary(Node):
    def __init__(self):
        super().__init__('turtle_boundary')
        # Subscriber: 위치 수신
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )
        # Publisher: 속도 명령 발행
        self.publisher_ = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )
        self.pose = None

    def pose_callback(self, msg):
        self.pose = msg
        cmd = Twist()

        # 벽 근처(1.0 이하 또는 10.0 이상)이면 중앙으로 회전
        if msg.x < 1.0 or msg.x > 10.0 or msg.y < 1.0 or msg.y > 10.0:
            cmd.linear.x = 0.5
            cmd.angular.z = 1.5
            self.get_logger().warn('Near wall! Turning...')
        else:
            cmd.linear.x = 2.0
            cmd.angular.z = 0.0

        self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleBoundary()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

이 패턴 — **구독한 데이터를 기반으로 발행** — 은 로봇 소프트웨어에서 가장 기본적인 구조다. 센서 데이터를 받아서 제어 명령을 내리는 모든 노드가 이 구조를 따른다.

`setup.py`에 추가:

```python
'turtle_boundary = my_first_pkg.turtle_boundary:main',
```

## 정리

| 개념 | 설명 |
|------|------|
| `create_subscription(타입, 토픽, 콜백, 큐)` | 토픽 구독 설정 |
| 콜백 함수 | 메시지 도착 시 자동 호출 |
| Pub + Sub 조합 | 센서 수신 → 제어 발행 패턴 |

## 핵심 포인트

- Subscriber는 `create_subscription`으로 생성하며, 콜백이 핵심이다
- 콜백 안에서 수신된 메시지를 자유롭게 처리할 수 있다
- 하나의 노드에 Publisher와 Subscriber를 함께 넣을 수 있다
- **수신 → 처리 → 발행** 패턴이 로봇 소프트웨어의 기본 골격이다

> **다음 튜토리얼**: [013. 서비스 Server/Client 작성](013_service_server_client.md)에서 요청-응답 패턴을 Python으로 구현한다.
