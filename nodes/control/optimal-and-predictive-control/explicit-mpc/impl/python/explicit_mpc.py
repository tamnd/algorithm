# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/explicit-mpc/. The authors are listed in prov/6TK6XY.jsonl.

"""Explicit linear MPC: the solution of the MPC quadratic program as a
piecewise affine function of the state, computed offline.

The MPC problem is the multiparametric QP (mp-QP)

    minimize over z   1/2 z^T H z + x^T F^T z
    subject to        G z <= w + E x,

with H positive definite, the decision z (the stacked inputs) and the
parameter x (the current state). For a set A of constraint rows with linearly
independent rows G_A, the KKT conditions with exactly these rows active give

    lambda_A(x) = -(G_A H^-1 G_A^T)^-1 (w_A + (E_A + G_A H^-1 F) x),
    z(x)        = -H^-1 (F x + G_A^T lambda_A(x)),

both affine in x. The critical region of A is the polyhedron of the x where
z(x) is feasible and lambda_A(x) >= 0. The offline part enumerates the
candidate sets, keeps the regions that have an interior point inside a box
of states, and stores (region, gain, offset). The online part finds the
region that contains x by sequential search and evaluates the affine law.

The enumeration visits every set of at most dim(z) rows, so the offline cost
is exponential in the number of constraints. This is the simplest correct
method; the geometric exploration of Bemporad, Morari, Dua and Pistikopoulos
(2002) and the combinatorial method of Gupta et al. (2011) visit fewer sets.
"""

from itertools import combinations

__all__ = ["mpc_to_mpqp", "explicit_mpc", "evaluate", "chebyshev_radius", "Region"]


def _mul(a, b):
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def _matvec(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def _t(a):
    return [list(c) for c in zip(*a)]


def _solve(a, b, tol=1e-12):
    """Solve a x = b (b a matrix) by Gaussian elimination; None if singular."""
    n = len(a)
    aa = [list(map(float, r)) + list(map(float, br)) for r, br in zip(a, b)]
    k = len(b[0])
    scale = max((abs(v) for r in a for v in r), default=1.0) or 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(aa[r][c]))
        if abs(aa[p][c]) <= tol * scale:
            return None
        aa[c], aa[p] = aa[p], aa[c]
        for r in range(n):
            if r != c and aa[r][c] != 0.0:
                f = aa[r][c] / aa[c][c]
                aa[r] = [x - f * y for x, y in zip(aa[r], aa[c])]
    return [[aa[i][n + j] / aa[i][i] for j in range(k)] for i in range(n)]


def mpc_to_mpqp(A, B, Q, R, P, N, umin, umax, xmin=None, xmax=None):
    """Return (H, F, G, w, E) of the condensed MPC problem.

    Cost sum_(k<N) x_k^T Q x_k + u_k^T R u_k + x_N^T P x_N, halved, so the
    objective is 1/2 z^T H z + x^T F^T z plus a constant. Constraints:
    umin <= u_k <= umax for k < N and, if given, xmin <= x_k <= xmax for
    k = 1..N.
    """
    n, m = len(A), len(B[0])
    powers = [[[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]]
    for _ in range(N):
        powers.append(_mul(A, powers[-1]))
    phi = [row for k in range(1, N + 1) for row in powers[k]]
    gamma = [[0.0] * (N * m) for _ in range(N * n)]
    for k in range(1, N + 1):
        for j in range(k):
            blk = _mul(powers[k - 1 - j], B)
            for i in range(n):
                for c in range(m):
                    gamma[(k - 1) * n + i][j * m + c] = blk[i][c]
    qbar = [[0.0] * (N * n) for _ in range(N * n)]
    for k in range(N):
        W = P if k == N - 1 else Q
        for i in range(n):
            for j in range(n):
                qbar[k * n + i][k * n + j] = W[i][j]
    gq = _mul(_t(gamma), qbar)
    H = _mul(gq, gamma)
    for k in range(N):
        for i in range(m):
            for j in range(m):
                H[k * m + i][k * m + j] += R[i][j]
    F = _mul(gq, phi)
    G, w, E = [], [], []
    for k in range(N):
        for c in range(m):
            e = [0.0] * (N * m)
            e[k * m + c] = 1.0
            G += [e, [-v for v in e]]
            w += [umax[c], -umin[c]]
            E += [[0.0] * n, [0.0] * n]
    if xmax is not None:
        for r in range(N * n):
            G += [gamma[r], [-v for v in gamma[r]]]
            w += [xmax[r % n], -xmin[r % n]]
            E += [[-v for v in phi[r]], list(phi[r])]
    return H, F, G, w, E


def _lp_max(c, rows, b, tol=1e-9):
    """Maximize c^T y subject to rows y <= b, y free (two phase simplex).

    Returns the optimal value, None if infeasible, or inf if unbounded.
    """
    n, mr = len(c), len(rows)
    arts = [i for i in range(mr) if b[i] < 0]
    ncols = 2 * n + mr + len(arts)
    T, basis = [], []
    for i, (row, bi) in enumerate(zip(rows, b)):
        line = list(row) + [-v for v in row] + [1.0 if j == i else 0.0 for j in range(mr)]
        line += [0.0] * len(arts) + [float(bi)]
        if bi < 0:
            line = [-v for v in line]
            a = 2 * n + mr + arts.index(i)
            line[a] = 1.0
            basis.append(a)
        else:
            basis.append(2 * n + i)
        T.append(line)

    def run(cost, ncol):
        while True:
            enter = None
            for j in range(ncol):
                if j not in basis:
                    rc = cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(mr))
                    if rc > tol:
                        enter = j
                        break
            if enter is None:
                return True
            leave, best = None, None
            for i in range(mr):
                if T[i][enter] > tol:
                    ratio = T[i][-1] / T[i][enter]
                    if best is None or ratio < best - tol or (abs(ratio - best) <= tol and basis[i] < basis[leave]):
                        best, leave = ratio, i
            if leave is None:
                return False
            piv = T[leave][enter]
            T[leave] = [v / piv for v in T[leave]]
            for i in range(mr):
                if i != leave and T[i][enter] != 0.0:
                    f = T[i][enter]
                    T[i] = [x - f * y for x, y in zip(T[i], T[leave])]
            basis[leave] = enter

    if arts:
        art_cols = set(range(2 * n + mr, ncols))
        run([0.0] * (2 * n + mr) + [-1.0] * len(arts), ncols)
        if sum(T[i][-1] for i in range(mr) if basis[i] in art_cols) > tol:
            return None
        for i in range(mr):
            if basis[i] in art_cols:
                for j in range(2 * n + mr):
                    if abs(T[i][j]) > tol and j not in basis:
                        piv = T[i][j]
                        T[i] = [v / piv for v in T[i]]
                        for r in range(mr):
                            if r != i and T[r][j] != 0.0:
                                f = T[r][j]
                                T[r] = [x - f * y for x, y in zip(T[r], T[i])]
                        basis[i] = j
                        break
        for row in T:
            for j in art_cols:
                row[j] = 0.0
    cost = list(c) + [-v for v in c] + [0.0] * (mr + len(arts))
    if not run(cost, 2 * n + mr):
        return float("inf")
    y = [0.0] * ncols
    for i, j in enumerate(basis):
        y[j] = T[i][-1]
    return sum(ci * (y[j] - y[n + j]) for j, ci in enumerate(c))


