#include "nanobind_common.h"

// Main module definition
NB_MODULE(_capi, m)
{
    m.doc() = "Blend2D Python bindings using nanobind";

    // Register all submodules
    register_enums(m);
    register_geometry(m);
    register_array(m);
    register_image(m);
    register_font(m);
    register_path(m);
    register_gradient(m);
    register_pattern(m);
    register_context(m);
    register_misc(m);
    register_pixel_convert(m);
}