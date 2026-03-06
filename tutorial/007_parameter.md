# 007. 파라미터 다루기

노드를 실행한 후에 동작을 바꾸고 싶다면? 코드를 수정하고 재빌드하는 것은 번거롭다.
**파라미터(Parameter)**를 사용하면 노드를 **재시작하지 않고도** 설정을 변경할 수 있다.

## 파라미터란?

파라미터는 노드의 **설정값**이다. 각 노드는 자신만의 파라미터를 가질 수 있고,
실행 중에 외부에서 읽거나 변경할 수 있다.

실제 로봇에서의 파라미터 예시:

| 파라미터 | 용도 |
|----------|------|
| `max_speed` | 최대 이동 속도 제한 |
| `camera_fps` | 카메라 촬영 속도 |
| `obstacle_threshold` | 장애물 감지 거리 |
| `use_sim_time` | 시뮬레이션 시간 사용 여부 |

파라미터는 **토픽/서비스/액션과 별개의 메커니즘**이다.
통신이 아니라 노드 내부의 설정을 관리하는 도구다.

## 사전 조건

- turtlesim 노드와 teleop 노드가 실행 중

## 1. 파라미터 목록 확인

```bash
ros2 param list /turtlesim
```

```
  background_b
  background_g
  background_r
  qos_overrides./parameter_events.publisher.depth
  qos_overrides./parameter_events.publisher.durability
  qos_overrides./parameter_events.publisher.history
  qos_overrides./parameter_events.publisher.reliability
  use_sim_time
```

turtlesim의 주요 파라미터:
- `background_r`, `background_g`, `background_b` — 배경 색상 (RGB)
- `use_sim_time` — 시뮬레이션 시간 사용 여부

## 2. 파라미터 값 읽기

```bash
ros2 param get /turtlesim background_r
```

```
Integer value is: 69
```

현재 배경의 R(빨간) 값이 69인 것을 확인할 수 있다.

나머지 색상도 확인해보자:

```bash
ros2 param get /turtlesim background_g
ros2 param get /turtlesim background_b
```

기본값은 R=69, G=86, B=255로 파란색 배경이다.

## 3. 파라미터 값 변경

배경색을 변경해보자:

```bash
ros2 param set /turtlesim background_r 255
```

```
Set parameter successful
```

noVNC에서 배경이 보라색으로 바뀐 것을 확인한다 (R=255, G=86, B=255).

다른 색상도 변경해보자:

```bash
# 빨간 배경
ros2 param set /turtlesim background_g 0
ros2 param set /turtlesim background_b 0
```

```bash
# 초록 배경
ros2 param set /turtlesim background_r 0
ros2 param set /turtlesim background_g 255
ros2 param set /turtlesim background_b 0
```

노드를 재시작하지 않고도 실시간으로 동작이 바뀌는 것이 파라미터의 핵심이다.

## 4. 모든 파라미터 한번에 보기

```bash
ros2 param dump /turtlesim
```

```
/turtlesim:
  ros__parameters:
    background_b: 0
    background_g: 255
    background_r: 0
    use_sim_time: false
```

현재 설정된 모든 파라미터 값을 YAML 형식으로 출력한다.
이 출력을 파일로 저장하면 나중에 동일한 설정으로 노드를 실행할 수 있다.

```bash
ros2 param dump /turtlesim --output-dir .
```

현재 디렉토리에 `turtlesim.yaml` 파일이 생성된다.

## 5. 파라미터 파일로 노드 실행

저장한 파라미터 파일을 사용해 노드를 시작할 수 있다:

```bash
ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim.yaml
```

이렇게 하면 노드가 시작될 때 파일의 설정값이 자동으로 적용된다.
로봇 시스템에서는 이 방식으로 **재현 가능한 설정**을 관리한다.

## 6. 파라미터 설명 확인

```bash
ros2 param describe /turtlesim background_r
```

```
Parameter name: background_r
  Type: integer
  Description: Red channel of the background color
  Constraints:
    Min value: 0
    Max value: 255
```

파라미터의 타입, 설명, 제약 조건을 확인할 수 있다.
새로운 노드를 처음 접할 때 어떤 파라미터가 있고 무엇을 의미하는지 파악하는 데 유용하다.

## 정리

| 명령어 | 역할 |
|--------|------|
| `ros2 param list <노드>` | 파라미터 목록 |
| `ros2 param get <노드> <파라미터>` | 파라미터 값 읽기 |
| `ros2 param set <노드> <파라미터> <값>` | 파라미터 값 변경 |
| `ros2 param dump <노드>` | 모든 파라미터 YAML 출력 |
| `ros2 param describe <노드> <파라미터>` | 파라미터 설명 확인 |
| `--ros-args --params-file <파일>` | 파라미터 파일로 노드 실행 |

**이 튜토리얼에서 배운 것:**

- 파라미터는 노드를 재시작하지 않고 설정을 변경하는 메커니즘이다
- `param dump`로 설정을 저장하고 `--params-file`로 재사용할 수 있다
- 실제 로봇에서는 속도 제한, 센서 설정 등을 파라미터로 관리한다

다음 튜토리얼에서는 ROS 2의 GUI 도구 **RQt**를 배운다.
