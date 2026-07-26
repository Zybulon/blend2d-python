# Development Container for Blend2D Python

This directory contains configuration files for a development container that provides an isolated, consistent development environment for the Blend2D Python bindings project.

## Features

- Ubuntu 22.04 base image
- Multiple Python versions pre-installed:
  - Python 3.10
  - Python 3.11
  - Python 3.12
- Common development tools:
  - CMake
  - Git
  - Build essentials (compilers, etc.)
- VS Code extensions for Python and C++ development

## Using Different Python Versions

The container has all three Python versions available on the system. You can use them with the following commands:

```bash
# Default Python (3.12)
python --version

# Specific Python versions
python3.10 --version
python3.11 --version
python3.12 --version
```

## Installing Dependencies

The basic requirements for building the project (NumPy, Cython, and pytest) are automatically installed in the default Python environment during container creation.

To install them for a specific Python version:

```bash
python3.10 -m pip install numpy cython pytest
python3.11 -m pip install numpy cython pytest
python3.12 -m pip install numpy cython pytest
```

## Building with Different Python Versions

To build the project with a specific Python version:

```bash
# For Python 3.10
python3.10 setup.py build_ext --inplace

# For Python 3.11
python3.11 setup.py build_ext --inplace

# For Python 3.12
python3.12 setup.py build_ext --inplace
```

## Testing with Different Python Versions

```bash
# For Python 3.10
python3.10 -m pytest

# For Python 3.11
python3.11 -m pytest

# For Python 3.12
python3.12 -m pytest
```

## Starting the Container

If using VS Code:
1. Install the "Remote - Containers" extension
2. Open the command palette (F1 or Ctrl+Shift+P)
3. Select "Remote-Containers: Reopen in Container" 