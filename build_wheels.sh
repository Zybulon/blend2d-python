#!/bin/bash
set -e -u -x

# Install dependencies
python -m pip install --upgrade pip
python -m pip install cibuildwheel

# Build the wheels
python -m cibuildwheel --output-dir wheelhouse

# Print contents of wheelhouse directory
ls -l wheelhouse/
