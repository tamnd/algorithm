# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/criminisi-inpainting/. The authors are listed in prov/9PPPZC.jsonl.

"""Exemplar-based inpainting of Criminisi, Perez and Toyama (2004) for one gray channel.

The image is a list of H rows of W numbers, and mask[y][x] is True for the
pixels of the target region Omega, whose values are unknown. A patch of
radius r centered at p is the square of side 2r+1 around p, cut at the
image border. The source patches are the patches that lie fully inside
the image and contain no pixel of the original Omega.

Each step computes the priority P(p) = C(p) D(p) of every pixel p on the
fill front (unfilled pixels with a filled 4-neighbor), takes the pixel of
largest priority, finds the source patch with the least sum of squared
differences over the filled pixels of its patch, and copies the source
values into the unfilled pixels of that patch. Pixels that are known at
the start never change.

Choices of this code where the paper leaves room:
- the isophote at p is the central-difference gradient of largest size
  among the filled pixels of the patch, turned by 90 degrees; a difference
  uses only filled pixels, one-sided if only one neighbor is filled;
- the front normal is the normalized central-difference gradient of the
  unfilled indicator, with values outside the image taken equal to p;
- ties in priority go to the larger confidence, then to the first pixel in
  raster order (row by row); ties in distance go to the first source patch
  in raster order of its center.

Cost: each step takes O((F + S) a) time for F front pixels, S source
patches and patch area a = (2r+1)^2, and there are at most |Omega| steps.
"""

import math
from typing import List, Optional, Sequence, Tuple

Image = List[List[float]]
Pixel = Tuple[int, int]


def patch_pixels(x: int, y: int, r: int, w: int, h: int) -> List[Pixel]:
    """The pixels of the patch of radius r at (x, y), cut at the image border, in raster order."""
    return [(qx, qy) for qy in range(max(0, y - r), min(h, y + r + 1))
            for qx in range(max(0, x - r), min(w, x + r + 1))]


def source_centers(mask: Sequence[Sequence[bool]], r: int) -> List[Pixel]:
    """Centers of the patches that lie fully inside the image and outside the original Omega."""
    h, w = len(mask), len(mask[0])
    out = []
    for y in range(r, h - r):
        for x in range(r, w - r):
            if all(not mask[qy][qx] for qx, qy in patch_pixels(x, y, r, w, h)):
                out.append((x, y))
    return out


def front(filled: Sequence[Sequence[bool]]) -> List[Pixel]:
    """Unfilled pixels with a filled 4-neighbor, in raster order."""
    h, w = len(filled), len(filled[0])
    out = []
    for y in range(h):
        for x in range(w):
            if filled[y][x]:
                continue
            for qx, qy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= qx < w and 0 <= qy < h and filled[qy][qx]:
                    out.append((x, y))
                    break
    return out


def _diff(img, filled, x, y, dx, dy):
    """Central difference of img at (x, y) along (dx, dy) over filled pixels only."""
    h, w = len(img), len(img[0])
    ax, ay, bx, by = x + dx, y + dy, x - dx, y - dy
    a = 0 <= ax < w and 0 <= ay < h and filled[ay][ax]
    b = 0 <= bx < w and 0 <= by < h and filled[by][bx]
    if a and b:
        return (img[ay][ax] - img[by][bx]) / 2
    if a:
        return img[ay][ax] - img[y][x]
    if b:
        return img[y][x] - img[by][bx]
    return 0.0


def isophote(img, filled, x: int, y: int, r: int) -> Tuple[float, float]:
    """The gradient of largest size among the filled pixels of the patch at (x, y), turned by 90 degrees."""
    h, w = len(img), len(img[0])
    best, gx, gy = -1.0, 0.0, 0.0
    for qx, qy in patch_pixels(x, y, r, w, h):
        if not filled[qy][qx]:
            continue
        ux = _diff(img, filled, qx, qy, 1, 0)
        uy = _diff(img, filled, qx, qy, 0, 1)
        if ux * ux + uy * uy > best:
            best, gx, gy = ux * ux + uy * uy, ux, uy
    return -gy, gx


