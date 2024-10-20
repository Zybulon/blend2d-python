# The MIT License (MIT)
#
# Copyright (c) 2019 John Wiggins
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# BLImage
# BLResult blImageInit(BLImageCore* self)
# BLResult blImageInitMove(BLImageCore* self, BLImageCore* other)
# BLResult blImageInitWeak(BLImageCore* self, const BLImageCore* other)
# BLResult blImageInitAs(BLImageCore* self, int w, int h, BLFormat format)
# BLResult blImageInitAsFromData(BLImageCore* self, int w, int h, BLFormat format, void* pixelData, intptr_t stride, BLDataAccessFlags accessFlags, BLDestroyExternalDataFunc destroyFunc, void* userData)
# BLResult blImageDestroy(BLImageCore* self)
# BLResult blImageReset(BLImageCore* self)
# BLResult blImageAssignMove(BLImageCore* self, BLImageCore* other)
# BLResult blImageAssignWeak(BLImageCore* self, const BLImageCore* other)
# BLResult blImageAssignDeep(BLImageCore* self, const BLImageCore* other)
# BLResult blImageCreate(BLImageCore* self, int w, int h, BLFormat format)
# BLResult blImageCreateFromData(BLImageCore* self, int w, int h, BLFormat format, void* pixelData, intptr_t stride, BLDataAccessFlags accessFlags, BLDestroyExternalDataFunc destroyFunc, void* userData)
# BLResult blImageGetData(const BLImageCore* self, BLImageData* dataOut)
# BLResult blImageMakeMutable(BLImageCore* self, BLImageData* dataOut)
# BLResult blImageConvert(BLImageCore* self, BLFormat format)
# bool blImageEquals(const BLImageCore* a, const BLImageCore* b)
# BLResult blImageScale(BLImageCore* dst, const BLImageCore* src, const BLSizeI* size, BLImageScaleFilter filter)
# BLResult blImageReadFromFile(BLImageCore* self, const char* fileName, const BLArrayCore* codecs)
# BLResult blImageReadFromData(BLImageCore* self, const void* data, size_t size, const BLArrayCore* codecs)
# BLResult blImageWriteToFile(const BLImageCore* self, const char* fileName, const BLImageCodecCore* codec)
# BLResult blImageWriteToData(const BLImageCore* self, BLArrayCore* dst, const BLImageCodecCore* codec)

cdef class Image:
    cdef _capi.BLImageCore _self
    cdef object _array_ref

    def __cinit__(self, char [:, :, :] array):
        cdef int w, h
        h, w = array.shape[0], array.shape[1]

        _capi.blImageInitAsFromData(
            &self._self,
            w, h,
            _capi.BL_FORMAT_XRGB32,
            <char*>&array[0][0][0],
            array.strides[0],
            _capi.BL_DATA_ACCESS_RW,
            _destroy_array_data, NULL
        )
        self._array_ref = array

    def __dealloc__(self):
        _capi.blImageDestroy(&self._self)
        self._array_ref = None
