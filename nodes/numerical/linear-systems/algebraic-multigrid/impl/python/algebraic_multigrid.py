# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-multigrid/. The authors are listed in prov/EZNBXD.jsonl.
"""Classical (Ruge-Stueben) algebraic multigrid: strength of connection,
C/F splitting, direct interpolation, Galerkin coarse operators and a
V-cycle with symmetric Gauss-Seidel smoothing. A matrix is a list of rows,
each a dict {column: value}. Works with float or Fraction entries."""
import heapq
import math


class Singular(ArithmeticError):
    pass


def matvec(a, x):
    return [sum(v * x[j] for j, v in row.items()) for row in a]


def nnz(a):
    return sum(len(r) for r in a)


def strength(a, theta):
    """S[i] = the j != i on which i strongly depends:
    -a_ij >= theta * max_k(-a_ik), the max over k != i."""
    s = []
    for i, row in enumerate(a):
        m = max((-v for j, v in row.items() if j != i), default=0)
        if m <= 0:
            s.append(set())
        else:
            s.append({j for j, v in row.items() if j != i and -v >= theta * m})
    return s


def split(s):
    """Ruge-Stueben C/F splitting. Returns a list of booleans, True = C."""
    n = len(s)
    st = [[] for _ in range(n)]              # st[i] = points that depend on i
    for i in range(n):
        for j in s[i]:
            st[j].append(i)
    lam = [len(st[i]) for i in range(n)]
    state = [0] * n                          # 0 undecided, 1 C, 2 F
    for i in range(n):
        if not s[i] and not st[i]:
            state[i] = 2                     # isolated: smoother handles it
    heap = [(-lam[i], i) for i in range(n) if state[i] == 0]
    heapq.heapify(heap)
    while heap:
        neg, i = heapq.heappop(heap)
        if state[i] != 0 or -neg != lam[i]:
            continue
        state[i] = 1                         # new C point
        for j in st[i]:
            if state[j] == 0:
                state[j] = 2                 # depends on a C point: F
                for k in s[j]:
                    if state[k] == 0:
                        lam[k] += 1
                        heapq.heappush(heap, (-lam[k], k))
        for j in s[i]:
            if state[j] == 0:
                lam[j] -= 1
                heapq.heappush(heap, (-lam[j], j))
    for i in range(n):                       # second pass: F-F strong pairs
        if state[i] != 2:                    # need a common C point
            continue
        ci = {j for j in s[i] if state[j] == 1}
        for j in s[i]:
            if state[j] == 2 and not (s[j] & ci) and j not in ci:
                state[j] = 1
                ci.add(j)
    return [x == 1 for x in state]


def interpolation(a, s, c):
    """Direct interpolation. Returns (P as rows {coarse index: weight}, nc)."""
    n = len(a)
    idx, nc = [-1] * n, 0
    for i in range(n):
        if c[i]:
            idx[i], nc = nc, nc + 1
    p = []
    for i in range(n):
        if c[i]:
            p.append({idx[i]: 1})
            continue
        row = a[i]
        diag = row[i] + sum(v for j, v in row.items() if j != i and v > 0)
        ci = [j for j in s[i] if c[j] and row[j] < 0]
        neg = sum(v for j, v in row.items() if j != i and v < 0)
        den = sum(row[j] for j in ci)
        if not ci or diag == 0:
            p.append({})
            continue
        alpha = neg / den
        p.append({idx[j]: -alpha * row[j] / diag for j in ci})
    return p, nc


def galerkin(a, p, nc):
    """P^T A P."""
    ap = []
    for row in a:
        acc = {}
        for j, v in row.items():
            for q, w in p[j].items():
                acc[q] = acc.get(q, 0) + v * w
        ap.append(acc)
    out = [dict() for _ in range(nc)]
    for i, prow in enumerate(p):
        for q, w in prow.items():
            o = out[q]
            for r, v in ap[i].items():
                o[r] = o.get(r, 0) + w * v
    return out


def setup(a, theta=0.25, max_coarse=20, max_levels=25, stats=None):
    """Build the hierarchy: a list of (A_l, P_l); the last has P = None."""
    levels = []
    while True:                                        # @line L10
        n = len(a)
        if n <= max_coarse or len(levels) + 1 >= max_levels:
            break
        s = strength(a, theta)                         # @line L11
        c = split(s)                                   # @line L12
        p, nc = interpolation(a, s, c)                 # @line L13
        if nc == 0 or nc >= n:
            break
        levels.append((a, p))
        a = galerkin(a, p, nc)                         # @line L14
    levels.append((a, None))                           # @line L15
    if stats is not None:
        z0, n0 = nnz(levels[0][0]), len(levels[0][0])
        stats["levels"] = len(levels)
        stats["sizes"] = [len(l[0]) for l in levels]
        stats["operator_complexity"] = sum(nnz(l[0]) for l in levels) / z0
        stats["grid_complexity"] = sum(len(l[0]) for l in levels) / n0
    return levels


