# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-pca/. The authors are listed in prov/0NPZBY.jsonl.

"""Incremental PCA with mean update (Ross, Lim, Lin and Yang 2008, Figure 1).

The state holds the mean, the effective number of points n, and a thin SVD
U diag(sigma) of the centered data seen so far (U is d x r, stored as r columns).
update() adds a batch of m points. The covariance (divisor n) of the data seen
so far has the eigenvalues sigma_j^2 / n. With f = 1 and k at least the rank
of the data, the result equals batch PCA up to the signs of the components.
"""

import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def one_sided_jacobi(a, tol=1e-15, max_sweeps=60):
    """Hestenes one-sided Jacobi on the columns of a (rows x c).
    Returns (v, s): a v has orthogonal columns with the norms s, and v is c x c orthogonal.
    So a = (a v diag(1/s)) diag(s) v^T is an SVD, and v holds the right singular vectors."""
    rows, c = len(a), len(a[0])
    cols = [[a[i][j] for i in range(rows)] for j in range(c)]
    v = [[1.0 if i == j else 0.0 for i in range(c)] for j in range(c)]  # v[j] is column j of V
    for _ in range(max_sweeps):
        rotated = False
        for p in range(c - 1):
            for q in range(p + 1, c):
                alpha, beta, gamma = dot(cols[p], cols[p]), dot(cols[q], cols[q]), dot(cols[p], cols[q])
                if abs(gamma) <= tol * math.sqrt(alpha * beta) or gamma == 0.0:
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(1.0, zeta) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                cs = 1.0 / math.sqrt(1.0 + t * t)
                sn = cs * t
                for vec in (cols, v):
                    xp, xq = vec[p], vec[q]
                    vec[p] = [cs * x - sn * y for x, y in zip(xp, xq)]
                    vec[q] = [sn * x + cs * y for x, y in zip(xp, xq)]
        if not rotated:
            break
    s = [math.sqrt(dot(col, col)) for col in cols]
    return v, s


def orth(vectors, scale, tol=1e-12):
    """Orthonormal basis of the span of the given vectors, by modified Gram-Schmidt
    applied twice. Vectors whose remaining norm is below tol * scale are dropped."""
    basis = []
    for vec in vectors:
        w = list(vec)
        for _ in range(2):
            for b in basis:
                c = dot(b, w)
                w = [x - c * y for x, y in zip(w, b)]
        norm = math.sqrt(dot(w, w))
        if norm > tol * scale:
            basis.append([x / norm for x in w])
    return basis


class IncrementalPCA:
    def __init__(self, d, k, forget=1.0):
        self.d, self.k, self.forget = d, k, forget
        self.n = 0.0
        self.mean = [0.0] * d
        self.u = []  # orthonormal columns, each a list of d numbers
        self.sigma = []  # singular values, decreasing

    def update(self, batch):
        d, f, m = self.d, self.forget, len(batch)
        n, mu_a = self.n, self.mean
        mu_b = [sum(row[j] for row in batch) / m for j in range(d)]  # @line L1
        self.mean = [(f * n * a + m * b) / (f * n + m) for a, b in zip(mu_a, mu_b)]
        bhat = [[row[j] - mu_b[j] for j in range(d)] for row in batch]  # @line L2
        if n > 0:
            w = math.sqrt(n * m / (n + m))
            bhat.append([w * (b - a) for a, b in zip(mu_a, mu_b)])
        proj = [[dot(u, col) for col in bhat] for u in self.u]  # @line L3
        resid = [[col[i] - sum(proj[r][c] * self.u[r][i] for r in range(len(self.u))) for i in range(d)]
                 for c, col in enumerate(bhat)]
        scale = max([math.sqrt(dot(c, c)) for c in bhat] + self.sigma + [1.0])
        btilde = orth(self.u + resid, scale)[len(self.u):]  # @line L4
        r, p, c = len(self.u), len(btilde), len(self.u) + len(bhat)
        big = [[0.0] * c for _ in range(r + p)]  # @line L5
        for i in range(r):
            big[i][i] = f * self.sigma[i]
            for j, col in enumerate(bhat):
                big[i][r + j] = proj[i][j]
        for i, bt in enumerate(btilde):
            for j, col in enumerate(resid):
                big[r + i][r + j] = dot(bt, col)
        transposed = [[big[i][j] for i in range(r + p)] for j in range(c)]
        utilde, s = one_sided_jacobi(transposed)  # @line L6
        order = sorted(range(r + p), key=lambda j: -s[j])[: self.k]
        basis = self.u + btilde
        self.u = [[sum(utilde[j][t] * basis[t][i] for t in range(r + p)) for i in range(d)] for j in order]  # @line L7
        self.sigma = [s[j] for j in order]
        self.n = f * n + m
        return self  # @line L8

    def eigenvalues(self):
        """Eigenvalues of the covariance (divisor n) along the kept components."""
        return [s * s / self.n for s in self.sigma]

    def components(self):
        """The components, with the sign fixed so that the largest entry is positive."""
        out = []
        for u in self.u:
            big = max(range(self.d), key=lambda i: abs(u[i]))
            out.append([-x for x in u] if u[big] < 0 else list(u))
        return out

    def transform(self, x):
        return [[dot(u, [a - b for a, b in zip(row, self.mean)]) for u in self.u] for row in x]
