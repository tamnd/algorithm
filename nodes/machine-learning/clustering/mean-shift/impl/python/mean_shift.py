# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-shift/. The authors are listed in prov/AN3FSZ.jsonl.

"""Mean shift clustering with a Gaussian kernel (Fukunaga and Hostetler 1975,
Cheng 1995, Comaniciu and Meer 2002).

Each point is moved to the weighted mean of the data, with Gaussian weights
around its current position, until the move is shorter than tol. Points whose
end positions (modes) are closer than merge_dist share a cluster.
"""

import math


def sq_dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def density(y, points, h):
    """Gaussian kernel density estimate at y, without the normalizing constant."""
    return sum(math.exp(-sq_dist(y, x) / (2 * h * h)) for x in points) / len(points)


def shift(y, points, h):
    """One mean shift step: the Gaussian weighted mean of the data around y."""
    weights = [math.exp(-sq_dist(y, x) / (2 * h * h)) for x in points]  # @line L4
    total = sum(weights)
    return tuple(sum(w * x[k] for w, x in zip(weights, points)) / total for k in range(len(y)))  # @line L5


def find_mode(start, points, h, tol=1e-7, max_iter=10000, trace=None):
    """Iterate the mean shift step from start until the step is shorter than tol."""
    y = tuple(start)  # @line L2
    if trace is not None:
        trace.append(y)
    for _ in range(max_iter):  # @line L3
        y_new = shift(y, points, h)
        step = math.sqrt(sq_dist(y_new, y))  # @line L6
        y = y_new
        if trace is not None:
            trace.append(y)
        if step < tol:  # @line L7
            break
    return y


def mean_shift(points, h, tol=1e-7, merge_dist=None, max_iter=10000):
    """Return (labels, centers). labels[j] is the cluster of point j, and
    centers[c] is the first mode found for cluster c. merge_dist defaults to h / 2."""
    if h <= 0:
        raise ValueError("the bandwidth h must be positive")
    if merge_dist is None:
        merge_dist = h / 2
    modes = []
    for x in points:  # @line L1
        modes.append(find_mode(x, points, h, tol, max_iter))  # @line L8
    labels, centers = [], []  # @line L9
    for y in modes:  # @line L10
        for c, z in enumerate(centers):  # @line L11
            if math.sqrt(sq_dist(y, z)) < merge_dist:
                labels.append(c)
                break
        else:
            centers.append(y)  # @line L12
            labels.append(len(centers) - 1)
    return labels, centers  # @line L13