def chebyshev_radius(rows, b):
    """Radius of the largest ball inside {x : rows x <= b}; None if empty."""
    n = len(rows[0])
    ext = [list(r) + [sum(v * v for v in r) ** 0.5] for r in rows]
    ext.append([0.0] * n + [-1.0])  # r >= 0
    v = _lp_max([0.0] * n + [1.0], ext, list(b) + [0.0])
    return v


class Region:
    """A critical region {x : Ax x <= bx} with the law z = K x + k."""

    def __init__(self, active, Ax, bx, K, k, L, l):
        self.active, self.Ax, self.bx = active, Ax, bx
        self.K, self.k, self.L, self.l = K, k, L, l

    def contains(self, x, tol=1e-9):
        return all(sum(a * v for a, v in zip(r, x)) <= bi + tol for r, bi in zip(self.Ax, self.bx))

    def law(self, x):
        return [v + c for v, c in zip(_matvec(self.K, x), self.k)]

    def multipliers(self, x):
        return [v + c for v, c in zip(_matvec(self.L, x), self.l)]


def explicit_mpc(H, F, G, w, E, xbox, eps=1e-7):
    """Return the list of full-dimensional critical regions inside |x_i| <= xbox_i."""
    nz, nx, q = len(H), len(F[0]), len(G)
    Hinv = _solve(H, [[1.0 if i == j else 0.0 for j in range(nz)] for i in range(nz)])
    HiF = _mul(Hinv, F)
    box_rows = []
    box_b = []
    for i in range(nx):
        e = [0.0] * nx
        e[i] = 1.0
        box_rows += [e, [-1.0 * v for v in e]]
        box_b += [xbox[i], xbox[i]]
    regions = []  # @line L1
    for size in range(0, nz + 1):
        for act in combinations(range(q), size):  # @line L2
            GA = [G[i] for i in act]
            if act:
                M = _mul(_mul(GA, Hinv), _t(GA))  # @line L3
                Minv = _solve(M, [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)])
                if Minv is None:  # rows of G_A are dependent (LICQ fails)
                    continue
                S = [[e + s for e, s in zip(E[i], srow)] for i, srow in zip(act, _mul(GA, HiF))]
                L = [[-v for v in r] for r in _mul(Minv, S)]  # @line L4
                l = [-v for v in _matvec(Minv, [w[i] for i in act])]
                GtL = _mul(_t(GA), L)
                Gtl = _matvec(_t(GA), l)
            else:
                L, l = [], []
                GtL, Gtl = [[0.0] * nx for _ in range(nz)], [0.0] * nz
            K = [[-v for v in r] for r in _mul(Hinv, [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(F, GtL)])]  # @line L5
            k = [-v for v in _matvec(Hinv, Gtl)]
            rows, b = list(box_rows), list(box_b)  # @line L6
            GK = _mul(G, K)
            Gk = _matvec(G, k)
            for i in range(q):  # G (K x + k) <= w + E x
                rows.append([gk - e for gk, e in zip(GK[i], E[i])])
                b.append(w[i] - Gk[i])
            for j in range(size):  # lambda(x) = L x + l >= 0
                rows.append([-v for v in L[j]])
                b.append(l[j])
            r = chebyshev_radius(rows, b)  # @line L7
            if r is not None and r > eps:
                keep = [i for i in range(len(rows)) if any(abs(v) > 1e-12 for v in rows[i])]
                regions.append(Region(act, [rows[i] for i in keep], [b[i] for i in keep], K, k, L, l))
    return regions  # @line L8


def evaluate(regions, x, m=None, tol=1e-9):
    """Return (z(x), region index) by sequential search; (None, None) if x is in no region."""
    for idx, reg in enumerate(regions):  # @line L9
        if reg.contains(x, tol):  # @line L10
            z = reg.law(x)
            return (z if m is None else z[:m]), idx
    return None, None  # @line L11
