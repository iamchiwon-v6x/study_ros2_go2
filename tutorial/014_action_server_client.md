# 014. 액션 Server/Client 작성

서비스는 단발성 요청-응답이다. 하지만 로봇이 목표 지점까지 이동하는 것처럼 **시간이 걸리는 작업**에는 진행 상황을 알려주는 **액션(Action)**이 필요하다.

이번에는 액션 Server와 Client를 직접 구현한다.

## 액션의 세 가지 요소

| 요소 | 방향 | 역할 |
|------|------|------|
| **Goal** | Client → Server | 목표 전달 |
| **Feedback** | Server → Client | 진행 상황 보고 (반복) |
| **Result** | Server → Client | 최종 결과 반환 (1회) |

## 사전 조건

- `my_first_pkg` 패키지가 빌드된 상태
- `example_interfaces` 패키지 (기본 설치됨)

이 튜토리얼에서는 turtlesim의 내장 액션 타입인 `turtlesim/action/RotateAbsolute`를 사용한다.
별도의 커스텀 액션을 정의하지 않아도 되므로, 액션의 구현 패턴에 집중할 수 있다.

## 1. 액션 타입 확인

turtlesim의 `RotateAbsolute` 액션 구조를 확인한다.

```bash
ros2 interface show turtlesim/action/RotateAbsolute
```

```
# Goal
float32 theta
---
# Result
float32 delta
---
# Feedback
float32 remaining
```

- **Goal**: 목표 각도 (`theta`)
- **Result**: 실제 회전한 각도 (`delta`)
- **Feedback**: 남은 각도 (`remaining`)

## 2. Action Client 작성

turtlesim의 내장 액션 서버에 요청을 보내는 Client를 먼저 만든다.

```bash
cat << 'PYEOF' > ~/ros2_ws/src/my_first_pkg/my_first_pkg/rotate_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from turtlesim.action import RotateAbsolute
import math


class RotateClient(Node):
    def __init__(self):
        super().__init__('rotate_client')
        self._client = ActionClient(
            self, RotateAbsolute, '/turtle1/rotate_absolute'
        )

    def send_goal(self, angle_deg):
        goal_msg = RotateAbsolute.Goal()
        goal_msg.theta = math.radians(angle_deg)

        self.get_logger().info(f'Sending goal: {angle_deg} degrees')
        self._client.wait_for_server()

        self._send_goal_future = self._client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f'Result: rotated {math.degrees(result.delta):.1f} degrees'
        )
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        remaining = feedback_msg.feedback.remaining
        self.get_logger().info(
            f'Feedback: {math.degrees(remaining):.1f} degrees remaining'
        )


def main(args=None):
    rclpy.init(args=args)
    node = RotateClient()
    node.send_goal(90.0)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
PYEOF
```

### 코드 해설

| 코드 | 설명 |
|------|------|
| `ActionClient(self, 타입, 이름)` | 액션 클라이언트 생성 |
| `send_goal_async(goal, feedback_callback)` | 비동기로 Goal 전송 + 피드백 콜백 등록 |
| `goal_response_callback` | Goal 수락/거절 확인 |
| `get_result_async()` | 최종 결과 요청 |
| `feedback_callback` | 진행 상황 수신 (반복 호출) |

액션의 흐름을 정리하면:

1. `send_goal_async` → Goal 전송
2. `goal_response_callback` → 수락 확인
3. `feedback_callback` → 진행 상황 수신 (여러 번)
4. `get_result_callback` → 최종 결과 수신

## 3. Action Server 작성

이번에는 직접 Server를 만든다. 카운트다운을 수행하는 커스텀 서버를 구현하되,
별도 액션 타입 정의 없이 `example_interfaces`를 활용한다.

여기서는 turtlesim의 RotateAbsolute 서버가 이미 존재하므로,
Server 구현의 패턴을 보여주기 위해 **별도 이름으로 동일 타입의 서버**를 만든다.

