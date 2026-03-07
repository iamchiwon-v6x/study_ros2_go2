# 016. 파라미터 프로그래밍

1부에서 CLI로 파라미터를 다루는 법을 배웠다.
이번에는 **노드 코드 안에서 파라미터를 선언하고, 동적으로 변경에 반응**하는 법을 배운다.

## 파라미터를 코드로 다루는 이유

CLI의 `ros2 param set`은 외부에서 파라미터를 바꿔주는 것이다.
하지만 **노드가 어떤 파라미터를 사용하는지 선언**하고, **값이 바뀌었을 때 어떻게 반응할지** 정하는 것은 노드 코드의 몫이다.

예를 들어:
- 로봇 속도 상한(`max_speed`)을 파라미터로 선언
- 운영 중에 `ros2 param set`으로 속도를 조절
- 노드가 새 값을 즉시 반영

## 사전 조건

- `my_first_pkg` 패키지
- 워크스페이스: `~/ros2_ws`

## 1. 파라미터 선언과 사용

```bash
cat << 'PYEOF' > ~/ros2_ws/src/my_first_pkg/my_first_pkg/param_node.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class ParamTurtle(Node):
    def __init__(self):
        super().__init__('param_turtle')

        # 파라미터 선언 (이름, 기본값)
        self.declare_parameter('speed', 1.0)
        self.declare_parameter('turn_rate', 0.5)
        self.declare_parameter('enable', True)

        self.publisher_ = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        enable = self.get_parameter('enable').value
        if not enable:
            return

        speed = self.get_parameter('speed').value
        turn = self.get_parameter('turn_rate').value

        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = turn
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ParamTurtle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

### 핵심 API

| 메서드 | 설명 |
|--------|------|
| `declare_parameter('name', default)` | 파라미터 선언 + 기본값 설정 |
| `get_parameter('name').value` | 현재 값 읽기 |
| `set_parameters([Parameter('name', value=v)])` | 코드에서 값 변경 |

`declare_parameter`를 호출하지 않은 파라미터는 외부에서 `set`할 수 없다. 이 선언이 **파라미터 스키마** 역할을 한다.

## 2. entry_points 등록 및 실행

`setup.py`에 추가:

```python
'param_turtle = my_first_pkg.param_node:main',
```

빌드 후 실행:

```bash
cd ~/ros2_ws && colcon build --packages-select my_first_pkg --symlink-install
source install/setup.bash
```

터미널 1:
```bash
ros2 run turtlesim turtlesim_node
```

터미널 2:
```bash
ros2 run my_first_pkg param_turtle
```

터틀이 원을 그리며 이동한다. 이제 파라미터를 바꿔보자.

터미널 3:
```bash
# 속도 변경
ros2 param set /param_turtle speed 3.0

# 회전 멈추기
ros2 param set /param_turtle turn_rate 0.0

# 완전 정지
ros2 param set /param_turtle enable false
```

실시간으로 터틀의 움직임이 변하는 것을 확인할 수 있다.

## 3. 파라미터 변경 콜백

위 코드에서는 `get_parameter`를 매번 호출한다. 더 효율적인 방법은 **파라미터가 변경될 때만 콜백**을 받는 것이다.

```bash
cat << 'PYEOF' > ~/ros2_ws/src/my_first_pkg/my_first_pkg/param_callback_node.py
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult


class ParamCallbackNode(Node):
    def __init__(self):
        super().__init__('param_callback_node')
        self.declare_parameter('threshold', 50.0)
        self.declare_parameter('name', 'robot_1')

        self.add_on_set_parameters_callback(self.param_callback)
        self.get_logger().info(
            f'Started with threshold={self.get_parameter("threshold").value}'
        )

    def param_callback(self, params):
        for param in params:
            self.get_logger().info(
                f'Parameter changed: {param.name} = {param.value}'
            )

            # 유효성 검사
            if param.name == 'threshold' and param.value < 0:
                self.get_logger().warn('Threshold must be >= 0, rejecting.')
                return SetParametersResult(successful=False)

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = ParamCallbackNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

