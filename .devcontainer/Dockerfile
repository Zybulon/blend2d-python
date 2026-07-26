FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    pkg-config \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create the vscode user
RUN apt-get update \
    && apt-get install -y sudo \
    && echo ubuntu ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu \
    && rm -rf /var/lib/apt/lists/*

# Set up Blend2D dependencies
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links for python -> python3
RUN ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip

# Create venv
RUN python3 -m venv /opt/venv

# Activate venv
ENV PATH="/opt/venv/bin:$PATH"

# Make permissions for venv
RUN chown -R ubuntu:ubuntu /opt/venv




