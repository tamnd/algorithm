# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reference-governor/. The authors are listed in prov/JN3QT7.jsonl.

"""Scalar reference governor for a discrete-time closed loop.

The closed loop is x_(k+1) = A x_k + B v_k, y_k = C x_k + D v_k, with A Schur
and the constraint H y_k <= h (h > 0). The governor replaces the reference r_k
by v_k = v_(k-1) + kappa_k (r_k - v_(k-1)) with the largest kappa_k in [0, 1]
such that (x_k, v_k) lies in the set O of states and constant inputs whose
future outputs meet the constraint and whose steady state output meets it with
the margin eps.

Matrices are lists of rows and vectors are flat lists. With int or Fraction
data and tol = 0 every step is exact rational arithmetic.
"""

__all__ = ["lp_max", "build_admissible_set", "governor_step", "run", "admissible"]


def _mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def _eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def _solve(a, b):
    """Solve a X = b by Gaussian elimination with partial pivoting."""
    n = len(a)
    M = [list(a[i]) + list(b[i]) for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            raise ValueError("singular matrix")
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [[v / M[i][i] for v in M[i][n:]] for i in range(n)]


def _pivot(T, r, c):
    p = T[r][c]
    T[r] = [v / p for v in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            T[i] = [x - f * y for x, y in zip(T[i], T[r])]


def _simplex(T, basis, cost, tol):
    """Minimize cost . lam on the tableau T, which is in canonical form for basis.

    Bland's rule (smallest index enters, smallest basic index leaves on ties)
    prevents cycling. Returns False if the objective is unbounded below.
    """
    ncol = len(T[0]) - 1
    while True:
        enter = None
        for j in range(ncol):
            if j in basis:
                continue
            rj = cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(len(T)))
            if rj < -tol:
                enter = j
                break
        if enter is None:
            return True
        leave, best = None, None
        for i in range(len(T)):
            if T[i][enter] > tol:
                ratio = T[i][-1] / T[i][enter]
                if best is None or ratio < best - tol or (abs(ratio - best) <= tol and basis[i] < basis[leave]):
                    leave, best = i, ratio
        if leave is None:
            return False
        _pivot(T, leave, enter)
        basis[leave] = enter


def lp_max(c, G, g, tol=1e-10):
    """Return max c . z subject to G z <= g, z free, or None if unbounded.

    Needs g >= 0, so that z = 0 is feasible. Solves the dual LP
    min g . lam subject to G^T lam = c, lam >= 0 by the two-phase simplex method;
    by strong duality its value is the primal maximum.
    """
    d, N = len(c), len(G)
    T = []
    for i in range(d):
        row = [G[j][i] for j in range(N)] + [0] * d + [c[i]]
        if c[i] < 0:
            row = [-v for v in row]
        row[N + i] = 1
        T.append(row)
    basis = [N + i for i in range(d)]
    _simplex(T, basis, [0] * N + [1] * d, tol)  # phase 1 is bounded below by 0
    if sum(T[i][-1] for i in range(d) if basis[i] >= N) > tol * max(1, d):
        return None  # the dual is infeasible, so the primal is unbounded
    keep = []
    for i in range(d):
        if basis[i] >= N:
            j = next((j for j in range(N) if abs(T[i][j]) > tol), None)
            if j is None:
                continue  # redundant equation
            _pivot(T, i, j)
            basis[i] = j
        keep.append(i)
    T = [T[i][:N] + [T[i][-1]] for i in keep]
    basis = [basis[i] for i in keep]
    if not _simplex(T, basis, list(g), tol):
        raise ValueError("the primal LP is infeasible")
    return sum(g[basis[i]] * T[i][-1] for i in range(len(T)))


def build_admissible_set(A, B, C, D, H, h, eps, tol=1e-10, t_max=1000):
    """Return (rows, t_star): the rows (a, b) of a . (x, v) <= b that define O.

    O is the set of (x, v) with H y_t <= h for all t >= 0 when v is held
    constant from the state x, and H G0 v <= (1 - eps) h for the steady state
    gain G0 = C (I - A)^(-1) B + D. t_star is the first t whose rows were all
    redundant, so the rows of the times 0, ..., t_star - 1 define O.
    """
    n, m = len(A), len(B[0])
    if D is None:
        D = [[0] * m for _ in C]
    nH = len(H)
    G0 = _add(_mul(C, _solve(_add(_eye(n), [[-a for a in row] for row in A]), B)), D)  # @line L1
    HG0 = _mul(H, G0)
    rows = [([0] * n + HG0[i], (1 - eps) * h[i]) for i in range(nH)]
    Apow = _eye(n)
    SB = [[0] * m for _ in range(n)]  # S_t B with S_t = I + A + ... + A^(t-1)
    for t in range(t_max + 1):  # @line L2
        Hx = _mul(H, _mul(C, Apow))  # @line L3
        Hv = _mul(H, _add(_mul(C, SB), D))
        G = [a for a, _ in rows]
        g = [b for _, b in rows]
        new = []
        for i in range(nH):
            a = Hx[i] + Hv[i]
            val = lp_max(a, G, g, tol)  # @line L4
            if val is None or val > h[i] + tol:
                new.append((a, h[i]))
        if not new:
            return rows, t  # @line L4
        rows = rows + new  # @line L5
        SB = _add(B, _mul(A, SB))
        Apow = _mul(A, Apow)
    raise RuntimeError("O was not determined within t_max steps")


def admissible(rows, x, v, tol=0):
    """True if (x, v) satisfies every row."""
    z = list(x) + list(v)
    return all(sum(ai * zi for ai, zi in zip(a, z)) <= b + tol for a, b in rows)


def governor_step(rows, x, v_prev, r):
    """Return (v, kappa) with the largest kappa in [0, 1] such that (x, v) is in O."""
    n = len(x)
    d = [ri - vi for ri, vi in zip(r, v_prev)]
    kappa = 1  # @line L7
    for a, b in rows:
        beta = b - sum(ai * xi for ai, xi in zip(a[:n], x)) - sum(ai * vi for ai, vi in zip(a[n:], v_prev))
        alpha = sum(ai * di for ai, di in zip(a[n:], d))
        if alpha > 0 and beta < kappa * alpha:
            kappa = beta / alpha
    if kappa < 0:  # only rounding can make beta negative
        kappa = 0
    v = [vi + kappa * di for vi, di in zip(v_prev, d)]  # @line L8
    return v, kappa


def run(A, B, C, D, rows, x0, v_prev, refs):
    """Apply the governor to the references refs. Returns (xs, vs, ys, kappas)."""
    m = len(B[0])
    if D is None:
        D = [[0] * m for _ in C]
    x = list(x0)
    v = list(v_prev)
    xs, vs, ys, ks = [list(x)], [], [], []
    for r in refs:  # @line L6
        v, kappa = governor_step(rows, x, v, r)
        y = [sum(c * xi for c, xi in zip(Cr, x)) + sum(dd * vi for dd, vi in zip(Dr, v)) for Cr, Dr in zip(C, D)]
        x = [sum(a * xi for a, xi in zip(Ar, x)) + sum(b * vi for b, vi in zip(Br, v)) for Ar, Br in zip(A, B)]  # @line L8
        xs.append(x)
        vs.append(v)
        ys.append(y)
        ks.append(kappa)
    return xs, vs, ys, ks
