#include "nanobind_common.h"

void register_pattern(nb::module_ &m)
{
     nb::class_<BLPattern>(m, "BLPattern")
         .def(nb::init<>())
         .def("__init__", [](BLPattern &self, const BLImage &image, const BLRectI &area, BLExtendMode mode, const BLMatrix2D &matrix)
              { self.create(image, area, mode, matrix); }, nb::arg("image"), nb::arg("area"), nb::arg("extend_mode") = BL_EXTEND_MODE_REPEAT, nb::arg("matrix") = BLMatrix2D())
         .def("__del__", [](BLPattern *self)
              { self->reset(); })
         .def_prop_ro("image", [](const BLPattern &self)
                      { return self.getImage(); })
         .def_prop_ro("area", [](const BLPattern &self)
                      { return self.area(); })
         .def_prop_ro("extend_mode", [](const BLPattern &self)
                      { return self.extendMode(); })
         .def_prop_rw("matrix", [](const BLPattern &self)
                      { return self.transform(); }, [](BLPattern &self, const BLMatrix2D &matrix)
                      { return self.setTransform(matrix); })
         .def("reset", [](BLPattern &self)
              { self.reset(); })
         .def("apply_transform_op", [](BLPattern &self, BLTransformOp op, const nb::list &values)
              {
            BLArray<double> valueArray;
            for (size_t i = 0; i < values.size(); i++) {
                valueArray.append(nb::cast<double>(values[i]));
            }
            return self._applyTransformOp(op, valueArray.data()); }, nb::arg("op"), nb::arg("values"));
}