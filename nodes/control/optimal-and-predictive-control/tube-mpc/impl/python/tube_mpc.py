# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tube-mpc/. The authors are listed in prov/ZNT0ZQ.jsonl.

"""Tube MPC for x+ = A x + B u + w with w in a zonotope W.

The control is u = v + K (x - z), where z, v are the nominal state and input
and A + B K is Schur. The error e = x - z then stays in a robust positively
invariant set Z, an outer bound of the minimal one by the method of Rakovic,
Kerrigan, Kouramas and Mayne (2005). The nominal plan uses the tightened sets
X - Z and U - K Z, the terminal constraint z_N = 0, and the 1-norm cost
sum (|Q z_k|_1 + |R v_k|_1), so each sample solves one linear program. The
first nominal state z_0 is a decision variable with x - z_0 in Z.

Matrices are lists of rows, vectors flat lists. Sets are zonotopes given by a
list of generators (centered at 0) or polyhedra given by rows (a, b) for
a . x <= b. The LP solver is a dense two-phase simplex method with Bland's
rule; with Fraction data and tol = 0 everything is exact.
"""

import itertools
from fractions import Fraction

__all__ = ["lp_min", "support", "zonotope_rows", "rpi_outer", "tighten", "tube_mpc", "closed_loop"]


def _pivot(T, obj, r, c):
    p = T[r][c]
    if isinstance(p, int):
        p = Fraction(p)  # int / int would give a float
    prow = [v / p for v in T[r]]
    T[r] = prow
    nzj = [j for j, v in enumerate(prow) if v != 0]
    for row in T + [obj]:
        if row is not prow and row[c] != 0:
            f = row[c]
            for j in nzj:
                row[j] -= f * prow[j]


def _simplex(T, obj, basis, tol, limit):
    while True:
        enter = next((j for j in range(limit) if obj[j] < -tol), None)
        if enter is None:
            return True
        leave, best = None, None
        for i, row in enumerate(T):
            if row[enter] > tol:
                ratio = row[-1] / row[enter]
                if best is None or ratio < best - tol or (abs(ratio - best) <= tol and basis[i] < basis[leave]):
                    leave, best = i, ratio
        if leave is None:
            return False
        _pivot(T, obj, leave, enter)
        basis[leave] = enter


def lp_min(c, G, g, E=(), e=(), nonneg=(), tol=1e-9):
    """Minimize c . z subject to G z <= g and E z = e; variables in nonneg are >= 0.

    Returns (value, z), or None if infeasible. Raises ValueError if unbounded.
    With tol = 0 the data are used as given (exact for Fractions); otherwise
    they are converted to floats, since mixed Fraction and float arithmetic is slow.
    """
    if tol:
        c, g, e = [float(v) for v in c], [float(v) for v in g], [float(v) for v in e]
        G, E = [[float(v) for v in r] for r in G], [[float(v) for v in r] for r in E]
    n = len(c)
    nonneg = set(nonneg)
    free = [j for j in range(n) if j not in nonneg]
    neg_col = {j: n + i for i, j in enumerate(free)}
    nz = n + len(free)
    ns = len(G)
    rows = [(a, b, True) for a, b in zip(G, g)] + [(a, b, False) for a, b in zip(E, e)]
    need_art = [i for i, (a, b, ineq) in enumerate(rows) if b < 0 or not ineq]
    art_col = {i: nz + ns + k for k, i in enumerate(need_art)}
    ncol = nz + ns + len(need_art)
    T, basis = [], []
    for i, (a, b, ineq) in enumerate(rows):
        row = [0] * (ncol + 1)
        for j in range(n):
            row[j] = a[j]
            if j in neg_col:
                row[neg_col[j]] = -a[j]
        if ineq:
            row[nz + i] = 1
        row[-1] = b
        if b < 0:
            row = [-v for v in row]
        if i in art_col:
            row[art_col[i]] = 1
        T.append(row)
        basis.append(art_col.get(i, nz + i))
    if need_art:
        obj = [0] * (ncol + 1)
        for i in need_art:
            for j in range(ncol + 1):
                if j < nz + ns or j == ncol:
                    obj[j] -= T[i][j]
        _simplex(T, obj, basis, tol, ncol)
        if -obj[-1] > tol * max(1, len(need_art)):
            return None
        keep = []
        for i in range(len(T)):
            if basis[i] >= nz + ns:
                j = next((j for j in range(nz + ns) if abs(T[i][j]) > tol), None)
                if j is None:
                    continue
                _pivot(T, obj, i, j)
                basis[i] = j
            keep.append(i)
        T = [T[i][:nz + ns] + [T[i][-1]] for i in keep]
        basis = [basis[i] for i in keep]
    else:
        T = [row[:nz + ns] + [row[-1]] for row in T]
    cost = list(c) + [-c[j] for j in free] + [0] * ns
    obj = cost + [0]
    for i, j in enumerate(basis):
        if cost[j] != 0:
            f = cost[j]
            obj = [o - f * t for o, t in zip(obj, T[i])]
    if not _simplex(T, obj, basis, tol, nz + ns):
        raise ValueError("the LP is unbounded")
    val = [0] * (nz + ns)
    for i, j in enumerate(basis):
        val[j] = T[i][-1]
    z = [val[j] - (val[neg_col[j]] if j in neg_col else 0) for j in range(n)]
    return sum(ci * zi for ci, zi in zip(c, z)), z


