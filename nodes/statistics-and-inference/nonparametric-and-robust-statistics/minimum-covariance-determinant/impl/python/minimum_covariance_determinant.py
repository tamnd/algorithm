# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-covariance-determinant/. The authors are listed in prov/KD8XYJ.jsonl.

import itertools
import random

from stdist import chi2_cdf, chi2_ppf

# The arithmetic below is generic: with int or Fraction coordinates every
# determinant, distance and comparison is exact; with floats it is ordinary
# floating point.


def mean(points, idx):
    """The mean of the points with the given indices."""
    k = len(idx)
    p = len(points[0])
    return [sum(points[i][j] for i in idx) / k for j in range(p)]


def cov(points, idx, mu=None):
    """The covariance matrix of the points with the given indices, with divisor len(idx)."""
    if mu is None:
        mu = mean(points, idx)
    k = len(idx)
    p = len(mu)
    return [
        [sum((points[i][a] - mu[a]) * (points[i][b] - mu[b]) for i in idx) / k for b in range(p)]
        for a in range(p)
    ]


def det(m):
    """The determinant by Gaussian elimination with partial pivoting."""
    a = [list(row) for row in m]
    p = len(a)
    d = 1
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(a[r][col]))
        if a[piv][col] == 0:
            return 0
        if piv != col:
            a[col], a[piv] = a[piv], a[col]
            d = -d
        d = d * a[col][col]
        for r in range(col + 1, p):
            f = a[r][col] / a[col][col]
            for k in range(col, p):
                a[r][k] -= f * a[col][k]
    return d


def inverse(m):
    """The inverse by Gauss-Jordan elimination; the matrix must be nonsingular."""
    p = len(m)
    a = [list(row) + [1 if i == j else 0 for j in range(p)] for i, row in enumerate(m)]
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(a[r][col]))
        if a[piv][col] == 0:
            raise ZeroDivisionError("singular matrix")
        a[col], a[piv] = a[piv], a[col]
        f = a[col][col]
        a[col] = [v / f for v in a[col]]
        for r in range(p):
            if r != col and a[r][col] != 0:
                g = a[r][col]
                a[r] = [v - g * w for v, w in zip(a[r], a[col])]
    return [row[p:] for row in a]


def mahalanobis2(x, mu, s_inv):
    """The squared Mahalanobis distance (x - mu)^T S^{-1} (x - mu)."""
    z = [a - b for a, b in zip(x, mu)]
    return sum(z[a] * s_inv[a][b] * z[b] for a in range(len(z)) for b in range(len(z)))


def singular(s):
    """True if S is singular: exactly for exact numbers, relative to its diagonal for floats."""
    d = det(s)
    if isinstance(d, float):
        hadamard = 1.0
        for i in range(len(s)):
            hadamard *= s[i][i]
        return d <= 1e-12 * hadamard or hadamard == 0.0
    return d == 0


def closest(points, mu, s, h):
    """The indices of the h points with the least Mahalanobis distance; ties go to the lower index."""
    s_inv = inverse(s)
    d = [mahalanobis2(x, mu, s_inv) for x in points]
    return sorted(sorted(range(len(points)), key=lambda i: (d[i], i))[:h])


def c_step(points, idx, h):
    """One concentration step: the h points closest to the mean and covariance of idx."""
    mu = mean(points, idx)
    s = cov(points, idx, mu)
    return closest(points, mu, s, h)


def concentrate(points, idx, h, max_steps=100):
    """C-steps from the h-subset idx until the determinant stops decreasing.

    Returns (det, H, mu, S) for the best h-subset reached. If its covariance is
    singular (det 0), that subset is an exact fit and is returned at once.
    """
    mu = mean(points, idx)  # @line L6
    s = cov(points, idx, mu)
    d = det(s)
    for _ in range(max_steps):  # @line L5
        if singular(s):  # @line L7
            break
        new = closest(points, mu, s, h)  # @line L8
        new_mu = mean(points, new)
        new_s = cov(points, new, new_mu)
        new_d = det(new_s)
        if new == idx or new_d >= d:  # @line L9
            break
        idx, mu, s, d = new, new_mu, new_s, new_d  # @line L6
    return d, idx, mu, s


