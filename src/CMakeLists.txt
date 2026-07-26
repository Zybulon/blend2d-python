if( NOT NUMPY_INCLUDE_DIR )
  find_package( PythonInterp )
  execute_process(
    COMMAND ${PYTHON_EXECUTABLE} -c "import numpy; print(numpy.get_include())"
    OUTPUT_VARIABLE _numpy_include
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )
  find_path( NUMPY_INCLUDE_DIR numpy/arrayobject.h
    HINTS ${_numpy_include} )
endif()

include_directories( ${NUMPY_INCLUDE_DIR} )

set(BLEND2D_NANOBIND_SOURCES
  nanobind_main.cpp
  nanobind_enums.cpp
  nanobind_geometry.cpp
  nanobind_array.cpp
  nanobind_image.cpp
  nanobind_font.cpp
  nanobind_path.cpp
  nanobind_gradient.cpp
  nanobind_pattern.cpp
  nanobind_context.cpp
  nanobind_misc.cpp
  nanobind_pixel_convert.cpp
)

nanobind_add_module(
  ${BLEND2DPY_TARGET_NAME}
  NB_STATIC  
  ${BLEND2D_NANOBIND_SOURCES}
)

# Set the output name to _capi (without ABI tags)
# Python can import this as "import _capi" or "from . import _capi"
set_target_properties(${BLEND2DPY_TARGET_NAME} PROPERTIES OUTPUT_NAME "_capi")

if(WIN32)
  # Windows Python modules use .pyd extension instead of .so
  set_target_properties(${BLEND2DPY_TARGET_NAME} PROPERTIES SUFFIX ".pyd")
endif()

# Debug: print what we're building
message(STATUS "Building Python extension: ${BLEND2DPY_TARGET_NAME}")
message(STATUS "Output name will be: _capi")
get_target_property(TARGET_SUFFIX ${BLEND2DPY_TARGET_NAME} SUFFIX)
message(STATUS "File suffix: ${TARGET_SUFFIX}")

target_include_directories( ${BLEND2DPY_TARGET_NAME} BEFORE PRIVATE 
  ${BLEND2D_INCLUDE_DIR} 
  ${Python_NumPy_INCLUDE_DIRS}
  ${NANOBIND_DIR}/include
)
target_link_libraries( ${BLEND2DPY_TARGET_NAME} PRIVATE ${BLEND2D_LIBS} )
