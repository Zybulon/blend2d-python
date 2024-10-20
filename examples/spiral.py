from __future__ import division
import argparse

import numpy as np
from skimage.color import hsv2rgb
from skimage.io import imsave

import blend2d

# Some constants to fiddle with
CENTER_RADIUS = 25
CIRCLE_COUNT = 60
CIRCLE_SIZE = 20


def compute_offsets(maxoffset):
    offset = CENTER_RADIUS
    radius = 0
    offsets = [offset]
    while offset < maxoffset:
        radius = np.pi * offset / CIRCLE_COUNT

        # Estimate how far to push out the next line
        newradius = np.pi * (offset + radius * 2) / CIRCLE_COUNT
        offset += radius + newradius
        offsets.append(offset)
    return offsets


def spiral(size, hue, sat, val):
    array = np.empty((size[1], size[0], 4), dtype=np.uint8)
    image = blend2d.Image(array)
    canvas = blend2d.Context(image)
    circle = blend2d.Path()
    circle.add_ellipse(0, 0, CIRCLE_SIZE, CIRCLE_SIZE)

    divisions = np.linspace(0, 2 * np.pi, CIRCLE_COUNT, endpoint=False)
    centers = np.stack((np.cos(divisions), np.sin(divisions)), axis=1)
    offsets = compute_offsets(np.sqrt(size[0] ** 2 + size[1] ** 2) / 2)
    color_count = len(offsets)

    hsv = np.ones((color_count, 1, 3))
    hsv[:, 0, 0] = np.linspace(hue[0], hue[1], color_count, endpoint=False)
    hsv[:, 0, 1] = np.linspace(sat[0], sat[1], color_count, endpoint=False)
    hsv[:, 0, 2] = np.linspace(val[0], val[1], color_count, endpoint=False)
    spectrum = hsv2rgb(hsv).reshape(color_count, 3)

    canvas.clear_all()  # fill with black
    for idx, offset in enumerate(offsets):
        canvas.set_fill_style(spectrum[idx])
        radius = np.pi * offset / CIRCLE_COUNT
        scale = radius / CIRCLE_SIZE
        for i in range(CIRCLE_COUNT):
            if ((idx + i) % 2) == 0:
                continue
            canvas.reset_matrix()
            canvas.translate(
                size[0] / 2 + offset * centers[i, 0],
                size[1] / 2 + offset * centers[i, 1],
            )
            canvas.scale(scale, scale)
            canvas.fill_path((0, 0), circle)

    # BGRA -> RGBA
    array[:, :, [0, 1, 2]] = array[:, :, [2, 1, 0]]
    imsave("spiral.png", array)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-z", "--size", nargs=2, default=[1000, 1000])
    p.add_argument("-u", "--hue", nargs=2, default=[0.0, 1.0])
    p.add_argument("-s", "--sat", nargs=2, default=[0.95, 0.95])
    p.add_argument("-v", "--val", nargs=2, default=[0.85, 0.85])
    args = p.parse_args()
    size = tuple(int(a) for a in args.size)
    hue = tuple(float(a) for a in args.hue)
    sat = tuple(float(a) for a in args.sat)
    val = tuple(float(a) for a in args.val)
    spiral(size, hue, sat, val)
