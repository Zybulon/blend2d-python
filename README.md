# Blend2D Python Bindings (nanobind version)

Python bindings for the [Blend2D](https://blend2d.com/) rendering engine using nanobind.

## Overview

This project has been converted from the original Cython-based implementation to use nanobind, which offers:

- Improved performance
- Better compatibility with modern C++
- Simplified binding code
- Cleaner implementation

## Requirements

- C++17 compatible compiler
- CMake 3.15 or newer
- Python 3.8 or newer
- NumPy

## Installation

### From PyPI

Pre-built wheels are available for:
- Windows (x86_64)
- macOS (x86_64, arm64/Apple Silicon)
- Linux (x86_64, aarch64/ARM64)
- WebAssembly (via Emscripten)

```bash
pip install blend2d-python
```

### From Source

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

## Usage

```python
import numpy as np
from blend2d import Context, Image, Gradient, Path, Format

# Create an image
img = Image(480, 480, Format.PRGB32)

# Attach a rendering context to it
ctx = Context(img)

# Clear the image with white color
ctx.fill_all((1.0, 1.0, 1.0, 1.0))

# Create a linear gradient
gradient = Gradient.create_linear(0, 0, 480, 480)
gradient.add_stop(0.0, (1.0, 0.0, 0.0, 1.0))
gradient.add_stop(0.5, (0.0, 1.0, 0.0, 1.0))
gradient.add_stop(1.0, (0.0, 0.0, 1.0, 1.0))

# Create a path (a star, for example)
path = Path()
path.move_to(240, 80)
for i in range(5):
    angle = (i * 2.0 * np.pi / 5.0) + np.pi / 2.0
    path.line_to(240 + 160 * np.cos(angle), 240 + 160 * np.sin(angle))

# Fill the path with the gradient
ctx.set_fill_style(gradient)
ctx.fill_path(path)

# Save the image to a file
img.write_to_file("star.png")
```

## Building Wheels

This project uses [cibuildwheel](https://cibuildwheel.readthedocs.io/) to build wheels for multiple platforms:

- Windows (x86_64)
- macOS (x86_64, arm64/Apple Silicon)
- Linux (x86_64, aarch64/ARM64)
- WebAssembly (via Emscripten)

To build wheels locally:

```bash
pip install cibuildwheel
python -m cibuildwheel --platform auto
```

## License

MIT License

## Acknowledgements

This project was originally created by John Wiggins using Cython, and has been converted to use nanobind.
