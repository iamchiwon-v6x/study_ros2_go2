# 008. RQt 도구 활용

지금까지 모든 작업을 CLI로 했다. ROS 2는 **RQt**라는 GUI 도구 모음을 제공한다.
시각적으로 시스템을 모니터링하고 디버깅할 수 있어서, CLI와 함께 사용하면 효율이 올라간다.

## RQt란?

RQt는 **Qt 기반의 GUI 프레임워크**로, 플러그인 형태의 다양한 도구를 포함한다.
각 플러그인은 독립적으로 사용할 수 있고, 하나의 창에서 여러 플러그인을 조합할 수도 있다.

주요 플러그인:

| 플러그인 | 역할 |
|----------|------|
| `rqt_graph` | 노드-토픽 연결 관계 시각화 |
| `rqt_topic` | 토픽 데이터 실시간 모니터링 |
| `rqt_service_caller` | GUI에서 서비스 호출 |
| `rqt_console` | 로그 메시지 확인 |
| `rqt_plot` | 토픽 데이터 그래프 |
| `rqt_reconfigure` | 파라미터 실시간 조정 |

## 사전 조건

- turtlesim 노드와 teleop 노드가 실행 중
- 브라우저에서 noVNC(`http://localhost:6080`)에 접속된 상태

## 1. rqt_graph — 시스템 구조 시각화

```bash
ros2 run rqt_graph rqt_graph
```

noVNC 화면에 노드와 토픽의 연결 그래프가 표시된다.

확인할 수 있는 정보:
- 어떤 노드가 존재하는지
- 노드 간에 어떤 토픽으로 연결되어 있는지
- 데이터 흐름의 방향

시스템이 복잡해질수록 rqt_graph의 가치가 커진다.
"메시지가 안 오는데 어디가 문제지?" 같은 상황에서 연결이 제대로 되어 있는지 한눈에 확인할 수 있다.

상단의 드롭다운에서 **Nodes/Topics (all)** 을 선택하면 숨겨진 토픽까지 모두 볼 수 있다.

## 2. rqt_topic — 토픽 모니터링

```bash
rqt
```

RQt 메인 창이 열린다. 메뉴에서:

**Plugins → Topics → Topic Monitor**

토픽 목록이 나타나고, 체크박스를 클릭하면 해당 토픽의 데이터가 실시간으로 표시된다.

`/turtle1/pose`를 체크해보자. x, y, theta 값이 실시간으로 갱신되는 것을 볼 수 있다.
teleop으로 거북이를 움직이면 값이 변하는 것을 확인하자.

CLI의 `ros2 topic echo`와 같은 역할이지만, 여러 토픽을 동시에 모니터링할 수 있어 편리하다.

## 3. rqt_plot — 데이터 그래프

터미널에서:

```bash
ros2 run rqt_plot rqt_plot
```

상단 입력창에 다음을 입력하고 `+` 버튼을 클릭:

```
/turtle1/pose/x
```

같은 방식으로 `/turtle1/pose/y`도 추가하자.

teleop으로 거북이를 움직이면, x와 y 좌표가 **시간에 따른 그래프**로 표시된다.
센서 데이터의 변화 추이를 파악하거나, 제어 명령에 대한 응답을 분석할 때 유용하다.

## 4. rqt_service_caller — GUI로 서비스 호출

RQt 메인 창에서:

**Plugins → Services → Service Caller**

서비스 드롭다운에서 `/turtle1/teleport_absolute`를 선택한다.
x, y, theta 값을 입력하고 **Call** 버튼을 클릭하면 거북이가 순간이동한다.

CLI의 `ros2 service call`과 같은 기능이지만, 인터페이스 구조를 외울 필요 없이
GUI에서 바로 값을 입력할 수 있어 편리하다.

## 5. rqt_reconfigure — 파라미터 실시간 조정

```bash
ros2 run rqt_reconfigure rqt_reconfigure
```

왼쪽 패널에서 `/turtlesim`을 클릭하면 파라미터가 슬라이더로 표시된다.

`background_r`, `background_g`, `background_b` 슬라이더를 움직여보자.
noVNC에서 배경색이 실시간으로 바뀌는 것을 확인할 수 있다.

007에서 CLI로 하나씩 변경했던 것을 여기서는 슬라이더로 직관적으로 조정할 수 있다.
파라미터 튜닝 — 예를 들어 PID 게인 조정 같은 작업 — 에서 특히 유용하다.

## 6. rqt_console — 로그 확인

```bash
ros2 run rqt_console rqt_console
```

노드가 출력하는 로그 메시지(DEBUG, INFO, WARN, ERROR, FATAL)를 GUI로 확인한다.
심각도별 필터링이 가능해서, 에러 메시지만 골라보기 편리하다.

## CLI와 RQt, 언제 무엇을 쓰나?

| 상황 | 추천 도구 |
|------|----------|
| 빠른 확인, 스크립트 자동화 | CLI |
| 여러 값을 동시에 모니터링 | RQt Topic Monitor |
| 데이터 추이 분석 | rqt_plot |
| 시스템 구조 파악 | rqt_graph |
| 파라미터 튜닝 | rqt_reconfigure |
| 디버깅, 로그 분석 | rqt_console |

둘은 대립 관계가 아니다. CLI로 빠르게 확인하고, RQt로 깊이 분석하는 것이 일반적인 워크플로우다.

## 정리

| 명령어 | 역할 |
|--------|------|
| `rqt` | RQt 메인 창 (플러그인 선택) |
| `ros2 run rqt_graph rqt_graph` | 노드-토픽 그래프 |
| `ros2 run rqt_plot rqt_plot` | 토픽 데이터 그래프 |
| `ros2 run rqt_reconfigure rqt_reconfigure` | 파라미터 GUI 조정 |
| `ros2 run rqt_console rqt_console` | 로그 메시지 확인 |

**이 튜토리얼에서 배운 것:**

- RQt는 ROS 2의 GUI 도구 모음으로, 다양한 플러그인을 제공한다
- rqt_graph로 시스템 구조를, rqt_plot으로 데이터 추이를 확인할 수 있다
- CLI와 RQt를 상황에 맞게 조합하면 디버깅과 모니터링 효율이 높아진다

다음 튜토리얼에서는 토픽 데이터를 **파일로 녹화하고 재생**하는 방법을 배운다.
