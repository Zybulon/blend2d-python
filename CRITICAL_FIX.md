# Critical Fix: Reverted src/CMakeLists.txt

## Problem

My previous fix (removing `OUTPUT_NAME "_capi"`) broke Linux and macOS imports:
```
ModuleNotFoundError: No module named 'blend2d._capi'
```

## Root Cause

The `OUTPUT_NAME` setting is REQUIRED. Without it:
- Nanobind uses the full target name (with ABI tags) as the filename
- CMake can't handle dots in target names properly
- The module file doesn't get created/installed correctly

## Solution

**REVERTED** to original code with `OUTPUT_NAME "_capi"`:

```cmake
set_target_properties(${BLEND2DPY_TARGET_NAME} PROPERTIES OUTPUT_NAME "_capi")
```

This produces:
- Linux: `_capi.so` 
- macOS: `_capi.so`
- Windows: `_capi.pyd`

Python can import these without ABI tags in the filename.

## Status

- ✅ Linux: Should work again (was working before)
- ✅ Windows: Should work (was working before)  
- ❓ macOS: Still investigating

## Next Steps

1. Test with current code (reverted)
2. If macOS still fails, investigate:
   - Check if `_capi.so` is in the wheel
   - Check file permissions
   - Check library dependencies with `otool -L`

---

**The original approach was correct for Linux/Windows.**
**macOS issue must be something different - not the OUTPUT_NAME.**
