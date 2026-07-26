#include "nanobind_common.h"
#include <cstring> // For std::memcpy
#include <vector>

void register_path(nb::module_ &m)
{
     nb::class_<BLPath>(m, "BLPath")
         .def(nb::init<>())
         .def("__del__", [](BLPath *self)
              { self->reset(); })
         .def("copy", [](const BLPath &self)
              {
            BLPath* path = new BLPath();
            path->assignDeep(self);
            return path; })
         .def("clear", [](BLPath &self)
              { self.clear(); })
         .def("reset", [](BLPath &self)
              { self.reset(); })
         .def("empty", [](const BLPath &self)
              { return self.empty(); })
         .def("get_bounding_box", [](const BLPath &self)
              {
            BLBox box;
            self.getBoundingBox(&box);
            return box; })
         .def("get_last_vertex", [](const BLPath &self)
              {
            BLPoint pt;
            self.getLastVertex(&pt);
            return nb::make_tuple(pt.x, pt.y); })
         .def("close", [](BLPath &self)
              { self.close(); })
         .def("move_to", [](BLPath &self, double x, double y)
              { self.moveTo(x, y); }, nb::arg("x"), nb::arg("y"))
         .def("line_to", [](BLPath &self, double x, double y)
              { self.lineTo(x, y); }, nb::arg("x"), nb::arg("y"))
         .def("arc_to", [](BLPath &self, double cx, double cy, double rx, double ry, double start, double sweep, bool forceMoveTo)
              { self.arcTo(cx, cy, rx, ry, start, sweep, forceMoveTo); }, nb::arg("cx"), nb::arg("cy"), nb::arg("rx"), nb::arg("ry"), nb::arg("start"), nb::arg("sweep"), nb::arg("forceMoveTo") = false)
         .def("quadric_to", [](BLPath &self, double x1, double y1, double x2, double y2)
              { self.quadTo(x1, y1, x2, y2); }, nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"))
         .def("cubic_to", [](BLPath &self, double x1, double y1, double x2, double y2, double x3, double y3)
              { self.cubicTo(x1, y1, x2, y2, x3, y3); }, nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"), nb::arg("x3"), nb::arg("y3"))
         .def("arc_quadrant_to", [](BLPath &self, double x1, double y1, double x2, double y2)
              { self.arcQuadrantTo(x1, y1, x2, y2); }, nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"))
         .def("elliptic_arc_to", [](BLPath &self, double rx, double ry, double xAxisRotation, bool largeArcFlag, bool sweepFlag, double x, double y)
              { self.ellipticArcTo(rx, ry, xAxisRotation, largeArcFlag, sweepFlag, x, y); }, nb::arg("rx"), nb::arg("ry"), nb::arg("xAxisRotation"), nb::arg("largeArcFlag"), nb::arg("sweepFlag"), nb::arg("x"), nb::arg("y"))
         .def("add_rect", [](BLPath &self, const BLRect &rect)
              { self.addRect(rect); }, nb::arg("rect"))
         .def("add_circle", [](BLPath &self, double cx, double cy, double r)
              { self.addCircle(BLCircle(cx, cy, r)); }, nb::arg("cx"), nb::arg("cy"), nb::arg("r"))
         .def("add_ellipse", [](BLPath &self, double cx, double cy, double rx, double ry)
              { self.addEllipse(BLEllipse(cx, cy, rx, ry)); }, nb::arg("cx"), nb::arg("cy"), nb::arg("rx"), nb::arg("ry"))
         .def("add_round_rect", [](BLPath &self, const BLRect &rect, double r)
              { self.addRoundRect(BLRoundRect(rect, r)); }, nb::arg("rect"), nb::arg("r"))
         .def("add_round_rect", [](BLPath &self, const BLRect &rect, double rx, double ry)
              { self.addRoundRect(BLRoundRect(rect, rx, ry)); }, nb::arg("rect"), nb::arg("rx"), nb::arg("ry"))
         .def("add_arc", [](BLPath &self, double cx, double cy, double r, double start, double sweep)
              { self.addArc(BLArc(cx, cy, r, r, start, sweep)); }, nb::arg("cx"), nb::arg("cy"), nb::arg("r"), nb::arg("start"), nb::arg("sweep"))
         .def("add_pie", [](BLPath &self, double cx, double cy, double r, double start, double sweep)
              { self.addPie(BLArc(cx, cy, r, r, start, sweep)); }, nb::arg("cx"), nb::arg("cy"), nb::arg("r"), nb::arg("start"), nb::arg("sweep"))
         .def("add_chord", [](BLPath &self, double cx, double cy, double r, double start, double sweep)
              { self.addChord(BLArc(cx, cy, r, r, start, sweep)); }, nb::arg("cx"), nb::arg("cy"), nb::arg("r"), nb::arg("start"), nb::arg("sweep"))
         .def("add_path", [](BLPath &self, const BLPath &other)
              { self.addPath(other); }, nb::arg("other"))
         .def("transform", [](BLPath &self, const BLMatrix2D &matrix)
              { self.transform(matrix); }, nb::arg("matrix"))
         .def("get_command_data", [](const BLPath &self)
              {
            const uint8_t* cmd = self.commandData();
            size_t count = self.size();
            
            // Create a temporary buffer for the command data
            auto* buffer = new uint8_t[count];
            std::memcpy(buffer, cmd, count);
            
            // Create a capsule that will delete the buffer when the array is deleted
            nb::capsule deleter(buffer, [](void* p) noexcept { delete[] static_cast<uint8_t*>(p); });
            
            // Create numpy array with the buffer
            std::vector<size_t> shape = {count};
            return nb::ndarray<nb::numpy, uint8_t>(buffer, shape.size(), shape.data(), deleter); })
         .def("get_vertex_data", [](const BLPath &self)
              {
            const BLPoint* vtx = self.vertexData();
            size_t count = self.size();
            
            // Create a temporary buffer for the vertex data as doubles
            auto* buffer = new double[count * 2];
            for (size_t i = 0; i < count; i++) {
                buffer[i*2]     = vtx[i].x;
                buffer[i*2 + 1] = vtx[i].y;
            }
            
            // Create a capsule that will delete the buffer when the array is deleted
            nb::capsule deleter(buffer, [](void* p) noexcept { delete[] static_cast<double*>(p); });
            
            // Create numpy array with the buffer
            std::vector<size_t> shape = {count, 2};
            return nb::ndarray<nb::numpy, double>(buffer, shape.size(), shape.data(), deleter); })
         .def("hit_test", [](const BLPath &self, double x, double y, BLFillRule fillRule)
              { return self.hitTest(BLPoint(x, y), fillRule); }, nb::arg("x"), nb::arg("y"), nb::arg("fillRule") = BL_FILL_RULE_NON_ZERO);
}