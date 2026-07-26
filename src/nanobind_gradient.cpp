#include "nanobind_common.h"

void register_gradient(nb::module_ &m)
{
     // Base Gradient class
     auto gradient = nb::class_<BLGradient>(m, "BLGradient")
                         .def(nb::init<>())
                         .def("__del__", [](BLGradient *self)
                              { self->reset(); })
                         .def_prop_rw("extend_mode", [](const BLGradient &self)
                                      { return self.extendMode(); }, [](BLGradient &self, BLExtendMode value)
                                      { self.setExtendMode(value); })
                         .def("add_stop", [](BLGradient &self, double offset, const nb::tuple &color)
                              {
            uint32_t packed = _get_rgba32_value(color);
            BLRgba32 rgba32(packed);
            self.addStop(offset, rgba32); }, nb::arg("offset"), nb::arg("color"))
                         .def("shrink", [](BLGradient &self)
                              { self.shrink(); })
                         .def("reserve", [](BLGradient &self, size_t n)
                              { self.reserve(n); }, nb::arg("n"))
                         .def_prop_ro("type", [](const BLGradient &self)
                                      { return self.type(); })
                         .def("reset_stops", [](BLGradient &self)
                              { self.resetStops(); })
                         .def("remove_stop", [](BLGradient &self, size_t index)
                              { self.removeStop(index); }, nb::arg("index"))
                         .def("remove_stops_by_offset", [](BLGradient &self, double offsetMin, double offsetMax)
                              { self.removeStopsByOffset(offsetMin, offsetMax); }, nb::arg("offsetMin"), nb::arg("offsetMax"))
                         .def("value", [](const BLGradient &self, size_t index)
                              { return self.value(index); }, nb::arg("index"))
                         .def("set_value", [](BLGradient &self, size_t index, double value)
                              { self.setValue(index, value); }, nb::arg("index"), nb::arg("value"))
                         .def("set_values", [](BLGradient &self, size_t index, const nb::ndarray<nb::numpy, double> &values)
                              {
            if (values.ndim() != 1) {
                throw nb::value_error("Values must be a 1D array");
            }
            self.setValues(index, values.data(), values.shape(0)); }, nb::arg("index"), nb::arg("values"))
                         .def("transform", [](BLGradient &self, const BLMatrix2D &matrix)
                              { self.applyTransform(matrix); }, nb::arg("matrix"))
                         .def("set_transform", [](BLGradient &self, const BLMatrix2D &matrix)
                              { self.setTransform(matrix); }, nb::arg("matrix"))
                         .def("reset_transform", [](BLGradient &self)
                              { self.resetTransform(); });

     // Conical Gradient
     m.def("create_conical_gradient", [](double x, double y, double angle)
           {
        BLGradient* gradient = new BLGradient();
        gradient->reset();
        gradient->setType(BL_GRADIENT_TYPE_CONIC);
        
        double values[3] = {x, y, angle};
        gradient->setValues(0, values, 3);
        
        return gradient; }, nb::arg("x"), nb::arg("y"), nb::arg("angle"), nb::rv_policy::take_ownership);

     // Linear Gradient
     m.def("create_linear_gradient", [](double x0, double y0, double x1, double y1)
           {
        BLGradient* gradient = new BLGradient();
        gradient->reset();
        gradient->setType(BL_GRADIENT_TYPE_LINEAR);
        
        double values[4] = {x0, y0, x1, y1};
        gradient->setValues(0, values, 4);
        
        return gradient; }, nb::arg("x0"), nb::arg("y0"), nb::arg("x1"), nb::arg("y1"), nb::rv_policy::take_ownership);

     // Radial Gradient
     m.def("create_radial_gradient", [](double x0, double y0, double x1, double y1, double r)
           {
        BLGradient* gradient = new BLGradient();
        gradient->reset();
        gradient->setType(BL_GRADIENT_TYPE_RADIAL);
        
        double values[5] = {x0, y0, x1, y1, r};
        gradient->setValues(0, values, 5);
        
        return gradient; }, nb::arg("x0"), nb::arg("y0"), nb::arg("x1"), nb::arg("y1"), nb::arg("r"), nb::rv_policy::take_ownership);
}