```bash
cat << 'PYEOF' > ~/ros2_ws/src/my_first_pkg/my_first_pkg/rotate_server.py
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from turtlesim.action import RotateAbsolute
import time
import math


class RotateServer(Node):
    def __init__(self):
        super().__init__('rotate_server')
        self._action_server = ActionServer(
            self,
            RotateAbsolute,
            'my_rotate',
            self.execute_callback
        )
        self.get_logger().info('Rotate Server ready on /my_rotate')

    def execute_callback(self, goal_handle):
        self.get_logger().info(
            f'Goal received: {math.degrees(goal_handle.request.theta):.1f} deg'
        )

        feedback_msg = RotateAbsolute.Feedback()
        target = goal_handle.request.theta
        current = 0.0
        step = target / 10.0  # 10단계로 나눠서 실행

        for i in range(10):
            current += step
            feedback_msg.remaining = target - current
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(
                f'Feedback: {math.degrees(feedback_msg.remaining):.1f} deg remaining'
            )
            time.sleep(0.5)

        goal_handle.succeed()

        result = RotateAbsolute.Result()
        result.delta = target
        return result


def main(args=None):
    rclpy.init(args=args)
    node = RotateServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

### Server 핵심 패턴

| 코드 | 설명 |
|------|------|
| `ActionServer(self, 타입, 이름, 콜백)` | 액션 서버 생성 |
| `goal_handle.publish_feedback(feedback)` | 피드백 전송 |
| `goal_handle.succeed()` | 성공 상태로 마무리 |
| `return result` | 최종 결과 반환 |

서비스 Server와 비교하면:

| 서비스 Server | 액션 Server |
|---------------|-------------|
| `return response` (즉시) | 반복문 안에서 `publish_feedback` 후 `return result` |
| 단발성 | 장시간 실행 |
| 진행 보고 없음 | 피드백 제공 |

## 4. entry_points 등록 및 실행

`setup.py`에 추가:

```python
'rotate_client = my_first_pkg.rotate_client:main',
'rotate_server = my_first_pkg.rotate_server:main',
```

빌드:

```bash
cd ~/ros2_ws
colcon build --packages-select my_first_pkg --symlink-install
source install/setup.bash
```

### turtlesim 내장 서버와 연동

터미널 1:
```bash
ros2 run turtlesim turtlesim_node
```

터미널 2:
```bash
ros2 run my_first_pkg rotate_client
```

터틀이 90도 회전하면서 피드백이 출력된다.

### 직접 만든 서버 테스트

터미널 1:
```bash
ros2 run my_first_pkg rotate_server
```

터미널 2 (CLI로 테스트):
```bash
ros2 action send_goal /my_rotate turtlesim/action/RotateAbsolute "{theta: 1.57}" --feedback
```

0.5초 간격으로 피드백이 출력된 후 최종 결과가 표시된다.

## 5. Goal 취소

액션의 큰 장점 중 하나가 **Goal 취소**다. Client에서 `goal_handle.cancel_goal_async()`를 호출하면 Server에서 작업을 중단할 수 있다.

실무에서 이 기능은 중요하다. 로봇이 목표 지점으로 이동 중일 때 "멈춰!"라고 명령하는 것과 같다. 서비스에는 이런 기능이 없다.

## 정리

| 개념 | 설명 |
|------|------|
| `ActionServer(노드, 타입, 이름, 콜백)` | 액션 서버 생성 |
| `ActionClient(노드, 타입, 이름)` | 액션 클라이언트 생성 |
| `send_goal_async(goal, feedback_callback)` | Goal 전송 |
| `goal_handle.publish_feedback()` | 피드백 발행 |
| `goal_handle.succeed()` | 성공 완료 |

## 핵심 포인트

- 액션은 **Goal → Feedback(반복) → Result** 3단계로 동작한다
- Server는 `execute_callback`에서 작업을 수행하며 피드백을 보낸다
- Client는 Goal 전송 후 콜백 체인으로 응답/피드백/결과를 받는다
- `cancel_goal_async`로 진행 중인 작업을 취소할 수 있다
- 장시간 작업이나 진행 보고가 필요한 경우 서비스 대신 액션을 사용하라

> **다음 튜토리얼**: [015. 커스텀 인터페이스 정의](015_custom_interface.md)에서 나만의 메시지/서비스/액션 타입을 만든다.
