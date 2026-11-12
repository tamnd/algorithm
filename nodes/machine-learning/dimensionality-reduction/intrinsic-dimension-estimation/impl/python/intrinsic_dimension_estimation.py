# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/intrinsic-dimension-estimation/. The authors are listed in prov/253A61.jsonl.
"""Three estimators of the intrinsic dimension of a point cloud in R^D (Euclidean distance):
the maximum likelihood estimator of Levina and Bickel (2005), the TwoNN estimator of
Facco, d'Errico, Rodriguez and Laio (2017), and the correlation dimension of
Grassberger and Procaccia (1983) by a least squares slope."""

import math


def sorted_neighbor_distances(points, kmax):
    """For each point, the distances to its kmax nearest other points, in increasing order (brute force)."""
    n = len(points)
    out = []
    for i in range(n):
        p = points[i]
        ds = []
        for j in range(n):
            if j != i:
                q = points[j]
                ds.append(math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q))))
        ds.sort()
        out.append(ds[:kmax])
    return out


def levina_bickel_local(t, k):
    """m_k(x) = [ (1/(k-1)) sum_{j<k} ln(T_k / T_j) ]^(-1), with t[j-1] = T_j."""
    s = sum(math.log(t[k - 1] / t[j]) for j in range(k - 1))
    return (k - 1) / s


def levina_bickel(points, k1, k2=None):
    """The Levina-Bickel estimate: average the local MLE over the points, then over k = k1..k2."""
    if k2 is None:
        k2 = k1
    if k1 < 2 or k2 < k1:
        raise ValueError("need 2 <= k1 <= k2")
    nd = sorted_neighbor_distances(points, k2)
    per_k = []
    for k in range(k1, k2 + 1):
        per_k.append(sum(levina_bickel_local(t, k) for t in nd) / len(nd))
    return sum(per_k) / len(per_k)


def twonn_fit(mus, discard=0.1):
    """Fit y = d x through the origin on (ln mu, -ln(1 - F_emp(mu))) after dropping the largest mus.

    F_emp(mu_(i)) = i / N for the i-th smallest value; the slope is sum(x y) / sum(x x).
    """
    mus = sorted(mus)
    n = len(mus)
    keep = n - int(math.floor(discard * n))
    if keep >= n:  # the point i = N has F_emp = 1 and an infinite y
        keep = n - 1
    sxy = sxx = 0.0
    for i in range(1, keep + 1):
        x = math.log(mus[i - 1])
        y = -math.log(1.0 - i / n)
        sxy += x * y
        sxx += x * x
    return sxy / sxx


def twonn(points, discard=0.1):
    """The TwoNN estimate from mu_i = r2 / r1 of each point."""
    nd = sorted_neighbor_distances(points, 2)
    return twonn_fit([t[1] / t[0] for t in nd], discard)


def twonn_mle(points):
    """The maximum likelihood estimate (N - 1) / sum ln mu_i under the Pareto law of mu (unbiased form)."""
    nd = sorted_neighbor_distances(points, 2)
    s = sum(math.log(t[1] / t[0]) for t in nd)
    return (len(nd) - 1) / s


def correlation_integral(points, r):
    """C(r) = the fraction of pairs i < j with ||x_i - x_j|| < r."""
    n = len(points)
    cnt = 0
    for i in range(n):
        for j in range(i + 1, n):
            if math.dist(points[i], points[j]) < r:
                cnt += 1
    return cnt / (n * (n - 1) / 2)


def correlation_dimension(points, radii):
    """The least squares slope of ln C(r) against ln r over the given radii."""
    xs, ys = [], []
    for r in radii:
        c = correlation_integral(points, r)
        if c > 0:
            xs.append(math.log(r))
            ys.append(math.log(c))
    m = len(xs)
    if m < 2:
        raise ValueError("need two radii with C(r) > 0")
    mx, my = sum(xs) / m, sum(ys) / m
    return sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)


def embed_cube(n, m, big_d, rng):
    """n uniform points of [0, 1]^m mapped into R^big_d by a random isometry (orthonormal columns)."""
    basis = []
    while len(basis) < m:
        v = [rng.gauss(0, 1) for _ in range(big_d)]
        for b in basis:
            c = sum(a * e for a, e in zip(v, b))
            v = [a - c * e for a, e in zip(v, b)]
        nv = math.sqrt(sum(a * a for a in v))
        basis.append([a / nv for a in v])
    pts = []
    for _ in range(n):
        u = [rng.random() for _ in range(m)]
        pts.append([sum(u[i] * basis[i][c] for i in range(m)) for c in range(big_d)])
    return pts