def lu_solve_dense(a, b):
    """Gaussian elimination with partial pivoting; raises Singular."""
    n = len(a)
    m = [[a[i].get(j, 0) for j in range(n)] + [b[i]] for i in range(n)]
    big = max((abs(v) for r in m for v in r[:n]), default=0)
    for k in range(n):
        piv = max(range(k, n), key=lambda i: abs(m[i][k]))
        if m[piv][k] == 0 or abs(m[piv][k]) <= 1e-14 * big * n:
            raise Singular("singular coarsest matrix")
        m[k], m[piv] = m[piv], m[k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            if f:
                for j in range(k, n + 1):
                    m[i][j] -= f * m[k][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def gauss_seidel(a, b, x, backward=False):
    n = len(a)
    for i in (range(n - 1, -1, -1) if backward else range(n)):
        row = a[i]
        s = b[i]
        for j, v in row.items():
            if j != i:
                s -= v * x[j]
        x[i] = s / row[i]


def vcycle(levels, b, x=None, l=0, nu1=1, nu2=1):
    """One V-cycle for A_l x = b; returns the new x."""
    a, p = levels[l]
    if p is None:                                      # @line L1
        return lu_solve_dense(a, b)                    # @line L2
    x = [0 * v for v in b] if x is None else list(x)
    for _ in range(nu1):
        gauss_seidel(a, b, x)                          # @line L3
    r = [bi - ai for bi, ai in zip(b, matvec(a, x))]   # @line L4
    nc = len(levels[l + 1][0])
    rc = [0 * v for v in b[:1]] * nc
    for i, prow in enumerate(p):                       # @line L5
        for q, w in prow.items():
            rc[q] += w * r[i]
    ec = vcycle(levels, rc, None, l + 1, nu1, nu2)     # @line L6
    for i, prow in enumerate(p):                       # @line L7
        for q, w in prow.items():
            x[i] += w * ec[q]
    for _ in range(nu2):
        gauss_seidel(a, b, x, backward=True)           # @line L8
    return x                                           # @line L9


def norm2(v):
    return math.sqrt(sum(float(t) * float(t) for t in v))


def solve(a, b, tol=1e-8, maxit=100, levels=None, **kw):
    """Stand-alone AMG iteration. Returns (x, info) where info has
    'converged', 'iterations' and 'history' (residual 2-norms)."""
    if levels is None:
        levels = setup(a, **kw)
    x = [0.0] * len(b)
    nb = norm2(b) or 1.0
    hist = [norm2(b)]
    for it in range(1, maxit + 1):
        x = vcycle(levels, b, x)
        r = norm2([bi - ai for bi, ai in zip(b, matvec(a, x))])
        hist.append(r)
        if not math.isfinite(r) or r > 1e8 * nb:
            return x, {"converged": False, "iterations": it, "history": hist}
        if r <= tol * nb:
            return x, {"converged": True, "iterations": it, "history": hist}
    return x, {"converged": False, "iterations": maxit, "history": hist}


def pcg(a, b, tol=1e-8, maxit=200, levels=None, **kw):
    """Conjugate gradients preconditioned by one V-cycle from zero."""
    if levels is None:
        levels = setup(a, **kw)
    n = len(b)
    x = [0.0] * n
    r = list(b)
    zv = vcycle(levels, r)
    d = list(zv)
    rz = sum(ri * zi for ri, zi in zip(r, zv))
    nb = norm2(b) or 1.0
    for it in range(1, maxit + 1):
        ad = matvec(a, d)
        alpha = rz / sum(di * adi for di, adi in zip(d, ad))
        x = [xi + alpha * di for xi, di in zip(x, d)]
        r = [ri - alpha * adi for ri, adi in zip(r, ad)]
        if norm2(r) <= tol * nb:
            return x, {"converged": True, "iterations": it}
        zv = vcycle(levels, r)
        rz2 = sum(ri * zi for ri, zi in zip(r, zv))
        d = [zi + (rz2 / rz) * di for zi, di in zip(zv, d)]
        rz = rz2
    return x, {"converged": False, "iterations": maxit}


def poisson2d(k, eps=1.0):
    """5-point matrix of -eps u_xx - u_yy on a k by k grid, Dirichlet."""
    a = []
    for r in range(k):
        for c in range(k):
            row = {r * k + c: 2 * eps + 2.0}
            if c > 0:
                row[r * k + c - 1] = -eps
            if c + 1 < k:
                row[r * k + c + 1] = -eps
            if r > 0:
                row[(r - 1) * k + c] = -1.0
            if r + 1 < k:
                row[(r + 1) * k + c] = -1.0
            a.append(row)
    return a
