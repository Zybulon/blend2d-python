# macOS Builds Temporarily Disabled

## Status

macOS builds have been **temporarily disabled** until the import issue is resolved.

## Problem

The wheels build successfully on macOS but fail at import:
```
ModuleNotFoundError: No module named 'blend2d._capi'
```

The `_capi.so` file is either:
1. Not being included in the wheel
2. In the wrong location in the wheel
3. Has incorrect permissions/linking

## What Works

✅ **Linux (x86_64, aarch64)** - Fully working
✅ **Windows (AMD64)** - Fully working

## What's Disabled

❌ **macOS (Intel x86_64)** - Disabled
❌ **macOS (Apple Silicon arm64)** - Disabled

## Changes Made

1. **`.github/workflows/build-wheels.yml`**:
   - Removed `macos-13` and `macos-14` from build matrix

2. **`pyproject.toml`**:
   - Added `*-macosx*` to skip patterns

## Current Wheel Support

When published to PyPI, users will be able to install on:
- ✅ Linux x86_64 (Python 3.8-3.12)
- ✅ Linux aarch64/ARM64 (Python 3.8-3.12)
- ✅ Windows AMD64 (Python 3.8-3.12)
- ❌ macOS (all architectures) - source install only

**Total: 10 wheels** (5 Linux x86_64 + 5 Linux aarch64 + 5 Windows)

## For macOS Users

macOS users can still install from source:
```bash
pip install blend2d --no-binary blend2d
```

This will compile from source (requires CMake and a C++ compiler).

## Next Steps to Fix macOS

1. Investigate wheel contents: `unzip -l blend2d-*.whl`
2. Check if `_capi.so` is present
3. Verify it's in `blend2d/` directory
4. Check with `otool -L` for missing dependencies
5. Test locally on macOS with debug build

## Re-enabling macOS

Once fixed:
1. Restore OS list in `.github/workflows/build-wheels.yml`
2. Remove `*-macosx*` from skip in `pyproject.toml`
3. Test with new release candidate tag

---

**Decision: Ship Linux + Windows wheels now, fix macOS later**
