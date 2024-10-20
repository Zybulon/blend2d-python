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

# BLContext
# BLResult blContextInit(BLContextCore* self)
# BLResult blContextInitAs(BLContextCore* self, BLImageCore* image, const BLContextCreateInfo* options)
# BLResult blContextDestroy(BLContextCore* self)
# BLResult blContextReset(BLContextCore* self)
# BLResult blContextAssignMove(BLContextCore* self, BLContextCore* other)
# BLResult blContextAssignWeak(BLContextCore* self, const BLContextCore* other)
# uint32_t blContextGetType(const BLContextCore* self)
# BLResult blContextGetTargetSize(const BLContextCore* self, BLSize* targetSizeOut)
# BLImageCore* blContextGetTargetImage(const BLContextCore* self)
# BLResult blContextBegin(BLContextCore* self, BLImageCore* image, const BLContextCreateInfo* options)
# BLResult blContextEnd(BLContextCore* self)
# BLResult blContextFlush(BLContextCore* self, uint32_t flags)
# BLResult blContextQueryProperty(const BLContextCore* self, uint32_t propertyId, void* valueOut)
# BLResult blContextSave(BLContextCore* self, BLContextCookie* cookie)
# BLResult blContextRestore(BLContextCore* self, const BLContextCookie* cookie)
# BLResult blContextGetMetaTransform(const BLContextCore* self, BLMatrix2D* m)
# BLResult blContextGetUserTransform(const BLContextCore* self, BLMatrix2D* m)
# BLResult blContextUserToMeta(BLContextCore* self)
# BLResult blContextApplyTransformOp(BLContextCore* self, uint32_t opType, const void* opData)
# BLResult blContextSetHint(BLContextCore* self, uint32_t hintType, uint32_t value)
# BLResult blContextSetHints(BLContextCore* self, const BLContextHints* hints)
# BLResult blContextSetFlattenMode(BLContextCore* self, uint32_t mode)
# BLResult blContextSetFlattenTolerance(BLContextCore* self, double tolerance)
# BLResult blContextSetApproximationOptions(BLContextCore* self, const BLApproximationOptions* options)
# BLResult blContextSetCompOp(BLContextCore* self, uint32_t compOp)
# BLResult blContextSetGlobalAlpha(BLContextCore* self, double alpha)
# BLResult blContextSetFillAlpha(BLContextCore* self, double alpha)
# BLResult blContextGetFillStyle(const BLContextCore* self, BLStyleCore* styleOut)
# BLResult blContextSetFillStyle(BLContextCore* self, const BLUnknown* style)
# BLResult blContextSetFillStyleRgba(BLContextCore* self, const BLRgba* rgba)
# BLResult blContextSetFillStyleRgba32(BLContextCore* self, uint32_t rgba32)
# BLResult blContextSetFillStyleRgba64(BLContextCore* self, uint64_t rgba64)
# BLResult blContextSetFillRule(BLContextCore* self, uint32_t fillRule)
# BLResult blContextSetStrokeAlpha(BLContextCore* self, double alpha)
# BLResult blContextGetStrokeStyle(const BLContextCore* self, BLStyleCore* styleOut)
# BLResult blContextSetStrokeStyle(BLContextCore* self, const BLStyleCore* style)
# BLResult blContextSetStrokeStyleRgba(BLContextCore* self, const BLRgba* rgba)
# BLResult blContextSetStrokeStyleRgba32(BLContextCore* self, uint32_t rgba32)
# BLResult blContextSetStrokeStyleRgba64(BLContextCore* self, uint64_t rgba64)
# BLResult blContextSetStrokeStyleObject(BLContextCore* self, const void* object)
# BLResult blContextSetStrokeWidth(BLContextCore* self, double width)
# BLResult blContextSetStrokeMiterLimit(BLContextCore* self, double miterLimit)
# BLResult blContextSetStrokeCap(BLContextCore* self, uint32_t position, uint32_t strokeCap)
# BLResult blContextSetStrokeCaps(BLContextCore* self, uint32_t strokeCap)
# BLResult blContextSetStrokeJoin(BLContextCore* self, uint32_t strokeJoin)
# BLResult blContextSetStrokeDashOffset(BLContextCore* self, double dashOffset)
# BLResult blContextSetStrokeDashArray(BLContextCore* self, const BLArrayCore* dashArray)
# BLResult blContextSetStrokeTransformOrder(BLContextCore* self, uint32_t transformOrder)
# BLResult blContextGetStrokeOptions(const BLContextCore* self, BLStrokeOptionsCore* options)
# BLResult blContextSetStrokeOptions(BLContextCore* self, const BLStrokeOptionsCore* options)
# BLResult blContextClipToRectI(BLContextCore* self, const BLRectI* rect)
# BLResult blContextClipToRectD(BLContextCore* self, const BLRect* rect)
# BLResult blContextRestoreClipping(BLContextCore* self)
# BLResult blContextClearAll(BLContextCore* self)
# BLResult blContextClearRectI(BLContextCore* self, const BLRectI* rect)
# BLResult blContextClearRectD(BLContextCore* self, const BLRect* rect)
# BLResult blContextFillAll(BLContextCore* self)
# BLResult blContextFillRectI(BLContextCore* self, const BLRectI* rect)
# BLResult blContextFillRectD(BLContextCore* self, const BLRect* rect)
# BLResult blContextFillPathD(BLContextCore* self, const BLPathCore* path)
# BLResult blContextFillGeometry(BLContextCore* self, uint32_t geometryType, const void* geometryData)
# BLResult blContextFillUtf8TextI(BLContextCore* self, const BLPointI* pt, const BLFontCore* font, const void* text, size_t size)
# BLResult blContextFillUtf8TextD(BLContextCore* self, const BLPoint* pt, const BLFontCore* font, const void* text, size_t size)
# BLResult blContextFillGlyphRunI(BLContextCore* self, const BLPointI* pt, const BLFontCore* font, const BLGlyphRun* glyphRun)
# BLResult blContextFillGlyphRunD(BLContextCore* self, const BLPoint* pt, const BLFontCore* font, const BLGlyphRun* glyphRun)
# BLResult blContextStrokeRectI(BLContextCore* self, const BLRectI* rect)
# BLResult blContextStrokeRectD(BLContextCore* self, const BLRect* rect)
# BLResult blContextStrokePathD(BLContextCore* self, const BLPoint* origin, const BLPathCore* path)
# BLResult blContextStrokeGeometry(BLContextCore* self, uint32_t geometryType, const void* geometryData)
# BLResult blContextStrokeUtf8TextI(BLContextCore* self, const BLPointI* pt, const BLFontCore* font, const void* text)
# BLResult blContextStrokeUtf8TextD(BLContextCore* self, const BLPoint* pt, const BLFontCore* font, const void* text)
# BLResult blContextStrokeGlyphRunI(BLContextCore* self, const BLPointI* pt, const BLFontCore* font, const BLGlyphRun* glyphRun)
# BLResult blContextStrokeGlyphRunD(BLContextCore* self, const BLPoint* pt, const BLFontCore* font, const BLGlyphRun* glyphRun)
# BLResult blContextBlitImageI(BLContextCore* self, const BLPointI* pt, const BLImageCore* img, const BLRectI* imgArea)
# BLResult blContextBlitImageD(BLContextCore* self, const BLPoint* pt, const BLImageCore* img, const BLRectI* imgArea)
# BLResult blContextBlitScaledImageI(BLContextCore* self, const BLRectI* rect, const BLImageCore* img, const BLRectI* imgArea)
# BLResult blContextBlitScaledImageD(BLContextCore* self, const BLRect* rect, const BLImageCore* img, const BLRectI* imgArea)

