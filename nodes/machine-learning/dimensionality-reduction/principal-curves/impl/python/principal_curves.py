# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-curves/. The authors are listed in prov/RXEEKH.jsonl.

"""The principal curve algorithm of Hastie and Stuetzle (1989).

The curve is a polygonal line through the points f(lambda_i). It starts as the first
principal component line. Then two steps alternate:
  - conditional expectation: f(lambda_i) <- a locally weighted linear fit of x on lambda,
    with tricube weights over the span*n points nearest in lambda, evaluated at lambda_i;
  - projection: lambda_i <- the arc length position of the point of the polygon nearest to x_i.
The loop stops when the relative change of D^2 = sum |x_i - f(lambda_i)|^2 is below tol.
"""

import bisect
import math


def _sub(u, v):
    return [a - b for a, b in zip(u, v)]


def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def first_principal_direction(points, iters=500):
    """Mean and unit leading eigenvector of the sample covariance (power iteration)."""
    n, d = len(points), len(points[0])
    mean = [sum(p[k] for p in points) / n for k in range(d)]
    cov = [[sum((p[a] - mean[a]) * (p[b] - mean[b]) for p in points) / n for b in range(d)] for a in range(d)]
    v = [1.0 / math.sqrt(d + k) for k in range(d)]  # a fixed start, not orthogonal to any axis
    for _ in range(iters):
        w = [_dot(row, v) for row in cov]
        norm = math.sqrt(_dot(w, w))
        if norm == 0.0:
            break
        v = [a / norm for a in w]
    return mean, v


def project_to_polyline(x, vertices):
    """Return (lambda, point, squared distance): the nearest point of the polygon to x.

    lambda is the arc length from the first vertex. On ties the largest lambda is kept,
    as in the definition lambda_f(x) = sup{lambda : |x - f(lambda)| = min}.
    """
    best = None
    arc = 0.0
    if len(vertices) == 1:
        return 0.0, vertices[0][:], _dot(_sub(x, vertices[0]), _sub(x, vertices[0]))
    for a, b in zip(vertices, vertices[1:]):
        ab = _sub(b, a)
        length2 = _dot(ab, ab)
        t = 0.0 if length2 == 0.0 else max(0.0, min(1.0, _dot(_sub(x, a), ab) / length2))
        p = [ai + t * di for ai, di in zip(a, ab)]
        dist2 = _dot(_sub(x, p), _sub(x, p))
        lam = arc + t * math.sqrt(length2)
        if best is None or dist2 <= best[2]:
            best = (lam, p, dist2)
        arc += math.sqrt(length2)
    return best


def _window(lams, at, q):
    """Start of the q consecutive entries of the sorted list lams that are nearest to at."""
    n = len(lams)
    lo = max(0, min(bisect.bisect_left(lams, at) - q // 2, n - q))
    while lo > 0 and at - lams[lo - 1] < lams[lo + q - 1] - at:
        lo -= 1
    while lo + q < n and lams[lo + q] - at < at - lams[lo]:
        lo += 1
    return lo


def local_linear(lams, xs, at, span):
    """Locally weighted linear fit of x on lambda (tricube weights), evaluated at `at`.

    lams must be sorted; xs[i] is the point with index lams[i]. The fit uses the
    ceil(span * n) points nearest in lambda (at least 3).
    """
    n = len(lams)
    q = min(n, max(3, int(math.ceil(span * n))))
    lo = _window(lams, at, q)
    near = range(lo, lo + q)
    h = max(abs(lams[i] - at) for i in near) * 1.0001
    if h == 0.0:
        w = {i: 1.0 for i in near}
    else:
        w = {i: (1.0 - (abs(lams[i] - at) / h) ** 3) ** 3 for i in near}
    sw = sum(w.values())
    lbar = sum(w[i] * lams[i] for i in near) / sw
    sll = sum(w[i] * (lams[i] - lbar) ** 2 for i in near)
    out = []
    for k in range(len(xs[0])):
        xbar = sum(w[i] * xs[i][k] for i in near) / sw
        if sll <= 1e-300:
            out.append(xbar)
        else:
            slope = sum(w[i] * (lams[i] - lbar) * (xs[i][k] - xbar) for i in near) / sll
            out.append(xbar + slope * (at - lbar))
    return out


def principal_curve(points, span=0.3, tol=1e-3, max_iter=30):
    """Hastie-Stuetzle principal curve. Returns (vertices sorted by lambda, lambdas, D^2 per iteration)."""
    mean, v = first_principal_direction(points)  # @line L1
    lams = [_dot(_sub(x, mean), v) for x in points]  # @line L2
    history = [sum(_dot(_sub(x, [m + l * vk for m, vk in zip(mean, v)]),
                        _sub(x, [m + l * vk for m, vk in zip(mean, v)])) for x, l in zip(points, lams))]
    vertices = []
    for _ in range(max_iter):  # @line L3
        order = sorted(range(len(points)), key=lambda i: lams[i])  # @line L4
        ls = [lams[i] for i in order]
        xs = [points[i] for i in order]
        vertices = [local_linear(ls, xs, at, span) for at in ls]  # @line L5
        proj = [project_to_polyline(x, vertices) for x in points]  # @line L6
        lams = [p[0] for p in proj]
        d2 = sum(p[2] for p in proj)  # @line L7
        history.append(d2)
        if abs(history[-2] - d2) <= tol * history[-2] + 1e-20:  # @line L8
            break
    return vertices, lams, history  # @line L9
