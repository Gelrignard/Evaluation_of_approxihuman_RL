FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
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
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip but keep it below 24.1 for gym==0.21.0 compatibility
RUN pip3 install --upgrade "pip<24.1"

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Set working directory
WORKDIR /workspace

# Copy the project
COPY . /workspace

# Install the gym package in editable mode
RUN cd /workspace/Gym && pip3 install -e gym/

ENTRYPOINT ["/bin/bash"]