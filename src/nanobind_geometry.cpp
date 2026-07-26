#include "nanobind_common.h"
#include <cmath>

void register_geometry(nb::module_ &m)
{
     // Matrix2D
     nb::class_<BLMatrix2D>(m, "Matrix2D")
         .def(nb::init<>())
         .def(nb::init<double, double, double, double, double, double>())
         .def("__del__", [](BLMatrix2D *self)
              {
                   // No explicit destruction needed for BLMatrix2D
              })
         .def("rotate", [](BLMatrix2D &self, double angle, double cx, double cy)
              { self.rotate(angle, cx, cy); return self; }, nb::arg("angle"), nb::arg("cx") = 0.0, nb::arg("cy") = 0.0)
         .def("scale", [](BLMatrix2D &self, double x, double y)
              { self.scale(x, y); return self; }, nb::arg("x"), nb::arg("y"))
         .def("translate", [](BLMatrix2D &self, double x, double y)
              { self.translate(x, y); return self; }, nb::arg("x"), nb::arg("y"))
         .def("reset", [](BLMatrix2D &self)
              { self.reset(); return self; })
         .def("invert", [](BLMatrix2D &self)
              { return self.invert() == BL_SUCCESS; })
         .def("get_type", [](const BLMatrix2D &self)
              { return self.type(); })
         .def("is_identity", [](const BLMatrix2D &self)
              { return self.type() == BL_TRANSFORM_TYPE_IDENTITY; })
         .def("is_valid", [](const BLMatrix2D &self)
              {
            // Check if the matrix contains finite values
            const double* m = self.m;
            for (int i = 0; i < 6; i++) {
                if (!std::isfinite(m[i]))
                    return false;
            }
            return true; })
         .def("map", [](const BLMatrix2D &self, double x, double y)
              { return self.mapPoint(x, y); }, nb::arg("x"), nb::arg("y"))
         .def("map_point", [](const BLMatrix2D &self, const BLPoint &p)
              { return self.mapPoint(p); }, nb::arg("point"))
         .def("map_vector", [](const BLMatrix2D &self, double x, double y)
              { return self.mapVector(x, y); }, nb::arg("x"), nb::arg("y"))
         .def("map_vector_point", [](const BLMatrix2D &self, const BLPoint &p)
              { return self.mapVector(p); }, nb::arg("point"))
         .def("transform", [](BLMatrix2D &self, const BLMatrix2D &other)
              { self.transform(other); return self; }, nb::arg("matrix"))
         .def("post_translate", [](BLMatrix2D &self, double x, double y)
              { self.postTranslate(x, y); return self; }, nb::arg("x"), nb::arg("y"))
         .def("post_scale", [](BLMatrix2D &self, double x, double y)
              { self.postScale(x, y); return self; }, nb::arg("x"), nb::arg("y"))
         .def("post_rotate", [](BLMatrix2D &self, double angle)
              { self.postRotate(angle); return self; }, nb::arg("angle"))
         .def("get_m", [](const BLMatrix2D &self, int index)
              {
            if (index < 0 || index > 5) {
                throw nb::value_error("Matrix index out of range (0-5)");
            }
            return self.m[index]; }, nb::arg("index"));

     // Static methods as module-level functions
     m.def("make_identity_matrix", []()
           { return BLMatrix2D::makeIdentity(); });
     m.def("make_translation_matrix", [](double x, double y)
           { return BLMatrix2D::makeTranslation(x, y); }, nb::arg("x"), nb::arg("y"));
     m.def("make_scaling_matrix", [](double x, double y)
           { return BLMatrix2D::makeScaling(x, y); }, nb::arg("x"), nb::arg("y"));
     m.def("make_rotation_matrix", [](double angle, double x, double y)
           { return BLMatrix2D::makeRotation(angle, x, y); }, nb::arg("angle"), nb::arg("x") = 0.0, nb::arg("y") = 0.0);
     m.def("make_skewing_matrix", [](double x, double y)
           { return BLMatrix2D::makeSkewing(x, y); }, nb::arg("x"), nb::arg("y"));

     // Rect
     nb::class_<BLRect>(m, "BLRect")
         .def(nb::init<float, float, float, float>(),
              nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"))
         .def_rw("x", &BLRect::x)
         .def_rw("y", &BLRect::y)
         .def_rw("w", &BLRect::w)
         .def_rw("h", &BLRect::h)
         .def("__repr__", [](const BLRect &self)
              { return "Rect(x=" + std::to_string(self.x) +
                       ", y=" + std::to_string(self.y) +
                       ", w=" + std::to_string(self.w) +
                       ", h=" + std::to_string(self.h) + ")"; });

     // RectI
     nb::class_<BLRectI>(m, "BLRectI")
         .def(nb::init<int, int, int, int>(),
              nb::arg("x"), nb::arg("y"), nb::arg("w"), nb::arg("h"))
         .def_rw("x", &BLRectI::x)
         .def_rw("y", &BLRectI::y)
         .def_rw("w", &BLRectI::w)
         .def_rw("h", &BLRectI::h)
         .def("__repr__", [](const BLRectI &self)
              { return "RectI(x=" + std::to_string(self.x) +
                       ", y=" + std::to_string(self.y) +
                       ", w=" + std::to_string(self.w) +
                       ", h=" + std::to_string(self.h) + ")"; });

     // Box
     nb::class_<BLBox>(m, "BLBox")
         .def(nb::init<double, double, double, double>(),
              nb::arg("x0"), nb::arg("y0"), nb::arg("x1"), nb::arg("y1"))
         .def_rw("x0", &BLBox::x0)
         .def_rw("y0", &BLBox::y0)
         .def_rw("x1", &BLBox::x1)
         .def_rw("y1", &BLBox::y1)
         .def("__repr__", [](const BLBox &self)
              { return "Box(x0=" + std::to_string(self.x0) +
                       ", y0=" + std::to_string(self.y0) +
                       ", x1=" + std::to_string(self.x1) +
                       ", y1=" + std::to_string(self.y1) + ")"; });

     // Point
     nb::class_<BLPoint>(m, "BLPoint")
         .def(nb::init<double, double>(),
              nb::arg("x"), nb::arg("y"))
         .def_rw("x", &BLPoint::x)
         .def_rw("y", &BLPoint::y)
         .def("__repr__", [](const BLPoint &self)
              { return "Point(x=" + std::to_string(self.x) +
                       ", y=" + std::to_string(self.y) + ")"; });

     // PointI
     nb::class_<BLPointI>(m, "BLPointI")
         .def(nb::init<int, int>(),
              nb::arg("x"), nb::arg("y"))
         .def_rw("x", &BLPointI::x)
         .def_rw("y", &BLPointI::y)
         .def("__repr__", [](const BLPointI &self)
              { return "PointI(x=" + std::to_string(self.x) +
                       ", y=" + std::to_string(self.y) + ")"; });

     // Size
     nb::class_<BLSize>(m, "BLSize")
         .def(nb::init<double, double>(),
              nb::arg("w"), nb::arg("h"))
         .def_rw("w", &BLSize::w)
         .def_rw("h", &BLSize::h)
         .def("__repr__", [](const BLSize &self)
              { return "Size(w=" + std::to_string(self.w) +
                       ", h=" + std::to_string(self.h) + ")"; });

     // SizeI
     nb::class_<BLSizeI>(m, "BLSizeI")
         .def(nb::init<int, int>(),
              nb::arg("w"), nb::arg("h"))
         .def_rw("w", &BLSizeI::w)
         .def_rw("h", &BLSizeI::h)
         .def("__repr__", [](const BLSizeI &self)
              { return "SizeI(w=" + std::to_string(self.w) +
                       ", h=" + std::to_string(self.h) + ")"; });
}