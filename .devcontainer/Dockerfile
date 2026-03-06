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

# noVNC 시작 스크립트
RUN echo '#!/bin/bash\n\
Xvfb :1 -screen 0 1280x720x24 &\n\
sleep 1\n\
x11vnc -display :1 -forever -nopw -quiet &\n\
websockify --web /usr/share/novnc 6080 localhost:5900 &\n\
echo "noVNC ready: http://localhost:6080/vnc.html"' \
    > /usr/local/bin/start-vnc.sh && chmod +x /usr/local/bin/start-vnc.sh

ENV DISPLAY=:1

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
