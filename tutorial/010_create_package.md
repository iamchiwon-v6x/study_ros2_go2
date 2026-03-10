# 010. 패키지 만들기

1부에서는 이미 만들어진 패키지(`turtlesim`)를 CLI로 사용했다.
이제 **직접 패키지를 만들어** Python 코드를 작성하고 실행하는 법을 배운다.

## 패키지란?

ROS 2에서 **패키지(package)**는 코드를 조직하는 기본 단위다.
하나의 패키지 안에 여러 노드, 메시지 정의, launch 파일 등을 담을 수 있다.

패키지를 만들면 다음과 같은 이점이 있다:

- **빌드 시스템**: `colcon build` 한 번으로 의존성 해결과 설치가 된다
- **재사용**: 다른 프로젝트에서 패키지를 가져다 쓸 수 있다
- **배포**: 패키지 단위로 공유하고 설치할 수 있다

## 워크스페이스 구조

ROS 2는 **워크스페이스(workspace)**라는 디렉토리 안에서 패키지를 관리한다.

```
/workspaces/ros2_go2/ros2_ws/              ← 워크스페이스 루트
├── src/                ← 소스 코드 (패키지들이 여기에 위치)
│   └── my_package/     ← 내가 만든 패키지
├── build/              ← 빌드 결과물 (자동 생성)
├── install/            ← 설치된 패키지 (자동 생성)
└── log/                ← 빌드 로그 (자동 생성)
```

개발자가 직접 다루는 곳은 `src/` 뿐이다. 나머지는 `colcon build`가 자동으로 생성한다.

## 1. 워크스페이스 만들기

```bash
mkdir -p /workspaces/ros2_go2/ros2_ws/src
cd /workspaces/ros2_go2/ros2_ws/src
```

## 2. 패키지 생성

`ros2 pkg create` 명령으로 패키지를 생성한다.

```bash
ros2 pkg create --build-type ament_python my_first_pkg --dependencies rclpy std_msgs
```

각 옵션의 의미:

| 옵션 | 설명 |
|------|------|
| `--build-type ament_python` | Python 패키지로 생성 (C++은 `ament_cmake`) |
| `my_first_pkg` | 패키지 이름 (소문자 + 밑줄) |
| `--dependencies rclpy std_msgs` | 의존하는 패키지 목록 |

실행하면 다음과 같은 구조가 만들어진다:

```
my_first_pkg/
├── my_first_pkg/       ← Python 모듈 디렉토리
│   └── __init__.py
├── test/               ← 테스트 파일
├── package.xml         ← 패키지 메타데이터
├── setup.py            ← Python 빌드 설정
├── setup.cfg           ← 설치 경로 설정
└── resource/
    └── my_first_pkg    ← ament index 마커 파일
```

## 3. 핵심 파일 이해하기

### package.xml — 패키지 신분증

패키지의 이름, 버전, 의존성 등을 선언한다. `apt`로 시스템 패키지를 관리하듯, ROS 2는 이 파일로 패키지 의존성을 관리한다.

```bash
cat my_first_pkg/package.xml
```

주요 태그:

| 태그 | 역할 |
|------|------|
| `<name>` | 패키지 이름 |
| `<version>` | 버전 번호 |
| `<depend>` | 빌드 + 실행 시 의존성 |
| `<exec_depend>` | 실행 시에만 필요한 의존성 |
| `<build_type>` | 빌드 시스템 (ament_python) |

### setup.py — Python 빌드 설정

Python 패키지의 빌드와 설치를 정의한다.
**노드를 추가할 때 반드시 이 파일의 `entry_points`를 수정해야 한다.**

```python
entry_points={
    'console_scripts': [
        'my_node = my_first_pkg.my_node:main',
    ],
},
```

형식은 `실행이름 = 패키지명.모듈명:함수명`이다. 이 설정이 있어야 `ros2 run`으로 노드를 실행할 수 있다.

### setup.cfg — 설치 경로

