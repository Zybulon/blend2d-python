#include "nanobind_common.h"

void register_array(nb::module_ &m)
{
     // BLArray - uint8_t
     nb::class_<BLArray<uint8_t>>(m, "BLArray")
         .def(nb::init<>()) // Default constructor
         .def("__del__", [](BLArray<uint8_t> *self)
              { self->reset(); })
         .def("size", [](const BLArray<uint8_t> &self)
              { return self.size(); })
         .def("capacity", [](const BLArray<uint8_t> &self)
              { return self.capacity(); })
         .def("clear", [](BLArray<uint8_t> &self)
              { self.clear(); })
         .def("shrink", [](BLArray<uint8_t> &self)
              { self.shrink(); })
         .def("reserve", [](BLArray<uint8_t> &self, size_t n)
              { self.reserve(n); }, nb::arg("n"))
         .def("reset", [](BLArray<uint8_t> &self)
              { self.reset(); })
         .def("from_numpy", [](nb::ndarray<nb::numpy, uint8_t> array)
              {
            if (array.ndim() > 1) {
                throw nb::value_error("Only 1D arrays supported");
            }

            auto* result = new BLArray<uint8_t>();
            result->reserve(array.shape(0));
            
            for (size_t i = 0; i < array.shape(0); i++) {
                result->append(array.data()[i]);
            }
            
            return result; }, nb::rv_policy::take_ownership);

     // BLArray - uint16_t
     nb::class_<BLArray<uint16_t>>(m, "BLArray16")
         .def(nb::init<>()) // Default constructor
         .def("__del__", [](BLArray<uint16_t> *self)
              { self->reset(); })
         .def("size", [](const BLArray<uint16_t> &self)
              { return self.size(); })
         .def("capacity", [](const BLArray<uint16_t> &self)
              { return self.capacity(); })
         .def("clear", [](BLArray<uint16_t> &self)
              { self.clear(); })
         .def("shrink", [](BLArray<uint16_t> &self)
              { self.shrink(); })
         .def("reserve", [](BLArray<uint16_t> &self, size_t n)
              { self.reserve(n); }, nb::arg("n"))
         .def("reset", [](BLArray<uint16_t> &self)
              { self.reset(); })
         .def_static("from_numpy", [](nb::ndarray<nb::numpy, uint16_t> array)
                     {
            if (array.ndim() > 1) {
                throw nb::value_error("Only 1D arrays supported");
            }

            auto* result = new BLArray<uint16_t>();
            result->reserve(array.shape(0));
            
            for (size_t i = 0; i < array.shape(0); i++) {
                result->append(array.data()[i]);
            }
            
            return result; }, nb::rv_policy::take_ownership);

     // BLArray - uint32_t
     nb::class_<BLArray<uint32_t>>(m, "BLArray32")
         .def(nb::init<>()) // Default constructor
         .def("__del__", [](BLArray<uint32_t> *self)
              { self->reset(); })
         .def("size", [](const BLArray<uint32_t> &self)
              { return self.size(); })
         .def("capacity", [](const BLArray<uint32_t> &self)
              { return self.capacity(); })
         .def("clear", [](BLArray<uint32_t> &self)
              { self.clear(); })
         .def("shrink", [](BLArray<uint32_t> &self)
              { self.shrink(); })
         .def("reserve", [](BLArray<uint32_t> &self, size_t n)
              { self.reserve(n); }, nb::arg("n"))
         .def("reset", [](BLArray<uint32_t> &self)
              { self.reset(); })
         .def_static("from_numpy", [](nb::ndarray<nb::numpy, uint32_t> array)
                     {
            if (array.ndim() > 1) {
                throw nb::value_error("Only 1D arrays supported");
            }

            auto* result = new BLArray<uint32_t>();
            result->reserve(array.shape(0));
            
            for (size_t i = 0; i < array.shape(0); i++) {
                result->append(array.data()[i]);
            }
            
            return result; }, nb::rv_policy::take_ownership);

     // BLArray - float
     nb::class_<BLArray<float>>(m, "BLArrayFloat")
         .def(nb::init<>()) // Default constructor
         .def("__del__", [](BLArray<float> *self)
              { self->reset(); })
         .def("size", [](const BLArray<float> &self)
              { return self.size(); })
         .def("capacity", [](const BLArray<float> &self)
              { return self.capacity(); })
         .def("clear", [](BLArray<float> &self)
              { self.clear(); })
         .def("shrink", [](BLArray<float> &self)
              { self.shrink(); })
         .def("reserve", [](BLArray<float> &self, size_t n)
              { self.reserve(n); }, nb::arg("n"))
         .def("reset", [](BLArray<float> &self)
              { self.reset(); })
         .def_static("from_numpy", [](nb::ndarray<nb::numpy, float> array)
                     {
            if (array.ndim() > 1) {
                throw nb::value_error("Only 1D arrays supported");
            }

            auto* result = new BLArray<float>();
            result->reserve(array.shape(0));
            
            for (size_t i = 0; i < array.shape(0); i++) {
                result->append(array.data()[i]);
            }
            
            return result; }, nb::rv_policy::take_ownership);

     // BLArray - double
     nb::class_<BLArray<double>>(m, "BLArrayDouble")
         .def(nb::init<>()) // Default constructor
         .def("__del__", [](BLArray<double> *self)
              { self->reset(); })
         .def("size", [](const BLArray<double> &self)
              { return self.size(); })
         .def("capacity", [](const BLArray<double> &self)
              { return self.capacity(); })
         .def("clear", [](BLArray<double> &self)
              { self.clear(); })
         .def("shrink", [](BLArray<double> &self)
              { self.shrink(); })
         .def("reserve", [](BLArray<double> &self, size_t n)
              { self.reserve(n); }, nb::arg("n"))
         .def("reset", [](BLArray<double> &self)
              { self.reset(); })
         .def_static("from_numpy", [](nb::ndarray<nb::numpy, double> array)
                     {
            if (array.ndim() > 1) {
                throw nb::value_error("Only 1D arrays supported");
            }

            auto* result = new BLArray<double>();
            result->reserve(array.shape(0));
            
            for (size_t i = 0; i < array.shape(0); i++) {
                result->append(array.data()[i]);
            }
            
            return result; }, nb::rv_policy::take_ownership);
}