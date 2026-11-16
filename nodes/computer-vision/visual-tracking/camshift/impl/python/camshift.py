# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/camshift/. The authors are listed in prov/WQRMAE.jsonl.

"""CAMShift (Bradski 1998): mean shift on a back-projected probability image,
with the window size and the orientation set from the image moments.

Images are lists of rows of integer values 0..255, indexed img[v][u]; the
center of pixel (u, v) is the point (u, v). The feature of a pixel is its
value divided into `bins` equal bins (Bradski uses the hue of a color pixel).
A window is (cu, cv, au, av): the pixels with |u - cu| <= au and
|v - cv| <= av, clipped to the image. Angles are measured from the u axis
toward the v axis; since v points down, a positive angle turns clockwise on
the screen.
"""

import math


def bin_of(value, bins):
    return value * bins // 256


def lookup_table(img, window, bins):
    """The histogram of the window, scaled so that the largest bin is 255."""
    hist = [0] * bins
    for u, v in window_pixels(img, window):
        hist[bin_of(img[v][u], bins)] += 1
    top = max(hist)
    if top == 0:
        raise ValueError("empty window")
    return [255.0 * x / top for x in hist]


def back_project(img, table, bins):
    """The probability image: each pixel replaced by the table value of its bin."""
    return [[table[bin_of(x, bins)] for x in row] for row in img]


def window_pixels(img, window):
    cu, cv, au, av = window
    rows, cols = len(img), len(img[0])
    for v in range(max(0, math.ceil(cv - av)), min(rows - 1, math.floor(cv + av)) + 1):
        for u in range(max(0, math.ceil(cu - au)), min(cols - 1, math.floor(cu + au)) + 1):
            yield u, v


def moments(prob, window):
    """M00, M10, M01, M20, M11, M02 of the probability image in the window."""
    m = [0.0] * 6
    for u, v in window_pixels(prob, window):
        p = prob[v][u]
        m[0] += p
        m[1] += p * u
        m[2] += p * v
        m[3] += p * u * u
        m[4] += p * u * v
        m[5] += p * v * v
    return m


def window_side(m00):
    """Bradski's size rule s = 2 sqrt(M00 / 256), rounded up to an odd
    integer, at least 3."""
    s = math.ceil(2 * math.sqrt(m00 / 256))
    if s % 2 == 0:
        s += 1
    return max(s, 3)


def shape(m):
    """Center, orientation, and the lengths along the two axes (the square
    roots of the eigenvalues of the second central moments)."""
    m00, m10, m01, m20, m11, m02 = m
    xc, yc = m10 / m00, m01 / m00
    a = m20 / m00 - xc * xc
    b = 2 * (m11 / m00 - xc * yc)
    c = m02 / m00 - yc * yc
    theta = 0.5 * math.atan2(b, a - c)
    root = math.sqrt(b * b + (a - c) ** 2)
    length = math.sqrt(max((a + c + root) / 2, 0.0))
    width = math.sqrt(max((a + c - root) / 2, 0.0))
    return (xc, yc), theta, length, width


def camshift_frame(prob, window, eps=0.5, max_iter=20, aspect=1.0):
    """One frame. Returns (new window, (center, theta, length, width)), or
    (window, None) if the window holds no probability."""
    cu, cv, au, av = window
    m = None
    for _ in range(max_iter):  # @line L3
        m = moments(prob, (cu, cv, au, av))  # @line L4
        if m[0] == 0:  # @line L5
            return window, None
        nu, nv = m[1] / m[0], m[2] / m[0]  # @line L6
        moved = math.hypot(nu - cu, nv - cv)
        cu, cv = nu, nv
        if moved < eps:  # @line L7
            break
    m = moments(prob, (cu, cv, au, av))
    if m[0] == 0:
        return window, None
    s = window_side(m[0])  # @line L8
    center, theta, length, width = shape(m)  # @line L9
    return (cu, cv, s / 2, aspect * s / 2), (center, theta, length, width)  # @line L10


def camshift(frames, window, bins=16, eps=0.5, max_iter=20, aspect=1.0):
    """Track the target that frames[0] shows in the window. Returns one
    (window, shape) pair per later frame; shape is None when the target is lost."""
    table = lookup_table(frames[0], window, bins)  # @line L1
    out = []
    for img in frames[1:]:
        prob = back_project(img, table, bins)  # @line L2
        window, info = camshift_frame(prob, window, eps, max_iter, aspect)
        out.append((window, info))
    return out  # @line L11
