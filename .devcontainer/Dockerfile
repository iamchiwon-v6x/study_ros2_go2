FROM osrf/ros:humble-desktop

# 기본 도구 + turtlesim
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    vim \
    # turtlesim
    ros-humble-turtlesim \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
