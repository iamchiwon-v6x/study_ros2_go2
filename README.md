# ROS 2 Humble Dev Environment

ROS 2 Humble 학습 및 개발을 위한 devcontainer 환경.

## 환경 구성

| 항목 | 내용 |
|------|------|
| Base Image | `osrf/ros:humble-desktop` |
| ROS Distro | Humble Hawksbill (Ubuntu 22.04) |
| GUI 접속 | noVNC — 브라우저에서 `http://localhost:6080` |
| 기본 도구 | python3-pip, git, vim |

## 시작하기

1. VS Code에서 이 폴더를 열고 `Reopen in Container` 실행
2. 브라우저에서 http://localhost:6080 접속 → Connect

## 설치된 패키지

| 패키지 | 용도 |
|--------|------|
| ros-humble-desktop | ROS 2 기본 + rviz2, rqt 등 GUI 도구 |
| ros-humble-turtlesim | ROS 2 학습용 시뮬레이터 |
| xvfb, x11vnc, novnc | 브라우저 기반 GUI 표시 (noVNC) |

> 패키지 추가 시 이 표를 업데이트할 것.

## Tutorial

| # | 제목 | 파일 |
|---|------|------|
| 001 | ROS 2 동작 환경 확인하기 | [001_verify_ros2_setup.md](tutorial/001_verify_ros2_setup.md) |
| 002 | Turtlesim으로 ROS 2 체험하기 | [002_turtlesim.md](tutorial/002_turtlesim.md) |
