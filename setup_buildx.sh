#!/bin/bash
# setup_buildx.sh - Script to set up Docker buildx for cross-compilation

# Make sure we exit on any error
set -e

echo "Setting up Docker buildx for cross-compilation..."

# Install prerequisites
echo "Installing Docker and QEMU..."
apt-get update
apt-get install -y qemu-user-static binfmt-support

# Set up QEMU to handle binaries for different architectures
echo "Setting up QEMU binary formats..."
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# Create a new buildx builder instance with multi-architecture support
echo "Creating buildx builder with multi-architecture support..."
docker buildx create --name multiarch-builder --driver docker-container --use

# Inspect the builder to verify it's set up properly
echo "Inspecting and bootstrapping the builder..."
docker buildx inspect --bootstrap

# Print supported platforms
echo "Supported platforms:"
docker buildx inspect --bootstrap | grep "Platforms"

echo "Docker buildx setup complete!"