```ini
[develop]
script_dir=$base/lib/my_first_pkg
[install]
install_scripts=$base/lib/my_first_pkg
```

이 파일은 보통 수정할 필요가 없다. 실행 파일이 설치되는 경로를 지정한다.

## 4. 간단한 노드 작성

Python 모듈 디렉토리에 노드 파일을 만든다.

```python
# my_first_pkg/my_first_pkg/hello_node.py
import rclpy
from rclpy.node import Node


class HelloNode(Node):
    def __init__(self):
        super().__init__('hello_node')
        self.get_logger().info('Hello, ROS 2!')


def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

코드의 핵심 구조:

| 부분 | 역할 |
|------|------|
| `rclpy.init()` | ROS 2 통신 시스템 초기화 |
| `Node` 상속 | ROS 2 노드의 기본 기능 사용 |
| `super().__init__('hello_node')` | 노드 이름 등록 |
| `rclpy.spin(node)` | 콜백 대기 루프 (Ctrl+C까지 실행) |
| `rclpy.shutdown()` | 정리 및 종료 |

## 5. entry_points 등록

`setup.py`의 `entry_points`에 노드를 등록한다.

```python
entry_points={
    'console_scripts': [
        'hello = my_first_pkg.hello_node:main',
    ],
},
```

`hello`가 실행 이름이 되어 `ros2 run my_first_pkg hello`로 실행할 수 있다.

## 6. 빌드와 실행

### 6-1. 빌드

워크스페이스 루트에서 빌드한다.

```bash
cd /workspaces/ros2_go2/ros2_ws
colcon build
```

특정 패키지만 빌드하려면:

```bash
colcon build --packages-select my_first_pkg
```

### 6-2. 환경 설정 (source)

빌드 후 새로 설치된 패키지를 인식시킨다.

```bash
source install/setup.bash
```

> **중요**: 빌드 후 반드시 `source`를 해야 한다. 새 터미널을 열 때마다 필요하다.

### 6-3. 실행

```bash
ros2 run my_first_pkg hello
```

```
[INFO] [hello_node]: Hello, ROS 2!
```

## 7. symlink-install로 개발 편의 높이기

매번 코드를 수정할 때마다 `colcon build`를 다시 해야 하면 번거롭다.
`--symlink-install` 옵션을 사용하면 Python 파일을 심볼릭 링크로 설치하여 **코드 수정 즉시 반영**된다.

```bash
colcon build --packages-select my_first_pkg --symlink-install
```

이 옵션을 사용하면 `src/` 안의 Python 파일을 수정하면 별도 빌드 없이 바로 실행에 반영된다.
단, `setup.py`의 `entry_points`를 변경했거나 새 파일을 추가했을 때는 다시 빌드해야 한다.

## 8. 패키지 정보 확인

빌드가 끝난 후 패키지 정보를 확인할 수 있다.

```bash
ros2 pkg list | grep my_first
```

```
my_first_pkg
```

```bash
ros2 pkg prefix my_first_pkg
```

```
/home/vscode/ros2_ws/install/my_first_pkg
```

## 정리

| 명령 | 역할 |
|------|------|
| `ros2 pkg create --build-type ament_python` | Python 패키지 생성 |
| `colcon build` | 워크스페이스 빌드 |
| `colcon build --packages-select <pkg>` | 특정 패키지만 빌드 |
| `colcon build --symlink-install` | 심볼릭 링크 설치 (Python 코드 즉시 반영) |
| `source install/setup.bash` | 빌드 결과 환경 적용 |

## 핵심 포인트

- 패키지는 ROS 2 코드의 기본 단위다
- `package.xml`은 의존성, `setup.py`의 `entry_points`는 실행 가능 노드를 정의한다
- **빌드 → source → 실행** 3단계가 기본 워크플로우다
- `--symlink-install`로 Python 개발 시 빌드 반복을 줄일 수 있다

> **다음 튜토리얼**: [011. 토픽 Publisher 작성](011_topic_publisher.md)에서 직접 토픽을 발행하는 노드를 만든다.
