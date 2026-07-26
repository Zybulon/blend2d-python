/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2023 Blend2D Python Nanobind Port Maintainers
 * Copyright (c) 2019 John Wiggins (original Cython implementation)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#pragma once

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/pair.h>

#include <blend2d.h>
#include <string>
#include <vector>
#include <cmath>

namespace nb = nanobind;
using namespace nb::literals;

// Helper functions (equivalent to the ones in _capi.pyx)
static void _destroy_array_data(void *impl, void *externalData, void *userData) noexcept
{
    // In the original this was empty, keeping it that way
}

static uint32_t _get_rgba32_value(const nb::tuple &color)
{
    uint32_t r, g, b, alpha;

    r = uint32_t(255 * nb::cast<double>(color[0]));
    g = uint32_t(255 * nb::cast<double>(color[1]));
    b = uint32_t(255 * nb::cast<double>(color[2]));

    if (color.size() > 3)
    {
        alpha = uint32_t(255 * nb::cast<double>(color[3]));
    }
    else
    {
        alpha = 255;
    }

    return (alpha << 24) | (b << 16) | (g << 8) | r;
}

static std::string _utf8_string(const nb::object &s)
{
    if (nb::isinstance<nb::str>(s))
    {
        return nb::cast<std::string>(s);
    }
    else
    {
        throw nb::type_error("The input should be a string object");
    }
}

// Function declarations for binding each module
void register_enums(nb::module_ &m);
void register_geometry(nb::module_ &m);
void register_array(nb::module_ &m);
void register_image(nb::module_ &m);
void register_font(nb::module_ &m);
void register_path(nb::module_ &m);
void register_gradient(nb::module_ &m);
void register_pattern(nb::module_ &m);
void register_context(nb::module_ &m);
void register_misc(nb::module_ &m);
void register_pixel_convert(nb::module_ &m);