#!/bin/bash
set -e

echo "========================================="
echo "Testing Wheel Build Configuration"
echo "========================================="
echo ""
echo "Building ONE wheel to verify configuration:"
echo "  Platform: Linux x86_64"
echo "  Python: 3.12 only"
echo ""
echo "This will take ~5-10 minutes..."
echo ""

# Install cibuildwheel if not already installed
pip install -q cibuildwheel

# Build just one wheel for testing
CIBW_BUILD="cp312-manylinux_x86_64" \
CIBW_SKIP="*-musllinux*" \
CIBW_ARCHS="x86_64" \
python -m cibuildwheel --platform linux --output-dir test_wheelhouse

echo ""
echo "========================================="
echo "Build Complete!"
echo "========================================="
echo ""
echo "Generated wheels:"
ls -lh test_wheelhouse/
echo ""

# Test the wheel
if [ -f test_wheelhouse/*.whl ]; then
    echo "✅ SUCCESS: Wheel built successfully!"
    echo ""
    echo "Testing installation..."
    pip install test_wheelhouse/*.whl --force-reinstall
    python -c "import blend2d; print(f'✅ Import successful! Version: {blend2d.__version__}')"
    echo ""
    echo "🎉 Everything works! Configuration is correct."
else
    echo "❌ FAILED: No wheel was generated"
    exit 1
fi

