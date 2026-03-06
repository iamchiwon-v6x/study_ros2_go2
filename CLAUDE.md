# Project Rules — ROS 2 + Unitree Go2 Tutorial

## 프로젝트 개요

ROS 2 Humble 학습 및 Unitree Go2 제어를 위한 튜토리얼 프로젝트.
devcontainer 환경에서 실행되며, noVNC를 통해 GUI를 제공한다.

## 튜토리얼 작성 규칙

### 문서 구조
- 튜토리얼 파일은 `tutorial/` 디렉토리에 `NNN_제목.md` 형식으로 저장한다
- 각 튜토리얼은 실습 내용뿐 아니라 **개념 설명**을 포함해야 한다
- 튜토리얼만으로도 독립적으로 학습할 수 있도록 충분한 배경 지식을 제공한다
- 새 튜토리얼 추가 시 `README.md`의 커리큘럼 표도 함께 업데이트한다

### 다이어그램 / 이미지 규칙

**원칙: 다이어그램이 필요할 때 Excalidraw로 그리고 export 해서 문서에 반영한다.**

1. **Excalidraw MCP** (`https://mcp.excalidraw.com`)를 사용하여 다이어그램을 생성한다
2. Excalidraw MCP를 사용할 수 없는 환경에서는 **matplotlib**로 다이어그램을 생성한다
3. 이미지 파일은 `tutorial/images/` 디렉토리에 저장한다
4. 파일명은 `NNN_설명.png` 형식을 따른다 (예: `001_pubsub.png`)
5. 마크다운 문서에서 이미지를 참조할 때는 상대 경로를 사용한다:
   ```markdown
   ![Pub/Sub 구조도](images/001_pubsub.png)
   ```
6. ASCII 아트 다이어그램은 사용하지 않는다 — 렌더링이 깨지기 쉽다
7. **이미지 크기 제한**: 문서에 삽입했을 때 과도하게 크지 않아야 한다
   - matplotlib: `figsize`는 가로 5~6, 세로 1.5~3 이내로 제한한다
   - DPI는 120 이하로 설정한다
   - 박스, 폰트, 여백을 컴팩트하게 유지한다

### 코드 블록 규칙
- 모든 명령어는 `bash` 코드 블록으로 감싼다
- 명령어의 출력 예시는 별도 코드 블록(언어 지정 없음)으로 표시한다
- 패키지명, 노드명, 토픽명은 인라인 코드(`` ` ``)로 표시한다

## 커리큘럼 구성

| 파트 | 범위 | 내용 |
|------|------|------|
| 1부 | 001–009 | ROS 2 기본 개념 (CLI로 익히기) |
| 2부 | 010–017 | Python으로 ROS 2 프로그래밍 |
| 3부 | 018–027 | Unitree Go2 시뮬레이션과 제어 |

## 기술 환경

- **ROS Distro**: Humble Hawksbill (Ubuntu 22.04, LTS)
- **시뮬레이터**: unitree_mujoco (CycloneDDS 기반)
- **ROS 2 브릿지**: unitree_ros2 (시뮬레이터/실기기 공용)
- **GUI**: noVNC (브라우저에서 `http://localhost:6080`, 비밀번호: `vscode`)

## Go2 관련 참고

- Unitree Go2는 ROS 2 토픽을 직접 사용하지 않고 **CycloneDDS**를 통해 `unitree_sdk2`로 통신한다
- `unitree_ros2` 브릿지를 통해 SDK의 DDS 토픽을 ROS 2 토픽으로 변환한다
- 시뮬레이터(unitree_mujoco)와 실기기가 **동일한 통신 레이어**를 사용하므로, 시뮬레이터용 코드가 실기기에서도 그대로 동작한다
