# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-greedy-reduced-basis/. The authors are listed in prov/3WNNGB.jsonl.
"""Weak greedy construction of a reduced basis, driven by the residual based error bound.

The model problem is -u'' + mu u = 1 on (0, 1) with u(0) = u(1) = 0 and mu > 0, in P1 finite
elements: A(mu) = K + mu M. All matrices are tridiagonal, so the truth solves cost O(n).
"""

import math

from scimat import dot, matvec, solve

Matrix = list[list[float]]
Vector = list[float]


def fe_model(n: int) -> tuple[list[Matrix], Vector]:
    """Return ([K, M], F) for P1 elements with n interior nodes and h = 1/(n+1)."""
    h = 1.0 / (n + 1)
    k = [[0.0] * n for _ in range(n)]
    m = [[0.0] * n for _ in range(n)]
    for i in range(n):
        k[i][i] = 2.0 / h
        m[i][i] = 4.0 * h / 6.0
        if i > 0:
            k[i][i - 1] = k[i - 1][i] = -1.0 / h
            m[i][i - 1] = m[i - 1][i] = h / 6.0
    return [k, m], [h] * n


def combine(aq: list[Matrix], th: Vector) -> Matrix:
    """Return sum over q of th[q] A_q."""
    n = len(aq[0])
    return [[sum(t * a[i][j] for t, a in zip(th, aq)) for j in range(n)] for i in range(n)]


def tridiag_solve(a: Matrix, b: Vector) -> Vector:
    """Solve a x = b for a tridiagonal a (stored dense) by elimination without pivoting."""
    n = len(b)
    c = [0.0] * n
    d = [0.0] * n
    for i in range(n):
        lo = a[i][i - 1] if i > 0 else 0.0
        den = a[i][i] - (lo * c[i - 1] if i > 0 else 0.0)
        c[i] = (a[i][i + 1] / den) if i < n - 1 else 0.0
        d[i] = (b[i] - (lo * d[i - 1] if i > 0 else 0.0)) / den
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = d[i] - (c[i] * x[i + 1] if i < n - 1 else 0.0)
    return x


class ReducedBasis:
    """A reduced basis with its offline tables, grown one snapshot at a time."""

    def __init__(self, aq: list[Matrix], f: Vector, x: Matrix, mu_bar: float):
        self.aq, self.f, self.x, self.mu_bar = aq, f, x, mu_bar
        nq = len(aq)
        self.z: list[Vector] = []  # X-orthonormal basis vectors
        self.az: list[list[Vector]] = [[] for _ in aq]  # A_q z_j
        self.ez: list[list[Vector]] = [[] for _ in aq]  # X^-1 A_q z_j
        # small tables of the online stage; their sizes do not depend on n
        self.ar: list[Matrix] = [[] for _ in aq]  # ar[q][i][j] = z_i^T A_q z_j
        self.fr: Vector = []  # fr[j] = F^T z_j
        self.g: list[Vector] = [[] for _ in aq]  # g[q][j] = F^T X^-1 A_q z_j
        self.gg: list[list[Matrix]] = [[[] for _ in aq] for _ in range(nq)]  # gg[q][p][i][j] = (A_q z_i)^T X^-1 A_p z_j
        ef = tridiag_solve(x, f)
        self.gff = dot(f, ef)

    def truth(self, mu: float) -> Vector:
        return tridiag_solve(combine(self.aq, [1.0, mu]), self.f)

    def add(self, u: Vector) -> None:
        """Add a snapshot: Gram-Schmidt in X (two passes) and the new table entries."""
        w = list(u)
        for _ in range(2):
            for zj in self.z:
                c = dot(zj, matvec(self.x, w))
                w = [wi - c * zi for wi, zi in zip(w, zj)]
        nw = math.sqrt(dot(w, matvec(self.x, w)))
        if nw <= 1e-10 * math.sqrt(dot(u, matvec(self.x, u))):
            raise ValueError("the new snapshot is in the span of the basis")
        z = [wi / nw for wi in w]
        self.z.append(z)
        k = len(self.z) - 1
        for q, a in enumerate(self.aq):
            v = matvec(a, z)
            self.az[q].append(v)
            self.ez[q].append(tridiag_solve(self.x, v))
        self.fr.append(dot(self.f, z))
        nq = len(self.aq)
        for q in range(nq):
            for i in range(k):
                self.ar[q][i].append(dot(self.z[i], self.az[q][k]))
            self.ar[q].append([dot(z, self.az[q][j]) for j in range(k + 1)])
            self.g[q].append(dot(self.f, self.ez[q][k]))
            for p in range(nq):
                for i in range(k):
                    self.gg[q][p][i].append(dot(self.az[q][i], self.ez[p][k]))
                self.gg[q][p].append([dot(self.az[q][k], self.ez[p][j]) for j in range(k + 1)])

    def online(self, mu: float) -> tuple[Vector, float]:
        """Return the coefficients c of u_r(mu) = Z c and the bound Delta(mu), from the small tables only."""
        th = [1.0, mu]
        r = len(self.z)
        nq = len(th)
        ar = [[sum(th[q] * self.ar[q][i][j] for q in range(nq)) for j in range(r)] for i in range(r)]
        c = solve(ar, self.fr)
        res2 = self.gff
        for q in range(nq):
            res2 -= 2.0 * th[q] * sum(c[j] * self.g[q][j] for j in range(r))
            for p in range(nq):
                res2 += th[q] * th[p] * sum(c[i] * c[j] * self.gg[q][p][i][j] for i in range(r) for j in range(r))
        alpha_lb = min(1.0, mu / self.mu_bar)
        return c, math.sqrt(max(res2, 0.0)) / alpha_lb

    def lift(self, c: Vector) -> Vector:
        return [sum(cj * zj[i] for cj, zj in zip(c, self.z)) for i in range(len(self.f))]


def weak_greedy(aq: list[Matrix], f: Vector, x: Matrix, mu_bar: float, train: list[float], tol: float, r_max: int) -> tuple[ReducedBasis, list[float], list[float]]:
    """Build a reduced basis by the weak greedy algorithm over the training set train.

    Return the basis, the chosen parameters and the list eps_0, eps_1, ... of the largest
    bound over train after each step (eps_0 is the bound of the empty basis, ||F||_X' / alpha_LB).
    Stop when the largest bound is at most tol or the basis has r_max vectors.
    """
    rb = ReducedBasis(aq, f, x, mu_bar)
    chosen: list[float] = []
    eps = [max(math.sqrt(rb.gff) / min(1.0, mu / mu_bar) for mu in train)]
    mu = max(train, key=lambda m: math.sqrt(rb.gff) / min(1.0, m / mu_bar))  # @line L1: mu_1 maximizes the bound of the empty basis
    while True:  # @line L2
        rb.add(rb.truth(mu))  # @line L3: one truth solve, then extend the basis and the tables
        chosen.append(mu)
        bounds = [rb.online(m)[1] for m in train]  # @line L4: the bound at every training point, online
        k = max(range(len(train)), key=lambda i: bounds[i])  # @line L5
        eps.append(bounds[k])
        if bounds[k] <= tol or len(chosen) >= r_max:  # @line L6
            return rb, chosen, eps  # @line L7
        mu = train[k]  # @line L8
