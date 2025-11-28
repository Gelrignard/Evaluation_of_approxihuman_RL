FROM ros:noetic-ros-base

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies + ROS packages
RUN apt-get update --fix-missing && \
    apt-get install -y \
    python3-dev \
    python3-pip \
    nano \
    git \
    unzip \
    build-essential \
    autoconf \
    libtool \
    cmake \
    vim \
    xvfb \
    ffmpeg \
    libeigen3-dev \
    ros-noetic-tf2 \
    ros-noetic-tf2-ros \
    ros-noetic-ackermann-msgs \
    ros-noetic-map-server \
    ros-noetic-rviz \
    ros-noetic-xacro \
    ros-noetic-robot-state-publisher \
    ros-noetic-nav-msgs \
    ros-noetic-geometry-msgs \
    ros-noetic-std-msgs \
    ros-noetic-sensor-msgs \
    && rm -rf /var/lib/apt/lists/*

# Source ROS in bashrc
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Upgrade pip but keep it below 24.1 for gym==0.21.0 compatibility
RUN pip3 install --upgrade "pip<24.1"

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
# Force reinstall PyYAML to override the system-installed distutils version
RUN pip3 install --ignore-installed PyYAML==6.0
RUN pip3 install -r /tmp/requirements.txt

# Set working directory
WORKDIR /workspace

# Copy the project
COPY . /workspace

# Install the gym package in editable mode
RUN cd /workspace/Gym && pip3 install -e gym/

ENTRYPOINT ["/bin/bash"]