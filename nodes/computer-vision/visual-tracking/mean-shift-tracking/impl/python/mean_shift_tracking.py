# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-shift-tracking/. The authors are listed in prov/85H8BD.jsonl.

"""Mean shift tracking (Comaniciu, Ramesh and Meer) with the Epanechnikov
profile and the Bhattacharyya coefficient.

Images are lists of rows of integer gray values 0..255, indexed img[v][u];
the center of pixel (u, v) is the point (u, v). A window is an ellipse with
center y = (yu, yv) and half axes (hu, hv). The normalized squared distance
of pixel x is r = ((u - yu) / hu)^2 + ((v - yv) / hv)^2, and the profile is
k(r) = 1 - r for r < 1 and 0 otherwise. Gray values fall into `bins` equal
bins.
"""

import math


def bin_of(value, bins):
    return value * bins // 256


def window_pixels(img, y, h):
    """The pixels (u, v, r) with r < 1 for the window at y with half axes h."""
    rows, cols = len(img), len(img[0])
    out = []
    for v in range(max(0, math.ceil(y[1] - h[1])), min(rows - 1, math.floor(y[1] + h[1])) + 1):
        for u in range(max(0, math.ceil(y[0] - h[0])), min(cols - 1, math.floor(y[0] + h[0])) + 1):
            r = ((u - y[0]) / h[0]) ** 2 + ((v - y[1]) / h[1]) ** 2
            if r < 1:
                out.append((u, v, r))
    return out


def histogram(img, y, h, bins):
    """Kernel-weighted histogram p_u(y), normalized to sum 1."""
    p = [0.0] * bins
    for u, v, r in window_pixels(img, y, h):
        p[bin_of(img[v][u], bins)] += 1 - r
    s = sum(p)
    if s == 0:
        return p
    return [x / s for x in p]


def bhattacharyya(p, q):
    """The Bhattacharyya coefficient sum_u sqrt(p_u q_u)."""
    return sum(math.sqrt(a * b) for a, b in zip(p, q))


def weighted_mean_shift(points, weights, y, h):
    """One mean shift step of the weighted Epanechnikov density
    f(y) = sum_i w_i k(|(x_i - y) / h|^2): the w-weighted mean of the points
    inside the window at y (the profile g = -k' is 1 there). Returns y if
    the window holds no point with positive weight."""
    su = sv = sw = 0.0
    for (u, v), w in zip(points, weights):
        if ((u - y[0]) / h[0]) ** 2 + ((v - y[1]) / h[1]) ** 2 <= 1 and w > 0:
            su += w * u
            sv += w * v
            sw += w
    if sw == 0:
        return y
    return (su / sw, sv / sw)


def mean_shift_step(img, q, y0, p0, h, bins, eps=0.1, max_iter=20, max_halving=10):
    """Find the target near y0 in img. q is the target model and p0 the
    histogram at y0. Returns (y, rho, history), where history lists the
    Bhattacharyya coefficient of every accepted location."""
    rho0 = bhattacharyya(p0, q)  # @line L1
    history = [rho0]
    for _ in range(max_iter):  # @line L2
        su = sv = sw = 0.0
        for u, v, r in window_pixels(img, y0, h):  # @line L3
            b = bin_of(img[v][u], bins)
            w = math.sqrt(q[b] / p0[b])
            su += w * u
            sv += w * v
            sw += w
        if sw == 0:
            return y0, rho0, history
        y1 = (su / sw, sv / sw)  # @line L4
        p1 = histogram(img, y1, h, bins)  # @line L5
        rho1 = bhattacharyya(p1, q)
        halving = 0
        while rho1 < rho0 and halving < max_halving:  # @line L6
            y1 = ((y0[0] + y1[0]) / 2, (y0[1] + y1[1]) / 2)  # @line L7
            p1 = histogram(img, y1, h, bins)
            rho1 = bhattacharyya(p1, q)
            halving += 1
        if rho1 < rho0:  # @line L8
            return y0, rho0, history
        history.append(rho1)
        if math.hypot(y1[0] - y0[0], y1[1] - y0[1]) < eps:  # @line L9
            return y1, rho1, history
        y0, p0, rho0 = y1, p1, rho1  # @line L10
    return y0, rho0, history  # @line L11


def track(frames, y0, h, bins=16, eps=0.1, max_iter=20):
    """Track the target that frames[0] shows in the window at y0. The model q
    is the histogram of that window. Returns the list of centers and the
    list of Bhattacharyya coefficients, one per frame."""
    q = histogram(frames[0], y0, h, bins)
    centers, scores = [y0], [1.0]
    y = y0
    for img in frames[1:]:
        p = histogram(img, y, h, bins)
        y, rho, _ = mean_shift_step(img, q, y, p, h, bins, eps, max_iter)
        centers.append(y)
        scores.append(rho)
    return centers, scores
