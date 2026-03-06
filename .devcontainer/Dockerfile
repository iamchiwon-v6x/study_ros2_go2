FROM osrf/ros:humble-desktop

# 기본 도구 + GUI(noVNC) + turtlesim
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    vim \
    # noVNC: 브라우저에서 GUI 확인
    xvfb \
    x11vnc \
    novnc \
    websockify \
    # turtlesim
    ros-humble-turtlesim \
    && rm -rf /var/lib/apt/lists/*

# index.html → vnc.html 심링크
RUN ln -sf /usr/share/novnc/vnc.html /usr/share/novnc/index.html

# noVNC 시작 스크립트
COPY start-vnc.sh /usr/local/bin/start-vnc.sh
RUN chmod +x /usr/local/bin/start-vnc.sh

ENV DISPLAY=:1

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
