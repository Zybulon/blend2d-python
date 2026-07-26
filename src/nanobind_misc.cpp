#include "nanobind_common.h"

using namespace nanobind::literals;

void register_misc(nb::module_ &m)
{
      // Version information
      // Hardcoded version since BL_VERSION_* constants are not defined in the header
      m.attr("BL_VERSION") = nb::make_tuple(0, 8, 0);

      // Constants
      m.attr("PI") = 3.14159265358979323846;
      m.attr("HALF_PI") = 1.57079632679489661923;
      m.attr("TWO_PI") = 6.28318530717958647692;

      // Runtime functions
      m.def("get_runtime_build_info", []()
            {
        BLRuntimeBuildInfo info;
        blRuntimeQueryInfo(BL_RUNTIME_INFO_TYPE_BUILD, &info);

        nb::dict result;
        result["compiler"] = nb::str(info.compilerInfo, strlen(info.compilerInfo));
        
        nb::dict features;
        features["BASELINE"] = info.baselineCpuFeatures;
        features["ENABLED"] = info.supportedCpuFeatures;
        result["cpuFeatures"] = features;

        // Only add valid members to the optimizations dictionary
        nb::dict optimizations;
        result["optimizations"] = optimizations;

        return result; });

      m.def("get_runtime_memory_info", []()
            {
        BLRuntimeResourceInfo info;
        blRuntimeQueryInfo(BL_RUNTIME_INFO_TYPE_RESOURCE, &info);

        nb::dict result;
        result["vmUsed"] = info.vmUsed;
        result["vmReserved"] = info.vmReserved;
        result["vmOverhead"] = info.vmOverhead;
        result["vmBlockCount"] = info.vmBlockCount;
        result["dynamicPipelineCount"] = info.dynamicPipelineCount;
        
        return result; });
}