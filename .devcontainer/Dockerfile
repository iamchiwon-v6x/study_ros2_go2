FROM osrf/ros:foxy-desktop

# ============================================================
# Go2 Jetson 실기기와 동일한 환경 구성
# - ROS 2 Foxy (Ubuntu 20.04) — Go2 Jetson: Ubuntu 20.04 + Foxy
# - CycloneDDS — Go2 통신 레이어
# - Python 3.8 — Go2 Jetson 기본 Python
# ============================================================

# 기본 도구
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    vim \
    tmux \
    # turtlesim (학습용)
    ros-foxy-turtlesim \
    # CycloneDDS — Go2가 사용하는 DDS 미들웨어
    ros-foxy-rmw-cyclonedds-cpp \
    # Go2 실기기에 설치된 SLAM 관련 패키지
    ros-foxy-nav2-map-server \
    ros-foxy-tf2-tools \
    # SLAM 패키지 (실기기에서도 설치 예정)
    ros-foxy-slam-toolbox \
    ros-foxy-pointcloud-to-laserscan \
    && rm -rf /var/lib/apt/lists/*

# CycloneDDS 설정 파일 복사
COPY cyclonedds.xml /etc/cyclonedds/cyclonedds.xml

# 환경 변수: Go2와 동일하게 CycloneDDS 사용
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV CYCLONEDDS_URI=file:///etc/cyclonedds/cyclonedds.xml

# bashrc 설정
RUN echo "source /opt/ros/foxy/setup.bash" >> /root/.bashrc && \
    echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /root/.bashrc && \
    echo "export CYCLONEDDS_URI=file:///etc/cyclonedds/cyclonedds.xml" >> /root/.bashrc
