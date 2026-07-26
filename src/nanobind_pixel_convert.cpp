#include "nanobind_common.h"

void register_pixel_convert(nb::module_ &m)
{
    // Pixel format conversion functions
    m.def("rgba32_from_argb32", [](uint32_t argb32)
          { return BLRgba32(argb32).value; }, nb::arg("argb32"));

    m.def("argb32_from_rgba32", [](uint32_t rgba32)
          {
              // RGBA -> ARGB
              return ((rgba32 & 0xFF000000) >> 0) |  // A stays the same
                     ((rgba32 & 0x00FF0000) >> 16) | // R goes to the lowest byte
                     ((rgba32 & 0x0000FF00) >> 0) |  // G stays in the middle
                     ((rgba32 & 0x000000FF) << 16);  // B goes to the highest byte
          },
          nb::arg("rgba32"));

    m.def("rgba32_from_rgba", [](double r, double g, double b, double a)
          { return BLRgba32(
                       uint32_t(r * 255),
                       uint32_t(g * 255),
                       uint32_t(b * 255),
                       uint32_t(a * 255))
                .value; }, nb::arg("r"), nb::arg("g"), nb::arg("b"), nb::arg("a") = 1.0);

    m.def("rgba64_from_rgba", [](double r, double g, double b, double a)
          { return BLRgba64(
                       uint32_t(r * 65535),
                       uint32_t(g * 65535),
                       uint32_t(b * 65535),
                       uint32_t(a * 65535))
                .value; }, nb::arg("r"), nb::arg("g"), nb::arg("b"), nb::arg("a") = 1.0);
}