#include "nanobind_common.h"

void register_enums(nb::module_ &m)
{
    // Enums
    nb::enum_<BLObjectType>(m, "BLObjectType")
        .value("ARRAY_I8", BL_OBJECT_TYPE_ARRAY_INT8)
        .value("ARRAY_U8", BL_OBJECT_TYPE_ARRAY_UINT8)
        .value("ARRAY_I16", BL_OBJECT_TYPE_ARRAY_INT16)
        .value("ARRAY_U16", BL_OBJECT_TYPE_ARRAY_UINT16)
        .value("ARRAY_I32", BL_OBJECT_TYPE_ARRAY_INT32)
        .value("ARRAY_U32", BL_OBJECT_TYPE_ARRAY_UINT32)
        .value("ARRAY_I64", BL_OBJECT_TYPE_ARRAY_INT64)
        .value("ARRAY_U64", BL_OBJECT_TYPE_ARRAY_UINT64)
        .value("ARRAY_F32", BL_OBJECT_TYPE_ARRAY_FLOAT32)
        .value("ARRAY_F64", BL_OBJECT_TYPE_ARRAY_FLOAT64);

    nb::enum_<BLCompOp>(m, "BLCompOp")
        .value("SRC_OVER", BL_COMP_OP_SRC_OVER)
        .value("SRC_COPY", BL_COMP_OP_SRC_COPY)
        .value("SRC_IN", BL_COMP_OP_SRC_IN)
        .value("SRC_OUT", BL_COMP_OP_SRC_OUT)
        .value("SRC_ATOP", BL_COMP_OP_SRC_ATOP)
        .value("DST_OVER", BL_COMP_OP_DST_OVER)
        .value("DST_COPY", BL_COMP_OP_DST_COPY)
        .value("DST_IN", BL_COMP_OP_DST_IN)
        .value("DST_OUT", BL_COMP_OP_DST_OUT)
        .value("DST_ATOP", BL_COMP_OP_DST_ATOP)
        .value("XOR", BL_COMP_OP_XOR)
        .value("CLEAR", BL_COMP_OP_CLEAR)
        .value("PLUS", BL_COMP_OP_PLUS)
        .value("MINUS", BL_COMP_OP_MINUS)
        .value("MODULATE", BL_COMP_OP_MODULATE)
        .value("MULTIPLY", BL_COMP_OP_MULTIPLY)
        .value("SCREEN", BL_COMP_OP_SCREEN)
        .value("OVERLAY", BL_COMP_OP_OVERLAY)
        .value("DARKEN", BL_COMP_OP_DARKEN)
        .value("LIGHTEN", BL_COMP_OP_LIGHTEN)
        .value("COLOR_DODGE", BL_COMP_OP_COLOR_DODGE)
        .value("COLOR_BURN", BL_COMP_OP_COLOR_BURN)
        .value("LINEAR_BURN", BL_COMP_OP_LINEAR_BURN)
        .value("LINEAR_LIGHT", BL_COMP_OP_LINEAR_LIGHT)
        .value("PIN_LIGHT", BL_COMP_OP_PIN_LIGHT)
        .value("HARD_LIGHT", BL_COMP_OP_HARD_LIGHT)
        .value("SOFT_LIGHT", BL_COMP_OP_SOFT_LIGHT)
        .value("DIFFERENCE", BL_COMP_OP_DIFFERENCE)
        .value("EXCLUSION", BL_COMP_OP_EXCLUSION);

    nb::enum_<BLExtendMode>(m, "BLExtendMode")
        .value("PAD", BL_EXTEND_MODE_PAD)
        .value("REPEAT", BL_EXTEND_MODE_REPEAT)
        .value("REFLECT", BL_EXTEND_MODE_REFLECT)
        .value("PAD_X_PAD_Y", BL_EXTEND_MODE_PAD_X_PAD_Y)
        .value("REPEAT_X_REPEAT_Y", BL_EXTEND_MODE_REPEAT_X_REPEAT_Y)
        .value("REFLECT_X_REFLECT_Y", BL_EXTEND_MODE_REFLECT_X_REFLECT_Y)
        .value("PAD_X_REPEAT_Y", BL_EXTEND_MODE_PAD_X_REPEAT_Y)
        .value("PAD_X_REFLECT_Y", BL_EXTEND_MODE_PAD_X_REFLECT_Y)
        .value("REPEAT_X_PAD_Y", BL_EXTEND_MODE_REPEAT_X_PAD_Y)
        .value("REPEAT_X_REFLECT_Y", BL_EXTEND_MODE_REPEAT_X_REFLECT_Y)
        .value("REFLECT_X_PAD_Y", BL_EXTEND_MODE_REFLECT_X_PAD_Y)
        .value("REFLECT_X_REPEAT_Y", BL_EXTEND_MODE_REFLECT_X_REPEAT_Y);

    nb::enum_<BLFormat>(m, "BLFormat")
        .value("NONE", BL_FORMAT_NONE)
        .value("PRGB32", BL_FORMAT_PRGB32)
        .value("XRGB32", BL_FORMAT_XRGB32)
        .value("A8", BL_FORMAT_A8);

    nb::enum_<BLStrokeCap>(m, "BLStrokeCap")
        .value("CAP_BUTT", BL_STROKE_CAP_BUTT)
        .value("CAP_SQUARE", BL_STROKE_CAP_SQUARE)
        .value("CAP_ROUND", BL_STROKE_CAP_ROUND)
        .value("CAP_ROUND_REV", BL_STROKE_CAP_ROUND_REV)
        .value("CAP_TRIANGLE", BL_STROKE_CAP_TRIANGLE)
        .value("CAP_TRIANGLE_REV", BL_STROKE_CAP_TRIANGLE_REV);

    nb::enum_<BLStrokeCapPosition>(m, "BLStrokeCapPosition")
        .value("CAP_START", BL_STROKE_CAP_POSITION_START)
        .value("CAP_END", BL_STROKE_CAP_POSITION_END);

    nb::enum_<BLStrokeJoin>(m, "BLStrokeJoin")
        .value("JOIN_MITER_CLIP", BL_STROKE_JOIN_MITER_CLIP)
        .value("JOIN_MITER_BEVEL", BL_STROKE_JOIN_MITER_BEVEL)
        .value("JOIN_MITER_ROUND", BL_STROKE_JOIN_MITER_ROUND)
        .value("JOIN_BEVEL", BL_STROKE_JOIN_BEVEL)
        .value("JOIN_ROUND", BL_STROKE_JOIN_ROUND);

    // Font-related enums
    m.attr("OPENTYPE_GDEF") = BL_MAKE_TAG('G', 'D', 'E', 'F');
    m.attr("OPENTYPE_GPOS") = BL_MAKE_TAG('G', 'P', 'O', 'S');
    m.attr("OPENTYPE_GSUB") = BL_MAKE_TAG('G', 'S', 'U', 'B');
    m.attr("OPENTYPE_KERN") = BL_MAKE_TAG('k', 'e', 'r', 'n');

    nb::enum_<BLFontOutlineType>(m, "BLFontOutlineType")
        .value("NONE", BL_FONT_OUTLINE_TYPE_NONE)
        .value("TRUETYPE", BL_FONT_OUTLINE_TYPE_TRUETYPE)
        .value("CFF", BL_FONT_OUTLINE_TYPE_CFF);

    // Add gradient type enum
    nb::enum_<BLGradientType>(m, "BLGradientType")
        .value("LINEAR", BL_GRADIENT_TYPE_LINEAR)
        .value("RADIAL", BL_GRADIENT_TYPE_RADIAL)
        .value("CONICAL", BL_GRADIENT_TYPE_CONIC);

    // Add fill rule enum
    nb::enum_<BLFillRule>(m, "BLFillRule")
        .value("NON_ZERO", BL_FILL_RULE_NON_ZERO)
        .value("EVEN_ODD", BL_FILL_RULE_EVEN_ODD);

    // Add transform op enum
    nb::enum_<BLTransformOp>(m, "BLTransformOp")
        .value("RESET", BL_TRANSFORM_OP_RESET)
        .value("ASSIGN", BL_TRANSFORM_OP_ASSIGN)
        .value("TRANSLATE", BL_TRANSFORM_OP_TRANSLATE)
        .value("SCALE", BL_TRANSFORM_OP_SCALE)
        .value("SKEW", BL_TRANSFORM_OP_SKEW)
        .value("ROTATE", BL_TRANSFORM_OP_ROTATE)
        .value("ROTATE_PT", BL_TRANSFORM_OP_ROTATE_PT)
        .value("TRANSFORM", BL_TRANSFORM_OP_TRANSFORM);
}