def _matvec(M, x):
    return [sum(a * b for a, b in zip(row, x)) for row in M]


def _matmul(M, N):
    return [[sum(M[i][k] * N[k][j] for k in range(len(N))) for j in range(len(N[0]))] for i in range(len(M))]


def _det(M):
    M = [list(r) for r in M]
    n, d = len(M), 1
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d = d * M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / (Fraction(M[c][c]) if isinstance(M[c][c], int) else M[c][c])
            M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return d


def support(gens, a):
    """Support function of the zonotope with these generators: max a . z over the set."""
    return sum(abs(sum(ai * gi for ai, gi in zip(a, g))) for g in gens)


def zonotope_rows(gens, n):
    """Rows (c, b) with c . z <= b that describe the zonotope; one pair per facet normal."""
    if n == 1:
        b = support(gens, [1])
        return [([1], b), ([-1], b)]
    rows = []
    for S in itertools.combinations(gens, n - 1):
        # Normal of the hyperplane spanned by S: the cofactors of the n x (n - 1) matrix [S].
        c = [(-1) ** i * _det([[g[r] for g in S] for r in range(n) if r != i]) for i in range(n)]
        if any(ci != 0 for ci in c):
            b = support(gens, c)
            rows += [(c, b), ([-ci for ci in c], b)]
    return rows