def normal(filled, x: int, y: int) -> Tuple[float, float]:
    """Unit normal to the fill front at (x, y), from the gradient of the unfilled indicator."""
    h, w = len(filled), len(filled[0])

    def u(qx, qy):
        if not (0 <= qx < w and 0 <= qy < h):
            qx, qy = x, y
        return 0.0 if filled[qy][qx] else 1.0

    nx = (u(x + 1, y) - u(x - 1, y)) / 2
    ny = (u(x, y + 1) - u(x, y - 1)) / 2
    size = math.hypot(nx, ny)
    if size == 0:
        return 0.0, 0.0
    return nx / size, ny / size


def priority(img, filled, conf, x: int, y: int, r: int, alpha: float) -> Tuple[float, float, float]:
    """Return (P, C, D) for the front pixel (x, y)."""
    h, w = len(img), len(img[0])
    pp = patch_pixels(x, y, r, w, h)
    c = sum(conf[qy][qx] for qx, qy in pp if filled[qy][qx]) / len(pp)
    ix, iy = isophote(img, filled, x, y, r)
    nx, ny = normal(filled, x, y)
    d = abs(ix * nx + iy * ny) / alpha
    return c * d, c, d


def patch_distance(img, filled, p: Pixel, q: Pixel, r: int) -> float:
    """Sum of squared differences between the patches at p and q over the filled pixels of the patch at p."""
    h, w = len(img), len(img[0])
    s = 0
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            ax, ay = p[0] + dx, p[1] + dy
            if 0 <= ax < w and 0 <= ay < h and filled[ay][ax]:
                t = img[ay][ax] - img[q[1] + dy][q[0] + dx]
                s += t * t
    return s


def criminisi_inpaint(image: Sequence[Sequence[float]], mask: Sequence[Sequence[bool]],
                      radius: int = 4, alpha: float = 255.0,
                      trace: Optional[list] = None) -> Image:
    """Fill the pixels where mask is True by copying patches from the known part of the image.

    Precondition: image and mask have the same shape, radius >= 0, alpha > 0,
    and at least one patch of side 2*radius+1 fits in the image outside the
    mask. If trace is a list, one record per step is appended to it:
    (image, filled, conf) before the step, the chosen pixel and the chosen
    source center.
    """
    h = len(image)
    if h == 0 or len(image[0]) == 0:
        raise ValueError("the image is empty")
    w = len(image[0])
    if len(mask) != h or any(len(row) != w for row in image) or any(len(row) != w for row in mask):
        raise ValueError("image and mask must have the same shape")
    if radius < 0 or alpha <= 0:
        raise ValueError("radius must be >= 0 and alpha > 0")
    img: Image = [list(row) for row in image]
    filled = [[not m for m in row] for row in mask]  # @line L1
    conf = [[1.0 if f else 0.0 for f in row] for row in filled]  # @line L2
    sources = source_centers(mask, radius)  # @line L3
    if not sources and any(any(row) for row in mask):
        raise ValueError("no source patch fits outside the target region")
    while True:
        fr = front(filled)  # @line L4
        if not fr:  # @line L5
            break
        best = None
        for x, y in fr:  # @line L6
            p_val, c_val, _ = priority(img, filled, conf, x, y, radius, alpha)
            if best is None or (p_val, c_val) > (best[0], best[1]):
                best = (p_val, c_val, (x, y))
        p_hat = best[2]  # @line L7
        q_hat, q_dist = None, None
        for q in sources:  # @line L8
            dq = patch_distance(img, filled, p_hat, q, radius)
            if q_dist is None or dq < q_dist:
                q_hat, q_dist = q, dq
        if trace is not None:
            trace.append(([list(r) for r in img], [list(r) for r in filled],
                          [list(r) for r in conf], p_hat, q_hat))
        c_hat = best[1]
        for dy in range(-radius, radius + 1):  # @line L9
            for dx in range(-radius, radius + 1):
                ax, ay = p_hat[0] + dx, p_hat[1] + dy
                if 0 <= ax < w and 0 <= ay < h and not filled[ay][ax]:
                    img[ay][ax] = img[q_hat[1] + dy][q_hat[0] + dx]  # @line L10
                    filled[ay][ax] = True
                    conf[ay][ax] = c_hat  # @line L11
    return img  # @line L12