def start_subset(points, h, rng):
    """A random (p + 1)-subset, enlarged until its covariance is nonsingular, then its h closest points."""
    n, p = len(points), len(points[0])
    order = list(range(n))
    rng.shuffle(order)
    k = p + 1
    while singular(cov(points, order[:k])):  # @line L2
        k += 1
        if k > n:
            return None
    j = order[:k]
    mu = mean(points, j)  # @line L3
    s = cov(points, j, mu)
    return closest(points, mu, s, h)  # @line L4


def default_h(n, p):
    """floor((n + p + 1) / 2), the h with the highest breakdown point."""
    return (n + p + 1) // 2


def fast_mcd_raw(points, h=None, starts=500, seed=0, max_steps=100):
    """The raw FAST-MCD fit: (det, H, mu, S) with S the covariance of H with divisor h.

    starts is the number of random starts; if it is None, every (p + 1)-subset is
    used once as the start, which makes the result deterministic.
    """
    n, p = len(points), len(points[0])
    if h is None:
        h = default_h(n, p)
    if not p < h <= n:
        raise ValueError("need p < h <= n")
    rng = random.Random(seed)
    best = None
    if starts is None:
        pool = itertools.combinations(range(n), p + 1)
    else:
        pool = range(starts)
    for item in pool:  # @line L1
        if starts is None:
            j = list(item)
            if singular(cov(points, j)):
                continue
            mu = mean(points, j)
            idx = closest(points, mu, cov(points, j, mu), h)
        else:
            idx = start_subset(points, h, rng)
            if idx is None:
                continue
        fit = concentrate(points, idx, h, max_steps)
        if best is None or fit[0] < best[0]:  # @line L10
            best = fit
    if best is None:
        raise ValueError("every start was singular")
    return best


def exact_mcd(points, h=None):
    """The exact raw MCD by enumeration of all h-subsets: (det, H). Only for small n."""
    n, p = len(points), len(points[0])
    if h is None:
        h = default_h(n, p)
    best = None
    for idx in itertools.combinations(range(n), h):
        d = det(cov(points, list(idx)))
        if best is None or d < best[0]:
            best = (d, list(idx))
    return best


def consistency_factor(alpha, p):
    """alpha / F_{chi2(p+2)}(chi2_{p, alpha}): it makes the raw MCD scatter consistent at the normal."""
    return alpha / chi2_cdf(chi2_ppf(alpha, p), p + 2)


def mcd(points, h=None, starts=500, seed=0, delta=0.025):
    """FAST-MCD with the consistency factor and one reweighting step, in floating point.

    Returns a dict with the raw location and scatter, the reweighted location and
    scatter, the h-subset, and the outlier flags of the reweighting step.
    """
    pts = [[float(v) for v in x] for x in points]
    n, p = len(pts), len(pts[0])
    if h is None:
        h = default_h(n, p)
    _, idx, mu, s = fast_mcd_raw(pts, h, starts, seed)
    c = consistency_factor(h / n, p)  # @line L11
    s = [[c * v for v in row] for row in s]
    cut = chi2_ppf(1.0 - delta, p)
    s_inv = inverse(s)
    d2 = [mahalanobis2(x, mu, s_inv) for x in pts]
    keep = [i for i in range(n) if d2[i] <= cut]  # @line L12
    mu_w = mean(pts, keep)  # @line L13
    c_w = (1.0 - delta) / chi2_cdf(cut, p + 2)
    s_w = [[c_w * v for v in row] for row in cov(pts, keep, mu_w)]
    s_w_inv = inverse(s_w)
    flags = [mahalanobis2(x, mu_w, s_w_inv) > cut for x in pts]
    return {  # @line L14
        "raw_location": mu,
        "raw_scatter": s,
        "subset": idx,
        "location": mu_w,
        "scatter": s_w,
        "outlier": flags,
        "distance2": [mahalanobis2(x, mu_w, s_w_inv) for x in pts],
    }