cdef class Context:
    cdef _capi.BLContextCore _self
    cdef _capi.BLContextCookie _state_cookie
    cdef object _image_ref

    def __cinit__(self, Image image):
        _capi.blContextInitAs(&self._self, &image._self, NULL)
        self._image_ref = image

    def __dealloc__(self):
        _capi.blContextDestroy(&self._self)
        self._image_ref = None

    def __enter__(self):
        # Push the state when entering a context
        self.save()

    def __exit__(self, *args):
        # Pop the state when exiting
        self.restore()

    def clear_all(self):
        """ Clear everything
        """
        _capi.blContextClearAll(&self._self)

    def fill_all(self):
        """ Fill the entire image with the fill style
        """
        _capi.blContextFillAll(&self._self)

    def flush(self):
        """ Flush any pending drawing operations.
        """
        _capi.blContextFlush(&self._self, 0)

    def restore(self):
        """ Pop the current state off the stack.
        """
        _capi.blContextRestore(&self._self, NULL)

    def save(self):
        """ Push the current state onto the stack.
        """
        # XXX: It's not clear to me how the BLContextCookie argument is meant
        # to be used, so I'm leaving it out for now.
        _capi.blContextSave(&self._self, NULL)

    def clip_to_rect(self, Rect clip):
        """clip_to_rect(rect)
        """
        _capi.blContextClipToRectD(&self._self, &clip._self)

    def restore_clipping(self):
        _capi.blContextRestoreClipping(&self._self)

    def reset_matrix(self):
        """reset_matrix()
        Resets to the identity transform.
        """
        _capi.blContextApplyTransformOp(&self._self, _capi.BL_TRANSFORM_OP_RESET, NULL)

    def meta_matrix(self):
        """meta_matrix()
        Return the meta matrix
        """
        cdef Matrix2D mat = Matrix2D()
        _capi.blContextGetMetaTransform(&self._self, &mat._self)
        return mat

    def user_matrix(self):
        """user_matrix()
        Return the user matrix
        """
        cdef Matrix2D mat = Matrix2D()
        _capi.blContextGetUserTransform(&self._self, &mat._self)
        return mat

    def user_to_meta(self):
        """user_to_meta()
        Store the result of combining the current `MetaMatrix` and `UserMatrix`
        to `MetaMatrix` and reset `UserMatrix` to identity as shown below:

            MetaMatrix = MetaMatrix x UserMatrix
            UserMatrix = Identity

        Please note that this operation is irreversible. The only way to restore
        both matrices to the state before the call to `user_to_meta()` is to use
        `save()` and `restore()` functions.
        """
        _capi.blContextUserToMeta(&self._self)

    def scale(self, double x, double y):
        """scale(x, y)
        Apply a scaling to the transform

        :param x: The scale factor in X
        :param y: The scale factor in Y
        """
        cdef double *data = [x, y]
        _capi.blContextApplyTransformOp(&self._self, _capi.BL_TRANSFORM_OP_SCALE, data)

    def rotate(self, double angle):
        """rotate(angle)
        Apply a rotation to the transform.

        :param angle: The desired rotation in radians.
        """
        _capi.blContextApplyTransformOp(&self._self, _capi.BL_TRANSFORM_OP_ROTATE, &angle)

    def skew(self, double x, double y):
        """skew(x, y)
        Apply a skew to the transform.

        :param x: The skew factor in X
        :param y: The skew factor in Y
        """
        cdef double *data = [x, y]
        _capi.blContextApplyTransformOp(&self._self, _capi.BL_TRANSFORM_OP_SKEW, data)

    def translate(self, double x, double y):
        """translate(x, y)
        Apply a translation to the transform.

        :param x: The translation in X
        :param y: The translation in Y
        """
        cdef double *data = [x, y]
        _capi.blContextApplyTransformOp(&self._self, _capi.BL_TRANSFORM_OP_TRANSLATE, data)

    def transform(self, Matrix2D mat):
        """transform(matrix)
        Pre-multiply the transform by another matrix

        :param matrix: A Matrix2D instance
        """
        _capi.blContextApplyTransformOp(&self._self, _capi.BL_TRANSFORM_OP_TRANSFORM, &mat._self)

    def post_transform(self, Matrix2D mat):
        """post_transform(matrix)
        Post-multiply the transform by another matrix

        :param matrix: A Matrix2D instance
        """
        _capi.blContextApplyTransformOp(&self._self, _capi.BL_TRANSFORM_OP_POST_TRANSFORM, &mat._self)

    def set_alpha(self, float alpha):
        _capi.blContextSetGlobalAlpha(&self._self, alpha)

    def set_comp_op(self, CompOp op):
        _capi.blContextSetCompOp(&self._self, op)

    cdef _apply_gradient_fill(self, Gradient style):
        _capi.blContextSetFillStyle(&self._self, &style._self)

    cdef _apply_gradient_stroke(self, Gradient style):
        _capi.blContextSetStrokeStyle(&self._self, &style._self)

    cdef _apply_pattern_fill(self, Pattern style):
        _capi.blContextSetFillStyle(&self._self, &style._self)

    cdef _apply_pattern_stroke(self, Pattern style):
        _capi.blContextSetStrokeStyle(&self._self, &style._self)

    def set_fill_style(self, style):
        if isinstance(style, Gradient):
            self._apply_gradient_fill(style)
            return
        elif isinstance(style, Pattern):
            self._apply_pattern_fill(style)
            return

        # Assume a plain color style
        cdef uint32_t packed = _get_rgba32_value(style)
        _capi.blContextSetFillStyleRgba32(&self._self, packed)

    def set_stroke_cap(self, StrokeCapPosition position, StrokeCap cap):
        _capi.blContextSetStrokeCap(&self._self, position, cap)

    def set_stroke_caps(self, StrokeCap cap):
        _capi.blContextSetStrokeCaps(&self._self, cap)

    def set_stroke_dash_array(self, Array arr):
        _capi.blContextSetStrokeDashArray(&self._self, &arr._self)

    def set_stroke_dash_offset(self, double offset):
        _capi.blContextSetStrokeDashOffset(&self._self, offset)

    def set_stroke_join(self, StrokeJoin join):
        _capi.blContextSetStrokeJoin(&self._self, join)

    def set_stroke_miter_limit(self, float value):
        _capi.blContextSetStrokeMiterLimit(&self._self, value)

    def set_stroke_style(self, style):
        if isinstance(style, Gradient):
            self._apply_gradient_stroke(style)
            return
        elif isinstance(style, Pattern):
            self._apply_pattern_stroke(style)
            return

        # Assume a plain color style
        cdef uint32_t packed = _get_rgba32_value(style)
        _capi.blContextSetStrokeStyleRgba32(&self._self, packed)

    def set_stroke_width(self, float width):
        _capi.blContextSetStrokeWidth(&self._self, width)

    def blit_image(self, origin, Image img, Rect img_area):
        cdef:
            _capi.BLPoint point
            _capi.BLRectI rect

        point.x = origin[0]; point.y = origin[1]
        rect.x = <int>img_area._self.x; rect.y = <int>img_area._self.y
        rect.w = <int>img_area._self.w; rect.h = <int>img_area._self.h
        _capi.blContextBlitImageD(&self._self, &point, &img._self, &rect)

    def blit_scaled_image(self, Rect rect, Image img, Rect img_area):
        cdef:
            _capi.BLRectI dst_rect

        dst_rect.x = <int>img_area._self.x; dst_rect.y = <int>img_area._self.y
        dst_rect.w = <int>img_area._self.w; dst_rect.h = <int>img_area._self.h
        _capi.blContextBlitScaledImageD(&self._self, &rect._self, &img._self, &dst_rect)

    def fill_all(self):
        _capi.blContextFillAll(&self._self)

    def fill_rect(self, Rect rect):
        _capi.blContextFillRectD(&self._self, &rect._self)

    def fill_path(self, origin, Path path):
        cdef:
            _capi.BLPoint point
            
        point.x = origin[0]
        point.y = origin[1]
        _capi.blContextFillPathD(&self._self, &point, &path._self)
        
    def fill_text(self, origin, Font font, text):
        cdef:
            bytes utf8_text = _utf8_string(text)
            char * c_text = utf8_text
            size_t size = len(utf8_text)
            _capi.BLPoint point

        point.x = origin[0]
        point.y = origin[1]
        _capi.blContextFillUtf8TextD(&self._self, &point, &font._self, c_text, size)

    def stroke_rect(self, Rect rect):
        _capi.blContextStrokeRectD(&self._self, &rect._self)

    def stroke_path(self, origin, Path path):
        cdef:
            _capi.BLPoint point
            
        point.x = origin[0]
        point.y = origin[1]
        _capi.blContextStrokePathD(&self._self, &point, &path._self)

    def stroke_text(self, origin, Font font, text):
        cdef:
            bytes utf8_text = _utf8_string(text)
            char * c_text = utf8_text
            size_t size = len(utf8_text)
            _capi.BLPoint point

        point.x = origin[0]
        point.y = origin[1]
        _capi.blContextStrokeUtf8TextD(
            &self._self, &point, &font._self,
            c_text, size)