### 콜백의 핵심

| 기능 | 설명 |
|------|------|
| `add_on_set_parameters_callback` | 파라미터 변경 시 호출될 콜백 등록 |
| `SetParametersResult(successful=True)` | 변경 수락 |
| `SetParametersResult(successful=False)` | 변경 거부 (값이 바뀌지 않음) |

이 패턴의 장점:
- **유효성 검사**: 잘못된 값을 거부할 수 있다
- **부수 효과**: 파라미터 변경 시 추가 동작을 수행할 수 있다 (예: 하드웨어 재설정)
- **로깅**: 누가 언제 무엇을 바꿨는지 기록할 수 있다

## 4. 실행 시 파라미터 지정

`ros2 run` 실행 시 파라미터 초기값을 지정할 수 있다.

```bash
ros2 run my_first_pkg param_turtle --ros-args -p speed:=2.5 -p turn_rate:=1.0
```

여러 파라미터를 파일로 관리하려면 YAML 파일을 사용한다.

```bash
cat << 'EOF' > ~/ros2_ws/turtle_params.yaml
param_turtle:
  ros__parameters:
    speed: 2.0
    turn_rate: 0.8
    enable: true
EOF
```

```bash
ros2 run my_first_pkg param_turtle --ros-args --params-file ~/ros2_ws/turtle_params.yaml
```

## 5. 파라미터 타입

`declare_parameter`에 전달하는 기본값의 타입으로 파라미터 타입이 결정된다.

| Python 기본값 | ROS 2 타입 | 예시 |
|----------------|------------|------|
| `1.0` | DOUBLE | 소수점 숫자 |
| `1` | INTEGER | 정수 |
| `'hello'` | STRING | 문자열 |
| `True` | BOOL | 참/거짓 |
| `[1.0, 2.0]` | DOUBLE_ARRAY | 숫자 배열 |
| `['a', 'b']` | STRING_ARRAY | 문자열 배열 |

타입이 맞지 않는 값을 `ros2 param set`으로 설정하면 에러가 발생한다.

## 6. 파라미터 디스크립터

파라미터에 설명, 범위 등 메타데이터를 추가할 수 있다.

```python
from rcl_interfaces.msg import ParameterDescriptor, FloatingPointRange

descriptor = ParameterDescriptor(
    description='Maximum speed in m/s',
    floating_point_range=[FloatingPointRange(
        from_value=0.0,
        to_value=10.0,
        step=0.1
    )]
)
self.declare_parameter('max_speed', 1.0, descriptor)
```

이렇게 하면 `ros2 param describe`에서 설명이 표시되고, `rqt_reconfigure`에서 슬라이더 범위가 자동으로 설정된다.

## 정리

| API | 설명 |
|-----|------|
| `declare_parameter(name, default)` | 파라미터 선언 |
| `get_parameter(name).value` | 값 읽기 |
| `add_on_set_parameters_callback(cb)` | 변경 콜백 등록 |
| `--ros-args -p name:=value` | 실행 시 지정 |
| `--ros-args --params-file file.yaml` | YAML로 일괄 지정 |

## 핵심 포인트

- `declare_parameter`로 선언하지 않은 파라미터는 사용할 수 없다
- `get_parameter`로 매 콜백마다 읽거나, `add_on_set_parameters_callback`으로 변경 이벤트를 받을 수 있다
- 콜백에서 `successful=False`를 반환하면 잘못된 값을 거부할 수 있다
- YAML 파일과 `ParameterDescriptor`로 파라미터를 체계적으로 관리하라

> **다음 튜토리얼**: [017. Launch 파일 작성](017_launch_file.md)에서 여러 노드를 한 번에 실행하고 설정하는 법을 배운다.
