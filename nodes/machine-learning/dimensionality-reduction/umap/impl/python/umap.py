# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/umap/. The authors are listed in prov/FBD238.jsonl.

"""UMAP (McInnes, Healy and Melville 2018), Algorithms 1 to 5 of the paper, with dense matrices.

1. For each point, the k nearest neighbors (brute force), rho_i = the nearest distance, and
   sigma_i by bisection so that sum_j exp(-max(0, d_ij - rho_i) / sigma_i) = log2(k).
2. Directed memberships a_ij = exp(-max(0, d_ij - rho_i) / sigma_i) on the kNN edges.
3. Fuzzy union w_ij = a_ij + a_ji - a_ij a_ji.
4. Map curve 1 / (1 + a d^(2b)), with (a, b) fitted by least squares to the target curve
   psi(d) = 1 for d <= min_dist and exp(-(d - min_dist)) for d > min_dist.
5. Spectral start: eigenvectors of the normalized graph Laplacian, scaled to [0, 10].
6. SGD on the fuzzy cross entropy: each edge is sampled with probability w_ij; an attractive
   step moves both ends; then `neg` random points push the first end away.
"""

import math


def distances(points):
    n = len(points)
    return [[math.sqrt(sum((a - b) ** 2 for a, b in zip(points[i], points[j]))) for j in range(n)] for i in range(n)]


def nearest_neighbors(dist, k):
    """Indices of the k nearest neighbors of each point, the point itself excluded."""
    n = len(dist)
    return [sorted((j for j in range(n) if j != i), key=lambda j: (dist[i][j], j))[:k] for i in range(n)]


def smooth_knn(knn_dists, tol=1e-5, max_iter=64):
    """Return (rho, sigma) with rho = min distance and sum exp(-max(0, d - rho)/sigma) = log2(k)."""
    k = len(knn_dists)
    target = math.log2(k)
    rho = min(knn_dists)
    lo, hi, sigma = 0.0, math.inf, 1.0
    for _ in range(max_iter):
        s = sum(math.exp(-max(0.0, d - rho) / sigma) for d in knn_dists)
        if abs(s - target) <= tol:
            break
        if s > target:  # the sum grows with sigma, so sigma is too large
            hi = sigma
            sigma = (lo + hi) / 2.0
        else:
            lo = sigma
            sigma = sigma * 2.0 if hi == math.inf else (lo + hi) / 2.0
    return rho, sigma


def fuzzy_simplicial_set(points, k):
    """Directed memberships a[i][j] on the kNN graph (Algorithm 2 of the paper)."""
    dist = distances(points)
    n = len(points)
    a = [[0.0] * n for _ in range(n)]
    for i, nbrs in enumerate(nearest_neighbors(dist, k)):  # @line L1
        rho, sigma = smooth_knn([dist[i][j] for j in nbrs])  # @line L2
        for j in nbrs:
            a[i][j] = math.exp(-max(0.0, dist[i][j] - rho) / sigma)  # @line L3
    return a


def fuzzy_union(a):
    """w = A + A^T - A o A^T (the probabilistic t-conorm, entry by entry)."""
    n = len(a)
    return [[a[i][j] + a[j][i] - a[i][j] * a[j][i] for j in range(n)] for i in range(n)]


def fit_ab(min_dist, spread=1.0, points=300, iters=200):
    """Least squares fit of 1/(1 + a x^(2b)) to psi on 300 points in [0, 3 spread] (Levenberg-Marquardt)."""
    xs = [3.0 * spread * t / (points - 1) for t in range(points)]
    ys = [1.0 if x < min_dist else math.exp(-(x - min_dist) / spread) for x in xs]

    def residuals(a, b):
        r, ja, jb = [], [], []
        for x, y in zip(xs, ys):
            p = x ** (2.0 * b) if x > 0.0 else 0.0
            f = 1.0 / (1.0 + a * p)
            r.append(f - y)
            ja.append(-p * f * f)
            jb.append(-a * p * 2.0 * math.log(x) * f * f if x > 0.0 else 0.0)
        return r, ja, jb

    a, b, lam = 1.0, 1.0, 1e-3
    r, ja, jb = residuals(a, b)
    cost = sum(v * v for v in r)
    for _ in range(iters):
        g11 = sum(v * v for v in ja)
        g22 = sum(v * v for v in jb)
        g12 = sum(u * v for u, v in zip(ja, jb))
        r1 = sum(u * v for u, v in zip(ja, r))
        r2 = sum(u * v for u, v in zip(jb, r))
        h11, h22 = g11 * (1.0 + lam), g22 * (1.0 + lam)
        det = h11 * h22 - g12 * g12
        da = -(h22 * r1 - g12 * r2) / det
        db = -(h11 * r2 - g12 * r1) / det
        r_new, ja_new, jb_new = residuals(a + da, b + db)
        new_cost = sum(v * v for v in r_new)
        if new_cost < cost:
            a, b, r, ja, jb, lam = a + da, b + db, r_new, ja_new, jb_new, lam / 10.0
            done = cost - new_cost < 1e-15 * max(cost, 1e-300)
            cost = new_cost
            if done:
                break
        else:
            lam *= 10.0
            if lam > 1e12:
                break
    return a, b


