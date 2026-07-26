#include "nanobind_common.h"
#include <cstring>
#include <stdexcept>

// Helper function for destroying data
static void fontDataDestroyCallback(void *impl, void *userData, void *) noexcept
{
    delete[] static_cast<char *>(userData);
}

void register_font(nb::module_ &m)
{
    // FontData
    nb::class_<BLFontData>(m, "BLFontData")
        .def(nb::init<>())
        .def("__del__", [](BLFontData *self)
             { self->reset(); })
        .def_static("create_from_file", [](const char *fileName)
                    {
             BLFontData data;
             data.createFromFile(fileName, BL_FILE_READ_MMAP_ENABLED);
             return data; }, nb::arg("fileName"))
        .def_static("create_from_data", [](nb::bytes data)
                    {
             // Copy the data to a new buffer
             char* buffer = new char[data.size()];
             std::memcpy(buffer, data.c_str(), data.size());

             BLFontData fontData;
             fontData.createFromData(buffer, data.size(), fontDataDestroyCallback, buffer);
             return fontData; }, nb::arg("data"))
        .def("empty", [](const BLFontData &self)
             { return self.empty(); });

    // FontFace
    nb::class_<BLFontFace>(m, "BLFontFace")
        .def(nb::init<>())
        .def("__del__", [](BLFontFace *self)
             { self->reset(); })
        .def_static("create_from_file", [](const char *fileName, uint32_t index)
                    {
             BLFontFace face;
             // Use BL_FILE_READ_NO_FLAGS as second parameter
             face.createFromFile(fileName, BL_FILE_READ_NO_FLAGS);
             return face; }, nb::arg("fileName"), nb::arg("index") = 0)
        .def_static("create_from_data", [](const BLFontData &fontData, uint32_t index)
                    {
             BLFontFace face;
             face.createFromData(fontData, index);
             return face; }, nb::arg("fontData"), nb::arg("index") = 0)
        .def("empty", [](const BLFontFace &self)
             { return self.empty(); })
        .def_prop_ro("family_name", [](const BLFontFace &self)
                     { return std::string(self.familyName().data(), self.familyName().size()); })
        .def_prop_ro("full_name", [](const BLFontFace &self)
                     { return std::string(self.fullName().data(), self.fullName().size()); })
        .def_prop_ro("style_name", [](const BLFontFace &self)
                     { return std::string(self.subfamilyName().data(), self.subfamilyName().size()); })
        .def_prop_ro("post_script_name", [](const BLFontFace &self)
                     { return std::string(self.postScriptName().data(), self.postScriptName().size()); })
        .def_prop_ro("weight", [](const BLFontFace &self)
                     { return self.weight(); })
        .def_prop_ro("stretch", [](const BLFontFace &self)
                     { return self.stretch(); })
        .def_prop_ro("style", [](const BLFontFace &self)
                     { return self.style(); });

    // Font
    nb::class_<BLFont>(m, "BLFont")
        .def(nb::init<>())
        .def("__del__", [](BLFont *self)
             { self->reset(); })
        .def("create_from_face", [](BLFont &self, const BLFontFace &face, float size)
             {
             BLResult err = self.createFromFace(face, size);
             if (err != BL_SUCCESS)
                 throw std::runtime_error("Failed to create font from face");
             return nb::none(); }, nb::arg("face"), nb::arg("size"))
        .def_static("create_new", [](const BLFontFace &face, float size)
                    {
             BLFont font;
             BLResult err = font.createFromFace(face, size);
             if (err != BL_SUCCESS)
                 throw std::runtime_error("Failed to create font from face");
             return font; }, nb::arg("face"), nb::arg("size"))
        .def("empty", [](const BLFont &self)
             { return self.empty(); })
        .def_prop_ro("size", [](const BLFont &self)
                     { return self.size(); })
        .def_prop_ro("metrics", [](const BLFont &self)
                     {
             BLFontMetrics m = self.metrics();
             return nb::make_tuple(
                 m.size,
                 m.ascent,
                 m.descent,
                 m.lineGap,
                 m.xHeight,
                 m.capHeight); })
        .def("shape", [](const BLFont &self, const char *text)
             {
             BLGlyphBuffer gb;
             // Use BL_TEXT_ENCODING_UTF8 as the text encoding
             gb.setText(text, strlen(text), BL_TEXT_ENCODING_UTF8);
             self.shape(gb);
             
             size_t size = gb.size();
             nb::list indices;
             nb::list positions;

             // Use proper accessor methods instead of directly accessing impl
             const uint32_t* content = gb.content();
             const BLGlyphPlacement* placements = gb.placementData();

             if (content == nullptr || placements == nullptr) {
                 throw std::runtime_error("Failed to get glyph data");
             }

             for (size_t i = 0; i < size; i++) {
                 indices.append(content[i]);
                 positions.append(nb::make_tuple(placements[i].placement.x, placements[i].placement.y));
             }

             return nb::make_tuple(indices, positions); }, nb::arg("text"))
        .def("get_text_metrics", [](const BLFont &self, const char *text)
             {
             BLTextMetrics tm;
             BLGlyphBuffer gb;
             gb.setText(text, strlen(text), BL_TEXT_ENCODING_UTF8);
             self.shape(gb);
             
             // Use a temporary BLTextMetrics for the out parameter
             BLTextMetrics out;
             self.getTextMetrics(gb, out);
             tm = out;
             
             return nb::make_tuple(
                 tm.advance.x,
                 tm.advance.y,
                 tm.boundingBox.x0,
                 tm.boundingBox.y0,
                 tm.boundingBox.x1,
                 tm.boundingBox.y1); }, nb::arg("text"));

    // GlyphBuffer
    nb::class_<BLGlyphBuffer>(m, "BLGlyphBuffer")
        .def(nb::init<>())
        .def("__del__", [](BLGlyphBuffer *self)
             { self->reset(); })
        .def("clear", [](BLGlyphBuffer &self)
             { self.clear(); })
        .def("reset", [](BLGlyphBuffer &self)
             { self.reset(); })
        .def("set_text", [](BLGlyphBuffer &self, const char *text, size_t size)
             { self.setText(text, size, BL_TEXT_ENCODING_UTF8); }, nb::arg("text"), nb::arg("size"))
        .def("set_text", [](BLGlyphBuffer &self, const char *text)
             { self.setText(text, strlen(text), BL_TEXT_ENCODING_UTF8); }, nb::arg("text"))
        .def_prop_ro("size", [](const BLGlyphBuffer &self)
                     { return self.size(); })
        .def_prop_ro("empty", [](const BLGlyphBuffer &self)
                     { return self.empty(); });
}