def rpi_outer(AK, W, alpha_max=Fraction(1, 10), s_max=200):
    """Return (s, alpha, Z) with A_K^s W in alpha W and Z = (1 - alpha)^-1 (W + A_K W + ... + A_K^(s-1) W)."""
    n = len(AK)
    Wrows = zonotope_rows(W, n)
    P = [[1 if i == j else 0 for j in range(n)] for i in range(n)]  # A_K^s
    for s in range(1, s_max + 1):  # @line L1
        P = _matmul(AK, P)
        AsW = [_matvec(P, g) for g in W]
        alpha = max(support(AsW, c) / b for c, b in Wrows)
        if alpha <= alpha_max:
            scale = 1 / (1 - Fraction(alpha) if not isinstance(alpha, float) else 1 - alpha)
            Z, Pi = [], [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            for _ in range(s):
                Z += [[scale * v for v in _matvec(Pi, g)] for g in W]
                Pi = _matmul(AK, Pi)
            return s, alpha, Z
    raise ValueError("A_K^s W is not inside alpha_max W for s <= s_max")


def tighten(rows, Z, M=None):
    """Rows of S - M Z for S = {a . y <= b}: each b becomes b - h_Z(M^T a)."""
    out = []
    for a, b in rows:  # @line L2
        aa = a if M is None else [sum(a[i] * M[i][j] for i in range(len(M))) for j in range(len(M[0]))]
        out.append((a, b - support(Z, aa)))
    return out


def tube_mpc(A, B, Z, Zrows, x, N, Q, R, Xbar, Ubar, tol=1e-9):
    """Solve the nominal LP from the measured state x. Returns (value, z0, vs, zs) or None."""
    n, m = len(A), len(B[0])
    nv = n + N * m  # decision variables z0 and v_0..v_(N-1); the z_k are affine in them
    # z_k = Phi_k z0 + sum_j Gam_(k,j) v_j, stored as rows over the nv variables.
    zs_aff = [[[1 if c == i else 0 for c in range(nv)] for i in range(n)]]
    for k in range(N):
        prev = zs_aff[-1]
        nxt = []
        for i in range(n):
            r = [sum(A[i][l] * prev[l][c] for l in range(n)) for c in range(nv)]
            for j in range(m):
                r[n + k * m + j] += B[i][j]
            nxt.append(r)
        zs_aff.append(nxt)
    # Epigraph variables come after the nv variables.
    ne = N * (len(Q) + len(R))
    tot = nv + ne
    pad = [0] * ne

    G, g, E, e = [], [], [], []
    # @line L4
    for c, b in Zrows:  # x - z0 in Z
        G.append([-ci for ci in c] + [0] * (N * m) + pad)
        g.append(b - sum(ci * xi for ci, xi in zip(c, x)))
    for k in range(N):
        for a, b in Xbar:
            G.append([sum(a[i] * zs_aff[k][i][col] for i in range(n)) for col in range(nv)] + pad)
            g.append(b)
        for a, b in Ubar:
            r = [0] * tot
            for j in range(m):
                r[n + k * m + j] = a[j]
            G.append(r)
            g.append(b)
    for i in range(n):  # z_N = 0
        E.append(zs_aff[N][i] + pad)
        e.append(0)
    col = nv
    for k in range(N):
        for W_, isQ in ((Q, True), (R, False)):
            for wr in W_:
                for sg in (1, -1):
                    r = [0] * tot
                    if isQ:
                        for i in range(n):
                            for cc in range(nv):
                                r[cc] += sg * wr[i] * zs_aff[k][i][cc]
                    else:
                        for j in range(m):
                            r[n + k * m + j] += sg * wr[j]
                    r[col] = -1
                    G.append(r)
                    g.append(0)
                col += 1
    cost = [0] * nv + [1] * ne
    # @line L5
    sol = lp_min(cost, G, g, E, e, range(nv, tot), tol)
    if sol is None:
        return None
    val, zz = sol
    z0 = zz[:n]
    vs = [zz[n + k * m:n + (k + 1) * m] for k in range(N)]
    zs = [[sum(r[cc] * zz[cc] for cc in range(nv)) for r in zs_aff[k]] for k in range(N + 1)]
    return val, z0, vs, zs


def closed_loop(A, B, K, Z, Zrows, x0, N, Q, R, Xbar, Ubar, disturbances, tol=1e-9):
    """Run the tube controller. Returns (xs, us, z0s, values)."""
    x = list(x0)
    xs, us, z0s, vals = [list(x)], [], [], []
    for w in disturbances:  # @line L3
        sol = tube_mpc(A, B, Z, Zrows, x, N, Q, R, Xbar, Ubar, tol)
        if sol is None:
            raise RuntimeError("the nominal problem is infeasible")
        val, z0, vs, _ = sol
        # @line L6
        u = [vj + sum(K[j][i] * (x[i] - z0[i]) for i in range(len(x))) for j, vj in enumerate(vs[0])]
        x = [a + b + wi for a, b, wi in zip(_matvec(A, x), _matvec(B, u), w)]
        xs.append(x)
        us.append(u)
        z0s.append(z0)
        vals.append(val)
    return xs, us, z0s, vals