def jacobi_eigen(s, sweeps=100):
    """Eigenvalues and eigenvectors (as columns of V) of a symmetric matrix by cyclic Jacobi rotations."""
    n = len(s)
    a = [row[:] for row in s]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for r in range(n):
                    arp, arq = a[r][p], a[r][q]
                    a[r][p], a[r][q] = c * arp - sn * arq, sn * arp + c * arq
                for r in range(n):
                    apr, aqr = a[p][r], a[q][r]
                    a[p][r], a[q][r] = c * apr - sn * aqr, sn * apr + c * aqr
                for r in range(n):
                    vrp, vrq = v[r][p], v[r][q]
                    v[r][p], v[r][q] = c * vrp - sn * vrq, sn * vrp + c * vrq
    return [a[i][i] for i in range(n)], v


def spectral_init(w, dim):
    """Eigenvectors 2..dim+1 of L = I - D^(-1/2) W D^(-1/2) (smallest eigenvalues), each scaled to [0, 10]."""
    n = len(w)
    deg = [sum(row) for row in w]
    s = [[(1.0 if i == j else 0.0) - w[i][j] / math.sqrt(deg[i] * deg[j]) for j in range(n)] for i in range(n)]
    vals, vecs = jacobi_eigen(s)
    order = sorted(range(n), key=lambda i: vals[i])[1:dim + 1]
    y = [[vecs[i][c] for c in order] for i in range(n)]
    for c in range(dim):
        lo, hi = min(r[c] for r in y), max(r[c] for r in y)
        for r in y:
            r[c] = 10.0 * (r[c] - lo) / (hi - lo) if hi > lo else 0.0
    return y


def attract_coeff(d2, a, b):
    """-2ab d^(2(b-1)) / (1 + a d^(2b)): the step along (y_i - y_j) for -log v, v = 1/(1 + a d^(2b))."""
    return -2.0 * a * b * d2 ** (b - 1.0) / (1.0 + a * d2 ** b) if d2 > 0.0 else 0.0


def repel_coeff(d2, a, b, eps=0.001):
    """2b / ((eps + d^2)(1 + a d^(2b))): the step along (y_i - y_c) for -log(1 - v)."""
    return 2.0 * b / ((eps + d2) * (1.0 + a * d2 ** b))


def _clip(v, c=4.0):
    return max(-c, min(c, v))


def umap(points, rng, k=5, dim=2, min_dist=0.1, epochs=200, neg=5):
    """Fit a UMAP embedding; rng is a random.Random. Returns (Y, W)."""
    n = len(points)
    w = fuzzy_union(fuzzy_simplicial_set(points, k))  # @line L4
    a, b = fit_ab(min_dist)  # @line L5
    y = spectral_init(w, dim)  # @line L6
    edges = [(i, j, w[i][j]) for i in range(n) for j in range(n) if w[i][j] > 0.0]
    for e in range(epochs):  # @line L7
        alpha = 1.0 - e / epochs  # @line L8
        for i, j, p in edges:
            if rng.random() > p:  # @line L9
                continue
            d2 = sum((u - v) ** 2 for u, v in zip(y[i], y[j]))
            g = attract_coeff(d2, a, b)
            for t in range(dim):  # @line L10
                step = _clip(g * (y[i][t] - y[j][t])) * alpha
                y[i][t] += step
                y[j][t] -= step
            for _ in range(neg):  # @line L11
                c = rng.randrange(n)
                if c == i:
                    continue
                d2 = sum((u - v) ** 2 for u, v in zip(y[i], y[c]))
                g = repel_coeff(d2, a, b)
                for t in range(dim):
                    y[i][t] += _clip(g * (y[i][t] - y[c][t])) * alpha
    return y, w  # @line L12
