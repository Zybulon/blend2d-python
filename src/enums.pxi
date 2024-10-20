# The MIT License (MIT)
#
# Copyright (c) 2019 John Wiggins
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

cpdef enum ArrayType:
    ARRAY_I8 = _capi.BL_OBJECT_TYPE_ARRAY_INT8
    ARRAY_U8 = _capi.BL_OBJECT_TYPE_ARRAY_UINT8
    ARRAY_I16 = _capi.BL_OBJECT_TYPE_ARRAY_INT16
    ARRAY_U16 = _capi.BL_OBJECT_TYPE_ARRAY_UINT16
    ARRAY_I32 = _capi.BL_OBJECT_TYPE_ARRAY_INT32
    ARRAY_U32 = _capi.BL_OBJECT_TYPE_ARRAY_UINT32
    ARRAY_I64 = _capi.BL_OBJECT_TYPE_ARRAY_INT64
    ARRAY_U64 = _capi.BL_OBJECT_TYPE_ARRAY_UINT64
    ARRAY_F32 = _capi.BL_OBJECT_TYPE_ARRAY_FLOAT32
    ARRAY_F64 = _capi.BL_OBJECT_TYPE_ARRAY_FLOAT64

cpdef enum CompOp:
    SRC_OVER = _capi.BL_COMP_OP_SRC_OVER
    SRC_COPY = _capi.BL_COMP_OP_SRC_COPY
    SRC_IN = _capi.BL_COMP_OP_SRC_IN
    SRC_OUT = _capi.BL_COMP_OP_SRC_OUT
    SRC_ATOP = _capi.BL_COMP_OP_SRC_ATOP
    DST_OVER = _capi.BL_COMP_OP_DST_OVER
    DST_COPY = _capi.BL_COMP_OP_DST_COPY
    DST_IN = _capi.BL_COMP_OP_DST_IN
    DST_OUT = _capi.BL_COMP_OP_DST_OUT
    DST_ATOP = _capi.BL_COMP_OP_DST_ATOP
    XOR = _capi.BL_COMP_OP_XOR
    CLEAR = _capi.BL_COMP_OP_CLEAR
    PLUS = _capi.BL_COMP_OP_PLUS
    MINUS = _capi.BL_COMP_OP_MINUS
    MODULATE = _capi.BL_COMP_OP_MODULATE
    MULTIPLY = _capi.BL_COMP_OP_MULTIPLY
    SCREEN = _capi.BL_COMP_OP_SCREEN
    OVERLAY = _capi.BL_COMP_OP_OVERLAY
    DARKEN = _capi.BL_COMP_OP_DARKEN
    LIGHTEN = _capi.BL_COMP_OP_LIGHTEN
    COLOR_DODGE = _capi.BL_COMP_OP_COLOR_DODGE
    COLOR_BURN = _capi.BL_COMP_OP_COLOR_BURN
    LINEAR_BURN = _capi.BL_COMP_OP_LINEAR_BURN
    LINEAR_LIGHT = _capi.BL_COMP_OP_LINEAR_LIGHT
    PIN_LIGHT = _capi.BL_COMP_OP_PIN_LIGHT
    HARD_LIGHT = _capi.BL_COMP_OP_HARD_LIGHT
    SOFT_LIGHT = _capi.BL_COMP_OP_SOFT_LIGHT
    DIFFERENCE = _capi.BL_COMP_OP_DIFFERENCE
    EXCLUSION = _capi.BL_COMP_OP_EXCLUSION

cpdef enum ExtendMode:
    PAD = _capi.BL_EXTEND_MODE_PAD
    REPEAT = _capi.BL_EXTEND_MODE_REPEAT
    REFLECT = _capi.BL_EXTEND_MODE_REFLECT
    PAD_X_PAD_Y = _capi.BL_EXTEND_MODE_PAD_X_PAD_Y
    REPEAT_X_REPEAT_Y = _capi.BL_EXTEND_MODE_REPEAT_X_REPEAT_Y
    REFLECT_X_REFLECT_Y = _capi.BL_EXTEND_MODE_REFLECT_X_REFLECT_Y
    PAD_X_REPEAT_Y = _capi.BL_EXTEND_MODE_PAD_X_REPEAT_Y
    PAD_X_REFLECT_Y = _capi.BL_EXTEND_MODE_PAD_X_REFLECT_Y
    REPEAT_X_PAD_Y = _capi.BL_EXTEND_MODE_REPEAT_X_PAD_Y
    REPEAT_X_REFLECT_Y = _capi.BL_EXTEND_MODE_REPEAT_X_REFLECT_Y
    REFLECT_X_PAD_Y = _capi.BL_EXTEND_MODE_REFLECT_X_PAD_Y
    REFLECT_X_REPEAT_Y = _capi.BL_EXTEND_MODE_REFLECT_X_REPEAT_Y

cpdef enum Format:
    NONE = _capi.BL_FORMAT_NONE
    PRGB32 = _capi.BL_FORMAT_PRGB32
    XRGB32 = _capi.BL_FORMAT_XRGB32
    A8 = _capi.BL_FORMAT_A8

cpdef enum StrokeCap:
    CAP_BUTT = _capi.BL_STROKE_CAP_BUTT
    CAP_SQUARE = _capi.BL_STROKE_CAP_SQUARE
    CAP_ROUND = _capi.BL_STROKE_CAP_ROUND
    CAP_ROUND_REV = _capi.BL_STROKE_CAP_ROUND_REV
    CAP_TRIANGLE = _capi.BL_STROKE_CAP_TRIANGLE
    CAP_TRIANGLE_REV = _capi.BL_STROKE_CAP_TRIANGLE_REV

cpdef enum StrokeCapPosition:
    CAP_START = _capi.BL_STROKE_CAP_POSITION_START
    CAP_END = _capi.BL_STROKE_CAP_POSITION_END

cpdef enum StrokeJoin:
    JOIN_MITER_CLIP = _capi.BL_STROKE_JOIN_MITER_CLIP
    JOIN_MITER_BEVEL = _capi.BL_STROKE_JOIN_MITER_BEVEL
    JOIN_MITER_ROUND = _capi.BL_STROKE_JOIN_MITER_ROUND
    JOIN_BEVEL = _capi.BL_STROKE_JOIN_BEVEL
    JOIN_ROUND = _capi.BL_STROKE_JOIN_ROUND
