# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-z-buffer/. The authors are listed in prov/EAKK9Q.jsonl.

"""The hierarchical z-buffer (Greene, Kass and Miller 1993).

A z-pyramid sits on top of an ordinary z-buffer. Level 0 is the depth buffer,
padded to a square of side 2^L. Each entry of level l + 1 is the farthest
(largest) depth of the 2 x 2 entries below it. An object with screen bounds R
and nearest depth zmin is hidden if zmin >= the stored depth at each pixel of
R, and the pyramid proves this while it visits few entries.

The scene is a list of objects, each a list of screen-space triangles
((x0, y0, z0), (x1, y1, z1), (x2, y2, z2)) in pixel units, x to the right,
y down, pixel centers at (i + 1/2, j + 1/2), smaller z nearer. Objects are
drawn nearest first, by their zmin; this replaces the octree of the paper.
"""

from fractions import Fraction
from math import ceil, floor

HALF = Fraction(1, 2)
FAR = float("inf")


def _edge(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def _top_left(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    return dy < 0 or (dy == 0 and dx > 0)


def fragments(tri, width, height):
    """Yield (i, j, z) for each covered pixel center (top-left rule)."""
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
    area = _edge(x0, y0, x1, y1, x2, y2)
    if area == 0:
        return
    if area < 0:
        x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        area = -area
    edges = ((x1, y1, x2, y2), (x2, y2, x0, y0), (x0, y0, x1, y1))
    tl = [_top_left(*e) for e in edges]
    for j in range(max(0, ceil(min(y0, y1, y2) - HALF)), min(height - 1, floor(max(y0, y1, y2) - HALF)) + 1):
        for i in range(max(0, ceil(min(x0, x1, x2) - HALF)), min(width - 1, floor(max(x0, x1, x2) - HALF)) + 1):
            w = [_edge(*e, i + HALF, j + HALF) for e in edges]
            if all(w[k] > 0 or (w[k] == 0 and tl[k]) for k in range(3)):
                yield i, j, (w[0] * z0 + w[1] * z1 + w[2] * z2) / Fraction(area)


def pixel_bounds(tris, width, height):
    """Pixel rectangle (i0, j0, i1, j1), inclusive, that holds every pixel
    center the triangles can cover, clamped to the screen; None if empty."""
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    if not xs:
        return None
    i0, i1 = max(0, ceil(min(xs) - HALF)), min(width - 1, floor(max(xs) - HALF))
    j0, j1 = max(0, ceil(min(ys) - HALF)), min(height - 1, floor(max(ys) - HALF))
    if i0 > i1 or j0 > j1:
        return None
    return i0, j0, i1, j1


class ZPyramid:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.levels = 0
        while (1 << self.levels) < max(width, height):
            self.levels += 1
        side = 1 << self.levels
        # z[l][y][x]; level 0 is the depth buffer, padded with FAR.
        self.z = [[[FAR] * (side >> l) for _ in range(side >> l)] for l in range(self.levels + 1)]
        self.visits = 0

    def depth(self, i, j):
        return self.z[0][j][i]

    def write(self, i, j, d):
        """Set a depth at level 0 and update the farthest depth upward."""
        self.z[0][j][i] = d  # @line L12
        x, y = i, j
        for l in range(1, self.levels + 1):  # @line L13
            x, y = x >> 1, y >> 1
            below = self.z[l - 1]
            m = max(below[2 * y][2 * x], below[2 * y][2 * x + 1],
                    below[2 * y + 1][2 * x], below[2 * y + 1][2 * x + 1])
            if self.z[l][y][x] == m:
                break  # nothing above changes
            self.z[l][y][x] = m

    def hidden(self, rect, zmin):
        """True only if zmin >= depth at every pixel of rect = (i0, j0, i1, j1).
        Then no fragment with depth >= zmin inside rect can pass the test z < depth."""
        i0, j0, i1, j1 = rect
        stack = [(self.levels, 0, 0)]  # @line L1: the root
        while stack:  # @line L2
            l, x, y = stack.pop()
            self.visits += 1
            s = 1 << l  # the entry covers pixels [x*s, x*s+s) x [y*s, y*s+s)
            if x * s > i1 or (x + 1) * s - 1 < i0 or y * s > j1 or (y + 1) * s - 1 < j0:
                continue  # @line L3: outside the rectangle
            if zmin >= self.z[l][y][x]:
                continue  # @line L4: hidden in this whole entry
            if l == 0:
                return False  # @line L5: a pixel where the object may be visible
            for dy in (0, 1):  # @line L6
                for dx in (0, 1):
                    stack.append((l - 1, 2 * x + dx, 2 * y + dy))
        return True  # @line L7


def hzb_render(width, height, objects, colors, background=None):
    """Draw the objects nearest first, and skip an object or a triangle that the
    z-pyramid proves hidden. Return (color, depth, culled), where culled counts
    the culled objects and triangles."""
    pyr = ZPyramid(width, height)
    color = [[background] * width for _ in range(height)]
    order = sorted(range(len(objects)),
                   key=lambda o: min((v[2] for t in objects[o] for v in t), default=FAR))
    culled = {"objects": 0, "triangles": 0}
    for o in order:  # @line L8
        rect = pixel_bounds(objects[o], width, height)
        if rect is None:
            continue
        zmin = min(v[2] for t in objects[o] for v in t)
        if pyr.hidden(rect, zmin):  # @line L9
            culled["objects"] += 1
            continue
        for t in objects[o]:
            r = pixel_bounds([t], width, height)
            if r is None or pyr.hidden(r, min(v[2] for v in t)):  # @line L10
                culled["triangles"] += 1
                continue
            for i, j, z in fragments(t, width, height):  # @line L11: the z-buffer
                if z < pyr.depth(i, j):
                    pyr.write(i, j, z)
                    color[j][i] = colors[o]
    depth = [[None if pyr.depth(i, j) == FAR else pyr.depth(i, j) for i in range(width)]
             for j in range(height)]
    return color, depth, culled
