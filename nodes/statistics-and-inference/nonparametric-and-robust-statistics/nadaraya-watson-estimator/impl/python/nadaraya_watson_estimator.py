# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nadaraya-watson-estimator/. The authors are listed in prov/HA8PMS.jsonl.

import math


def gaussian(u):
    return math.exp(-0.5 * u * u) / math.sqrt(2 * math.pi)


def epanechnikov(u):
    """(3/4)(1 - u^2) on [-1, 1]; works with floats and Fractions."""
    return 3 * (1 - u * u) / 4 if -1 <= u <= 1 else 0 * u


def weights(x, xs, h, kernel=epanechnikov):
    """The Nadaraya-Watson weights w_i(x); they sum to 1. None if all are 0."""
    k = [kernel((x - xi) / h) for xi in xs]
    s = sum(k)
    if s == 0:
        return None
    return [v / s for v in k]


def nadaraya_watson(x, xs, ys, h, kernel=epanechnikov):
    """m(x) = sum K((x - x_i)/h) y_i / sum K((x - x_i)/h). O(n) time.

    Returns None where no x_i is within the support of the kernel.
    """
    num = 0 * x  # @line L1
    den = 0 * x
    for xi, yi in zip(xs, ys):
        w = kernel((x - xi) / h)  # @line L2
        num += w * yi  # @line L3
        den += w
    if den == 0:  # @line L4
        return None
    return num / den  # @line L5


def loo_cv(h, xs, ys, kernel=epanechnikov):
    """Leave-one-out mean squared prediction error, in O(n^2).

    Uses m_{-i}(x_i) = (num_i - K(0) y_i) / (den_i - K(0)): removing point i
    from the sums at x_i removes the term K(0) y_i and K(0).
    Points whose leave-one-out denominator is 0 are skipped.
    """
    k0 = kernel(0 * h)
    tot, cnt = 0, 0
    for xi, yi in zip(xs, ys):
        num = sum(kernel((xi - xj) / h) * yj for xj, yj in zip(xs, ys)) - k0 * yi
        den = sum(kernel((xi - xj) / h) for xj in xs) - k0
        if den > 0:
            tot += (yi - num / den) ** 2
            cnt += 1
    return tot / cnt if cnt else math.inf


def loo_cv_brute(h, xs, ys, kernel=epanechnikov):
    """The same score by refitting without each point (for tests)."""
    tot, cnt = 0, 0
    for i in range(len(xs)):
        rest_x = xs[:i] + xs[i + 1:]
        rest_y = ys[:i] + ys[i + 1:]
        m = nadaraya_watson(xs[i], rest_x, rest_y, h, kernel)
        if m is not None:
            tot += (ys[i] - m) ** 2
            cnt += 1
    return tot / cnt if cnt else math.inf


def choose_bandwidth(xs, ys, candidates, kernel=epanechnikov):
    """The candidate with the smallest leave-one-out error."""
    return min(candidates, key=lambda h: loo_cv(h, xs, ys, kernel))
