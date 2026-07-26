#include "nanobind_common.h"
#include <cstring>
#include <stdexcept>

namespace nb = nanobind;

void register_image(nb::module_ &m)
{
    // First register the image filter enum
    nb::enum_<BLImageScaleFilter>(m, "BLImageScaleFilter")
        .value("NONE", BL_IMAGE_SCALE_FILTER_NONE)
        .value("NEAREST", BL_IMAGE_SCALE_FILTER_NEAREST)
        .value("BILINEAR", BL_IMAGE_SCALE_FILTER_BILINEAR)
        .value("BICUBIC", BL_IMAGE_SCALE_FILTER_BICUBIC)
        .value("LANCZOS", BL_IMAGE_SCALE_FILTER_LANCZOS);

    // BLImage class - use BLImage as the class name to match C++ code
    nb::class_<BLImage>(m, "BLImage")
        .def(nb::init<>())
        .def(nb::init<int, int, BLFormat>(), nb::arg("w"), nb::arg("h"), nb::arg("format") = BL_FORMAT_PRGB32)

        // Common functionality
        .def("reset", &BLImage::reset)
        .def("empty", &BLImage::empty)
        .def("equals", &BLImage::equals)

        // Create functionality
        .def("create", [](BLImage &self, int w, int h, BLFormat format)
             {
            BLResult result = self.create(w, h, format);
            if (result != BL_SUCCESS) {
                throw std::runtime_error("Failed to create image");
            } }, nb::arg("w"), nb::arg("h"), nb::arg("format") = BL_FORMAT_PRGB32)

        .def_static("createNew", [](int w, int h, BLFormat format)
                    {
            BLImage img;
            BLResult result = img.create(w, h, format);
            if (result != BL_SUCCESS) {
                throw std::runtime_error("Failed to create image");
            }
            return img; }, nb::arg("w"), nb::arg("h"), nb::arg("format") = BL_FORMAT_PRGB32)

        // Image IO
        .def("readFromFile", [](BLImage &self, const std::string &fileName)
             {
            BLResult result = self.readFromFile(fileName.c_str());
            if (result != BL_SUCCESS) {
                throw std::runtime_error("Failed to read image from file");
            } }, nb::arg("fileName"))

        .def("writeToFile", [](const BLImage &self, const std::string &fileName)
             {
            BLResult result = self.writeToFile(fileName.c_str());
            if (result != BL_SUCCESS) {
                throw std::runtime_error("Failed to write image to file");
            } }, nb::arg("fileName"))

        // Image conversion
        .def("convert", [](BLImage &self, BLFormat format)
             {
            BLResult result = self.convert(format);
            if (result != BL_SUCCESS) {
                throw std::runtime_error("Failed to convert image format");
            } }, nb::arg("format"))

        // Scaling - use the proper enum type
        .def_static("scale", [](BLImage &dst, const BLImage &src, int w, int h, BLImageScaleFilter filter)
                    {
            BLSizeI size(w, h);
            BLResult result = BLImage::scale(dst, src, size, filter);
            if (result != BL_SUCCESS) {
                throw std::runtime_error("Failed to scale image");
            } }, nb::arg("dst"), nb::arg("src"), nb::arg("w"), nb::arg("h"), nb::arg("filter") = BL_IMAGE_SCALE_FILTER_BILINEAR)

        // Convenience method for in-place scaling - use the proper enum type
        .def("scaleToSize", [](BLImage &self, int w, int h, BLImageScaleFilter filter)
             {
            BLImage dst;
            BLSizeI size(w, h);
            BLResult result = BLImage::scale(dst, self, size, filter);
            if (result != BL_SUCCESS) {
                throw std::runtime_error("Failed to scale image");
            }
            self = std::move(dst); }, nb::arg("w"), nb::arg("h"), nb::arg("filter") = BL_IMAGE_SCALE_FILTER_BILINEAR)

        // Properties
        .def_prop_ro("width", &BLImage::width)
        .def_prop_ro("height", &BLImage::height)
        .def_prop_ro("depth", &BLImage::depth)
        .def_prop_ro("format", &BLImage::format)
        .def_prop_ro("size", [](const BLImage &self)
                     { return nb::make_tuple(self.width(), self.height()); })

        // Image data access
        .def("getData", [](const BLImage &self)
             {
            if (self.empty()) {
                throw nb::value_error("Image is empty");
            }

            BLImageData data;
            self.getData(&data);
            
            if (!data.pixelData) {
                throw nb::value_error("Failed to get pixel data");
            }

            // Return a dictionary with image data information
            auto result = nb::dict();
            result["width"] = self.width();
            result["height"] = self.height();
            result["format"] = int(self.format());
            result["stride"] = data.stride;
            
            return result; })

        // Create a NumPy array from image data
        .def("getDataAsNumPy", [](const BLImage &self)
             {
            if (self.empty()) {
                throw nb::value_error("Image is empty");
            }

            BLImageData data;
            self.getData(&data);
            
            if (!data.pixelData) {
                throw nb::value_error("Failed to get pixel data");
            }

            int width = self.width();
            int height = self.height();
            intptr_t stride = data.stride;
            uint32_t format = self.format();

            // Determine shape and format for numpy array
            std::vector<size_t> shape;
            std::vector<int64_t> strides;
            int channels;

            switch (format) {
                case BL_FORMAT_PRGB32:
                case BL_FORMAT_XRGB32:
                    channels = 4;
                    shape = {static_cast<size_t>(height), static_cast<size_t>(width), static_cast<size_t>(channels)};
                    strides = {stride, static_cast<int64_t>(channels), 1};
                    break;
                case BL_FORMAT_A8:
                    channels = 1;
                    shape = {static_cast<size_t>(height), static_cast<size_t>(width)};
                    strides = {stride, 1};
                    break;
                default:
                    throw nb::value_error("Unsupported format for numpy conversion");
            }

            // Create a numpy array that references the image data (no copy)
            return nb::ndarray<nb::numpy, uint8_t>(
                static_cast<uint8_t*>(data.pixelData),
                shape.size(), shape.data(),
                nullptr,  // No owner - the data is owned by the BLImage
                strides.data()
            ); });
}