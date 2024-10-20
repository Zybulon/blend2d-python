import blend2d
import numpy as np
from skimage.color import hsv2rgb
from skimage.io import imsave

if __name__ == "__main__":
    array = np.empty((500, 500, 4), dtype=np.uint8)
    image = blend2d.Image(array)
    canvas = blend2d.Context(image)

    canvas.clear_all()
    canvas.set_stroke_width(20.0)

    path = blend2d.Path()
    path.quadric_to(25, 25, 150, 0)
    path.quadric_to(275, -25, 300, 0)

    caps = {
        blend2d.StrokeCap.CAP_BUTT,
        blend2d.StrokeCap.CAP_SQUARE,
        blend2d.StrokeCap.CAP_ROUND,
        blend2d.StrokeCap.CAP_ROUND_REV,
        blend2d.StrokeCap.CAP_TRIANGLE,
        blend2d.StrokeCap.CAP_TRIANGLE_REV,
    }

    for i, cap in enumerate(caps):
        with canvas:
            color = hsv2rgb([[i / len(caps), 0.75, 0.75]])[0]
            canvas.set_stroke_style(color)
            canvas.set_stroke_caps(cap)
            canvas.stroke_path((100, (i + 1) * 75), path)

    imsave("lines.png", array)
