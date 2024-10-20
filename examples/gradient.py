import blend2d
import numpy as np
from skimage.io import imsave

if __name__ == "__main__":
    array = np.empty((256, 256, 4), dtype=np.uint8)
    image = blend2d.Image(array)
    context = blend2d.Context(image)

    gradient = blend2d.LinearGradient(0, 0, 256, 256)
    gradient.extend_mode = blend2d.ExtendMode.PAD
    gradient.add_stop(0.0, (1.0, 1.0, 1.0))
    gradient.add_stop(0.5, (1.0, 0.69, 0.0))
    gradient.add_stop(1.0, (1.0, 0.0, 0.0))

    context.set_fill_style(gradient)
    context.fill_all()

    circle = blend2d.Path()
    circle.add_ellipse(128, 128, 64, 64)

    context.set_comp_op(blend2d.CompOp.EXCLUSION)
    context.set_fill_style((0.0, 1.0, 1.0))
    context.fill_path((0, 0), circle)

    imsave("gradient.png", array)
