# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a-buffer/. The authors are listed in prov/1XFX5C.jsonl.

"""The A-buffer (Carpenter 1984): a z-buffer that keeps, per pixel, a list of
fragments with subpixel coverage masks, and resolves the list in depth order.

A triangle is ((x0, y0, z0), (x1, y1, z1), (x2, y2, z2)) in pixel units, x to
the right, y down, smaller z nearer. The pixel (i, j) is the square
[i, i + 1] x [j, j + 1]. It has sx * sy subpixel cells (Carpenter used 8 by 4,
a 32-bit mask). Bit a + sx * b of a mask is set when the triangle covers the
center of cell (a, b), under the top-left rule. Each fragment gets one depth:
the depth of the triangle plane at the pixel center. A color is a tuple of
numbers; use Fraction values for exact results.
"""

from fractions import Fraction
from math import ceil, floor
from typing import Sequence

HALF = Fraction(1, 2)


def _edge(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def _top_left(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    return dy < 0 or (dy == 0 and dx > 0)


class Fragment:
    __slots__ = ("z", "k", "mask", "color", "opacity")

    def __init__(self, z, k, mask, color, opacity):
        self.z, self.k, self.mask, self.color, self.opacity = z, k, mask, color, opacity


def fragments_of(tri, k, color, opacity, width, height, sx, sy):
    """Yield (i, j, Fragment) for each pixel where tri covers a cell center."""
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
    area = _edge(x0, y0, x1, y1, x2, y2)
    if area == 0:
        return
    if area < 0:
        x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        area = -area
    edges = ((x1, y1, x2, y2), (x2, y2, x0, y0), (x0, y0, x1, y1))
    tl = [_top_left(*e) for e in edges]
    i_lo, i_hi = max(0, floor(min(x0, x1, x2))), min(width - 1, ceil(max(x0, x1, x2)) - 1)
    j_lo, j_hi = max(0, floor(min(y0, y1, y2))), min(height - 1, ceil(max(y0, y1, y2)) - 1)
    for j in range(j_lo, j_hi + 1):
        for i in range(i_lo, i_hi + 1):
            mask = 0
            for b in range(sy):
                py = j + Fraction(2 * b + 1, 2 * sy)
                for a in range(sx):
                    px = i + Fraction(2 * a + 1, 2 * sx)
                    ok = True
                    for e, t in zip(edges, tl):
                        w = _edge(*e, px, py)
                        if w < 0 or (w == 0 and not t):
                            ok = False
                            break
                    if ok:
                        mask |= 1 << (a + sx * b)
            if mask:
                cx, cy = i + HALF, j + HALF
                z = (_edge(*edges[0], cx, cy) * z0 + _edge(*edges[1], cx, cy) * z1
                     + _edge(*edges[2], cx, cy) * z2) / Fraction(area)
                yield i, j, Fragment(z, k, mask, color, opacity)


class Pixel:
    """Carpenter's pixel: the nearest opaque fragment that covers the whole
    pixel (if any) and the list of fragments in front of it."""
    __slots__ = ("full", "frags")

    def __init__(self):
        self.full = None  # Fragment or None
        self.frags = []


def insert(pix: Pixel, f: Fragment, full_mask: int) -> None:
    key = (f.z, f.k)
    if pix.full is not None and key > (pix.full.z, pix.full.k):  # @line L4
        return  # hidden behind an opaque fragment that covers the pixel
    if f.opacity == 1 and f.mask == full_mask:  # @line L5
        pix.full = f  # @line L6
        pix.frags = [g for g in pix.frags if (g.z, g.k) < key]
    else:
        pix.frags.append(f)  # @line L7


def resolve(pix: Pixel, full_mask: int, cells: int, background):
    """Area-weighted color of the pixel. Fragments are taken front to back.
    groups holds disjoint subpixel masks with the product of (1 - opacity) of
    the nearer fragments that cover them; this unrolls Carpenter's recursive
    packing procedure, whose calls at one depth also have disjoint masks."""
    frags = sorted(pix.frags, key=lambda g: (g.z, g.k))  # @line L8
    if pix.full is not None:
        frags.append(pix.full)
    n = len(background)
    total = [Fraction(0)] * n
    groups = [(full_mask, Fraction(1))]  # @line L9
    for f in frags:  # @line L10
        new_groups = []
        for m, t in groups:
            inside, outside = m & f.mask, m & ~f.mask  # @line L11
            if inside:
                w = t * f.opacity * bin(inside).count("1")  # @line L12
                for c in range(n):
                    total[c] += w * f.color[c]
                if f.opacity != 1:
                    new_groups.append((inside, t * (1 - f.opacity)))  # @line L13
            if outside:
                new_groups.append((outside, t))
        groups = new_groups
        if not groups:
            break
    for m, t in groups:  # @line L14
        w = t * bin(m).count("1")
        for c in range(n):
            total[c] += w * background[c]
    return tuple(x / cells for x in total)  # @line L15


def a_buffer(width: int, height: int, triangles: Sequence, colors: Sequence,
             opacities: Sequence, background, sx: int = 8, sy: int = 4):
    """Render with the A-buffer. Return a height x width grid of color tuples."""
    full_mask = (1 << (sx * sy)) - 1
    pixels = [[Pixel() for _ in range(width)] for _ in range(height)]  # @line L1
    for k, tri in enumerate(triangles):  # @line L2
        for i, j, f in fragments_of(tri, k, colors[k], Fraction(opacities[k]),
                                    width, height, sx, sy):  # @line L3
            insert(pixels[j][i], f, full_mask)
    return [[resolve(pixels[j][i], full_mask, sx * sy, background)
             for i in range(width)] for j in range(height)]
