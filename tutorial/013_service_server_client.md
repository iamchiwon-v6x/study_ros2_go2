# 013. 서비스 Server/Client 작성

1부에서 서비스가 **요청-응답** 패턴이라는 것을 배웠다.
이번에는 서비스 **Server**와 **Client**를 직접 Python으로 작성한다.

## Server와 Client

서비스 통신에는 두 역할이 있다:

| 역할 | 하는 일 |
|------|---------|
| **Server** | 서비스를 등록하고, 요청이 오면 처리 후 응답을 보냄 |
| **Client** | 서비스에 요청을 보내고, 응답을 기다림 |

토픽의 Publisher/Subscriber가 "방송"이라면, 서비스의 Server/Client는 "전화 통화"에 비유할 수 있다.

## 사전 조건

- `my_first_pkg` 패키지가 빌드된 상태
- 워크스페이스: `/workspaces/ros2_go2/ros2_ws`

## 1. Service Server 작성

turtlesim의 `AddTwoInts` 같은 간단한 예제 대신, 실용적인 예제를 만든다.
turtlesim에 새 거북이를 소환하는 서비스를 **호출하는** Server를 만들어보자.

먼저, ROS 2에 포함된 `example_interfaces`의 `AddTwoInts` 서비스로 기본 구조를 익힌다.

```python
# /workspaces/ros2_go2/ros2_ws/src/my_first_pkg/my_first_pkg/add_server.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddServer(Node):
    def __init__(self):
        super().__init__('add_server')
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_callback
        )
        self.get_logger().info('Add Server ready.')

    def add_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            f'Request: {request.a} + {request.b} = {response.sum}'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AddServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 코드 해설

| 코드 | 설명 |
|------|------|
| `create_service(타입, 이름, 콜백)` | 서비스 서버 등록 |
| `add_callback(request, response)` | 요청 처리 후 응답 반환 |
| `request.a`, `request.b` | 요청 필드 (srv 정의에 따라 결정) |
| `response.sum` | 응답 필드 |
| `return response` | 반드시 response를 반환해야 한다 |

`AddTwoInts.srv`의 구조는 다음과 같다:

```
int64 a
int64 b
---
int64 sum
```

`---`를 기준으로 위가 Request, 아래가 Response다.

## 2. Service Client 작성

```python
# /workspaces/ros2_go2/ros2_ws/src/my_first_pkg/my_first_pkg/add_client.py
import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddClient(Node):
    def __init__(self):
        super().__init__('add_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        # 서버가 준비될 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for server...')

    def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        future = self.client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)
    node = AddClient()

    a = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    future = node.send_request(a, b)
    rclpy.spin_until_future_complete(node, future)

    result = future.result()
    node.get_logger().info(f'Result: {a} + {b} = {result.sum}')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 코드 해설

| 코드 | 설명 |
|------|------|
| `create_client(타입, 이름)` | 클라이언트 생성 |
| `wait_for_service(timeout_sec=1.0)` | 서버가 준비될 때까지 대기 |
| `call_async(request)` | **비동기** 요청 전송, Future 반환 |
| `spin_until_future_complete(node, future)` | 응답이 올 때까지 spin |
| `future.result()` | 응답 결과 가져오기 |

중요한 점은 **`call_async`**를 사용한다는 것이다. 동기 호출(`call`)도 있지만, ROS 2에서는 비동기가 권장된다. 동기 호출은 응답을 기다리는 동안 노드의 다른 콜백이 모두 멈추기 때문이다.

## 3. entry_points 등록 및 빌드

`setup.py`에 추가:

```python
'add_server = my_first_pkg.add_server:main',
'add_client = my_first_pkg.add_client:main',
```

빌드:

```bash
cd /workspaces/ros2_go2/ros2_ws
colcon build --packages-select my_first_pkg --symlink-install
source install/setup.bash
```

## 4. 실행

터미널 1 — Server:
```bash
ros2 run my_first_pkg add_server
```

```
[INFO] [add_server]: Add Server ready.
```

터미널 2 — Client:
```bash
ros2 run my_first_pkg add_client 10 20
```

```
[INFO] [add_client]: Result: 10 + 20 = 30
```

Server 터미널에도 로그가 출력된다:

```
[INFO] [add_server]: Request: 10 + 20 = 30
```

## 5. Turtlesim 서비스 Client

기존 turtlesim 서비스를 호출하는 Client를 만들어보자. 거북이를 소환하고 색상을 바꾸는 예제다.

```python
# /workspaces/ros2_go2/ros2_ws/src/my_first_pkg/my_first_pkg/spawn_turtle.py
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn


class SpawnTurtle(Node):
    def __init__(self):
        super().__init__('spawn_turtle')
        self.client = self.create_client(Spawn, '/spawn')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /spawn service...')

    def spawn(self, x, y, theta, name):
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = name
        future = self.client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)
    node = SpawnTurtle()

    future = node.spawn(3.0, 3.0, 0.0, 'my_turtle')
    rclpy.spin_until_future_complete(node, future)

    result = future.result()
    node.get_logger().info(f'Spawned turtle: {result.name}')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

`setup.py`에 추가 후 빌드하고 실행하면 turtlesim에 새 거북이가 나타난다.

## 6. 동기 vs 비동기 호출 비교

| 방식 | 코드 | 특징 |
|------|------|------|
| 동기 | `client.call(request)` | 응답 올 때까지 블로킹, 다른 콜백 중단 |
| 비동기 | `client.call_async(request)` | Future 반환, spin 중 다른 콜백 정상 동작 |

ROS 2에서는 **비동기 호출(`call_async`)을 권장**한다. 실무에서도 대부분 비동기를 사용한다.

## 정리

| 개념 | 설명 |
|------|------|
| `create_service(타입, 이름, 콜백)` | 서비스 서버 생성 |
| `create_client(타입, 이름)` | 서비스 클라이언트 생성 |
| `call_async(request)` | 비동기 서비스 호출 |
| `spin_until_future_complete()` | 응답 대기 |

## 핵심 포인트

- Server는 `create_service`로 등록하고, 콜백에서 request를 처리하여 response를 반환한다
- Client는 `call_async`로 비동기 요청을 보내고 Future로 결과를 받는다
- `wait_for_service`로 서버 준비 상태를 확인하는 것이 안전하다
- 동기 호출보다 **비동기 호출**을 사용하라

> **다음 튜토리얼**: [014. 액션 Server/Client 작성](014_action_server_client.md)에서 피드백을 제공하는 장시간 작업을 구현한다.
