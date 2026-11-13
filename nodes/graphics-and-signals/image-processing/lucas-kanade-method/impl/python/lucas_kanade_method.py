# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucas-kanade-method/. The authors are listed in prov/VEDYF0.jsonl.

"""Lucas-Kanade flow for one window, in one step and iterated.

Frames are lists of rows of gray values; row index y, column index x, pixel
centers at (x + 1/2, y + 1/2). The flow d = (u, v) of a window is the shift
with E2(p + d) close to E1(p) for the pixels p of the window. The gradient is
the central difference. Off-grid samples use bilinear interpolation with the
indices clamped to the image.
"""

import math


def normal_equations(ix, iy, it):
    """Return (a, b, c, p, q): G = [[a, b], [b, c]] and the right side (p, q) = -(sum Ix It, sum Iy It)."""
    a = sum(x * x for x in ix)
    b = sum(x * y for x, y in zip(ix, iy))
    c = sum(y * y for y in iy)
    p = -sum(x * t for x, t in zip(ix, it))
    q = -sum(y * t for y, t in zip(iy, it))
    return a, b, c, p, q


def solve_2x2(a, b, c, p, q, eps=0):
    """Solve [[a, b], [b, c]] d = (p, q) by the closed form; None if the determinant is at most eps."""
    det = a * c - b * b
    if det <= eps:
        return None
    return (c * p - b * q) / det, (a * q - b * p) / det


def min_eigenvalue(a, b, c):
    """The smaller eigenvalue of the symmetric matrix [[a, b], [b, c]]."""
    return (a + c - math.sqrt((a - c) ** 2 + 4 * b * b)) / 2


def sample(img, x, y):
    """Bilinear sample at the real position (x, y) in index units, indices clamped."""
    h, w = len(img), len(img[0])
    x0, y0 = math.floor(x), math.floor(y)
    fx, fy = x - x0, y - y0

    def at(yy, xx):
        return img[min(max(yy, 0), h - 1)][min(max(xx, 0), w - 1)]

    top = (1 - fx) * at(y0, x0) + fx * at(y0, x0 + 1)
    bottom = (1 - fx) * at(y0 + 1, x0) + fx * at(y0 + 1, x0 + 1)
    return (1 - fy) * top + fy * bottom


def window(x0, y0, r):
    return [(x, y) for y in range(y0 - r, y0 + r + 1) for x in range(x0 - r, x0 + r + 1)]


def lucas_kanade_step(e1, e2, pixels, d=(0, 0)):
    """One linearized solve around the shift d. Return the correction, or None if G is singular."""
    ix, iy, it = [], [], []  # @line L3
    for x, y in pixels:  # @line L4
        sx, sy = x + d[0], y + d[1]
        ix.append((sample(e2, sx + 1, sy) - sample(e2, sx - 1, sy)) / 2)  # @line L5
        iy.append((sample(e2, sx, sy + 1) - sample(e2, sx, sy - 1)) / 2)
        it.append(sample(e2, sx, sy) - e1[y][x])  # @line L6
    a, b, c, p, q = normal_equations(ix, iy, it)  # @line L7
    return solve_2x2(a, b, c, p, q)  # @line L8


def lucas_kanade(e1, e2, pixels, iterations=20, tol=1e-9):
    """Iterate the step until the correction is below tol. Return (d, number of steps) or None."""
    d = (0.0, 0.0)  # @line L1
    for k in range(1, iterations + 1):  # @line L2
        step = lucas_kanade_step(e1, e2, pixels, d)
        if step is None:
            return None
        d = (d[0] + step[0], d[1] + step[1])  # @line L9
        if math.hypot(*step) < tol:  # @line L10
            return d, k
    return d, iterations  # @line L11
