#!/bin/bash

# 가상 디스플레이
Xvfb :1 -screen 0 1280x720x24 &
sleep 1

# VNC 서버
x11vnc -display :1 -forever -nopw -quiet &

# noVNC (웹 브라우저 접속)
websockify --web /usr/share/novnc 6080 localhost:5900 &

echo "noVNC ready → http://localhost:6080"
