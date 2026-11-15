# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lmi-h-infinity-synthesis/. The authors are listed in prov/HWW5GT.jsonl.

"""LMI-based H-infinity synthesis (Gahinet and Apkarian 1994).

The plant is a dict with keys A, B1, B2, C1, C2, D11, D12, D21 (D22 = 0):

    x' = A x + B1 w + B2 u,  z = C1 x + D11 w + D12 u,  y = C2 x + D21 w.

The controller K = (A_K, B_K, C_K, D_K) is wired as u = K y, the lower
linear fractional transformation, as on the two-Riccati synthesis page.

The semidefinite programs are solved by a small log-barrier method with
Newton steps and a phase I. It is meant for plants with a few states;
a real code uses a primal-dual interior point solver.
"""

import math

from ctlmat import add, block, charpoly, eye, inv, mul, polyroots, scale, solve, sub, transpose, zeros

__all__ = [
    "null_space", "chol", "sdp_feasible", "sdp_minimize", "sdp_center",
    "gamma_lmis", "optimal_gamma", "reconstruct_x", "controller_lmi",
    "closed_loop", "is_hurwitz", "lmi_synthesis",
]


def _flo(a):
    return [[float(v) for v in row] for row in a]


# ---------------------------------------------------------------- algebra

def null_space(m, tol=1e-10):
    """Orthonormal basis of the kernel of m, as the columns of a matrix."""
    m = _flo(m)
    rows, cols = len(m), len(m[0])
    a = [list(r) for r in m]
    pivots = []
    r = 0
    big = max((abs(v) for row in a for v in row), default=0.0)
    for c in range(cols):
        if r == rows:
            break
        p = max(range(r, rows), key=lambda i: abs(a[i][c]))
        if abs(a[p][c]) <= tol * max(big, 1.0):
            continue
        a[r], a[p] = a[p], a[r]
        piv = a[r][c]
        a[r] = [v / piv for v in a[r]]
        for i in range(rows):
            if i != r and a[i][c] != 0.0:
                f = a[i][c]
                a[i] = [a[i][j] - f * a[r][j] for j in range(cols)]
        pivots.append(c)
        r += 1
    free = [c for c in range(cols) if c not in pivots]
    vecs = []
    for f in free:
        v = [0.0] * cols
        v[f] = 1.0
        for i, c in enumerate(pivots):
            v[c] = -a[i][f]
        vecs.append(v)
    basis = []
    for v in vecs:                       # Gram-Schmidt, twice for accuracy
        for _ in range(2):
            for q in basis:
                d = sum(x * y for x, y in zip(v, q))
                v = [x - d * y for x, y in zip(v, q)]
        n = math.sqrt(sum(x * x for x in v))
        basis.append([x / n for x in v])
    return [[basis[j][i] for j in range(len(basis))] for i in range(cols)]


def chol(a):
    """Lower Cholesky factor of a symmetric matrix, or None if not positive definite."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = a[j][j] - sum(low[j][k] ** 2 for k in range(j))
        if not d > 0.0:
            return None
        low[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            low[i][j] = (a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))) / low[j][j]
    return low


def is_hurwitz(m, tol=1e-9):
    return max(r.real for r in polyroots(charpoly(_flo(m)))) < -tol


def _sym(a):
    n = len(a)
    return [[0.5 * (a[i][j] + a[j][i]) for j in range(n)] for i in range(n)]


# ------------------------------------------------------- log-barrier SDP
#
# An LMI is a pair (G0, [G1, ..., Gk]) and means G0 + sum x_j G_j > 0.

def affine(fun, k):
    """Turn an affine map x -> symmetric matrix into the pair (G0, [G_j])."""
    g0 = _sym(_flo(fun([0.0] * k)))
    gs = []
    for j in range(k):
        e = [0.0] * k
        e[j] = 1.0
        gs.append(_sym(sub(_flo(fun(e)), g0)))
    return g0, gs


def _value(lmi, x):
    g0, gs = lmi
    n = len(g0)
    out = [list(row) for row in g0]
    for xj, gj in zip(x, gs):
        if xj != 0.0:
            for i in range(n):
                oi, gi = out[i], gj[i]
                for j in range(n):
                    oi[j] += xj * gi[j]
    return out


def _objective(c, t, lmis, x):
    f = t * sum(ci * xi for ci, xi in zip(c, x))
    for lmi in lmis:
        low = chol(_value(lmi, x))
        if low is None:
            return None
        f -= 2.0 * sum(math.log(low[i][i]) for i in range(len(low)))
    return f


def _center(c, t, lmis, x, stop=None, tol=1e-10, maxiter=80):
    """Newton's method with backtracking on t c^T x - sum log det G_i(x)."""
    k = len(x)
    for _ in range(maxiter):
        g = [t * ci for ci in c]
        h = [[0.0] * k for _ in range(k)]
        for lmi in lmis:
            gi = inv(_value(lmi, x))
            a = [mul(gi, gj) for gj in lmi[1]]
            size = len(gi)
            for p in range(k):
                ap = a[p]
                g[p] -= sum(ap[i][i] for i in range(size))
                for q in range(p, k):
                    aq = a[q]
                    s = sum(ap[i][j] * aq[j][i] for i in range(size) for j in range(size))
                    h[p][q] += s
                    if q != p:
                        h[q][p] += s
        dx = solve(h, [-v for v in g])
        slope = sum(a * b for a, b in zip(g, dx))
        if -slope / 2.0 <= tol:
            break
        f0 = _objective(c, t, lmis, x)
        step = 1.0
        while True:
            xn = [xi + step * di for xi, di in zip(x, dx)]
            fn = _objective(c, t, lmis, xn)
            if fn is not None and fn <= f0 + 0.25 * step * slope:
                break
            step *= 0.5
            if step < 1e-14:
                return x
        x = xn
        if stop is not None and stop(x):
            return x
    return x


def sdp_minimize(c, lmis, x, eps=1e-8, mu=8.0):
    """Minimize c^T x over the LMIs from a strictly feasible x (barrier method)."""
    total = sum(len(lmi[0]) for lmi in lmis)
    t = 1.0
    while True:
        x = _center(c, t, lmis, x)  # @line L10
        if total / t < eps:  # @line L11
            return x
        t *= mu


def sdp_center(lmis, x):
    """Analytic center of the LMIs, from a strictly feasible x."""
    return _center([0.0] * len(x), 1.0, lmis, x)


def sdp_feasible(lmis, x0, eps=1e-9):
    """Phase I: return a strictly feasible x, or None if min s > 0.

    Solves min s subject to G_i(x) + s I > 0, starting at x0 with s large.
    The LMIs must bound x, or min s may be unbounded; the callers add a
    bound constraint.
    """
    k = len(x0)
    aug = [(g0, gs + [eye(len(g0))]) for g0, gs in lmis]
    s = 1.0
    while _objective([0.0] * (k + 1), 0.0, aug, list(x0) + [s]) is None:
        s *= 2.0
    s *= 2.0                             # now G_i(x0) + s I >= (s / 2) I
    c = [0.0] * k + [1.0]
    done = (lambda z: z[-1] < 0.0)
    total = sum(len(lmi[0]) for lmi in aug)
    z = list(x0) + [s]
    t = 1.0
    while True:  # @line L9
        z = _center(c, t, aug, z, stop=done)
        if z[-1] < 0.0:
            return z[:-1]
        # On the central path, min s >= s(t) - total / t.
        if z[-1] - total / t > 0.0 or total / t < eps:
            return None
        t *= 8.0


# ------------------------------------------------------- the H-infinity LMIs

def _svec_size(n):
    return n * (n + 1) // 2


def _smat(v, n):
    m = [[0.0] * n for _ in range(n)]
    idx = 0
    for i in range(n):
        for j in range(i, n):
            m[i][j] = m[j][i] = v[idx]
            idx += 1
    return m


def _dims(p):
    n = len(p["A"])
    return n, len(p["B1"][0]), len(p["B2"][0]), len(p["C1"]), len(p["C2"])


def gamma_lmis(p, gamma=None, bound=1e3):
    """The three LMIs of Gahinet and Apkarian, plus a bound, as SDP data.

    The variable is x = (svec R, svec S) and, if gamma is None, also gamma.
    """
    a, b1, b2, c1, c2 = (_flo(p[k]) for k in ("A", "B1", "B2", "C1", "C2"))
    d11, d12, d21 = (_flo(p[k]) for k in ("D11", "D12", "D21"))
    n, m1, m2, p1, p2 = _dims(p)
    q = _svec_size(n)
    nr = null_space(block([[transpose(b2), transpose(d12)]]))  # @line L1
    ns = null_space(block([[c2, d21]]))
    k = 2 * q + (1 if gamma is None else 0)

    def split(x):
        g = x[2 * q] if gamma is None else gamma
        return _smat(x[:q], n), _smat(x[q:2 * q], n), g

    def lmi_r(x):
        r, _, g = split(x)
        mid = block([[add(mul(a, r), mul(r, transpose(a))), mul(r, transpose(c1)), b1],
                     [mul(c1, r), scale(-g, eye(p1)), d11],
                     [transpose(b1), transpose(d11), scale(-g, eye(m1))]])
        w = block([[nr, zeros(n + p1, m1)], [zeros(m1, len(nr[0])), eye(m1)]])
        return scale(-1.0, mul(mul(transpose(w), mid), w))

    def lmi_s(x):
        _, s, g = split(x)
        mid = block([[add(mul(transpose(a), s), mul(s, a)), mul(s, b1), transpose(c1)],
                     [mul(transpose(b1), s), scale(-g, eye(m1)), transpose(d11)],
                     [c1, d11, scale(-g, eye(p1))]])
        w = block([[ns, zeros(n + m1, p1)], [zeros(p1, len(ns[0])), eye(p1)]])
        return scale(-1.0, mul(mul(transpose(w), mid), w))

    def coupling(x):
        r, s, _ = split(x)
        return block([[r, eye(n)], [eye(n), s]])

    def box(x):
        r, s, g = split(x)
        tr = sum(r[i][i] + s[i][i] for i in range(n))
        return [[bound - tr - (g if gamma is None else 0.0)]]

    lmis = [affine(f, k) for f in (lmi_r, lmi_s, coupling, box)]
    x0 = [0.0] * k
    for i in range(n):                       # R = S = I as a start
        x0[_svec_index(i, i, n)] = 1.0
        x0[q + _svec_index(i, i, n)] = 1.0
    if gamma is None:
        x0[-1] = 1.0
    return lmis, x0, split


def _svec_index(i, j, n):
    i, j = min(i, j), max(i, j)
    return i * n - i * (i - 1) // 2 + (j - i)


def optimal_gamma(p, eps=1e-8):
    """Return (gamma_opt, R, S) from min gamma subject to the three LMIs."""
    lmis, x0, split = gamma_lmis(p)
    x = sdp_feasible(lmis, x0)
    if x is None:
        raise ValueError("no stabilizing controller within the bound")
    c = [0.0] * (len(x) - 1) + [1.0]
    x = sdp_minimize(c, lmis, x, eps)  # @line L2
    r, s, g = split(x)
    return g, r, s


def reconstruct_x(r, s):
    """X_cl > 0 with (X_cl)_11 = S and (X_cl^-1)_11 = R, taking M = I."""
    n = len(r)
    nn = sub(eye(n), mul(s, r))  # @line L5
    w = _sym(sub(mul(mul(r, s), r), r))
    return block([[s, nn], [transpose(nn), w]])  # @line L6


def _closed_loop_mats(p, omega):
    a, b1, b2, c1, c2 = (_flo(p[k]) for k in ("A", "B1", "B2", "C1", "C2"))
    d11, d12, d21 = (_flo(p[k]) for k in ("D11", "D12", "D21"))
    n, m1, m2, p1, p2 = _dims(p)
    ak = [row[:n] for row in omega[:n]]
    bk = [row[n:] for row in omega[:n]]
    ck = [row[:n] for row in omega[n:]]
    dk = [row[n:] for row in omega[n:]]
    acl = block([[add(a, mul(mul(b2, dk), c2)), mul(b2, ck)], [mul(bk, c2), ak]])
    bcl = block([[add(b1, mul(mul(b2, dk), d21))], [mul(bk, d21)]])
    ccl = block([[add(c1, mul(mul(d12, dk), c2)), mul(d12, ck)]])
    dcl = add(d11, mul(mul(d12, dk), d21))
    return acl, bcl, ccl, dcl


def closed_loop(p, k):
    """Closed loop (A, B, C, D) from w to z with u = K y."""
    ak, bk, ck, dk = (_flo(m) for m in k)
    omega = block([[ak, bk], [ck, dk]])
    return _closed_loop_mats(p, omega)


def controller_lmi(p, xcl, gamma, bound=1e3):
    """Find Omega = [[A_K, B_K], [C_K, D_K]] with the bounded real LMI < 0."""
    n, m1, m2, p1, p2 = _dims(p)
    rows, cols = n + m2, n + p2
    k = rows * cols

    def unpack(x):
        return [[x[i * cols + j] for j in range(cols)] for i in range(rows)]

    def brl(x):
        acl, bcl, ccl, dcl = _closed_loop_mats(p, unpack(x))
        top = add(mul(transpose(acl), xcl), mul(xcl, acl))
        mid = block([[top, mul(xcl, bcl), transpose(ccl)],
                     [mul(transpose(bcl), xcl), scale(-gamma, eye(m1)), transpose(dcl)],
                     [ccl, dcl, scale(-gamma, eye(p1))]])
        return scale(-1.0, mid)

    def frob(x):
        return block([[scale(bound, eye(k)), [[v] for v in x]], [[list(x)], [[bound]]]])

    lmis = [affine(brl, k), affine(frob, k)]
    x = sdp_feasible(lmis, [0.0] * k)  # @line L7
    if x is None:
        return None
    x = sdp_center(lmis, x)
    om = unpack(x)
    return ([row[:n] for row in om[:n]], [row[n:] for row in om[:n]],
            [row[:n] for row in om[n:]], [row[n:] for row in om[n:]])


def lmi_synthesis(p, backoff=1.05, gopt=None):
    """Return (gamma_opt, gamma, K, X_cl) with K built at gamma = backoff * gamma_opt.

    A known gamma_opt can be passed in to skip the first SDP.
    """
    if gopt is None:
        gopt, _, _ = optimal_gamma(p)
    gamma = backoff * gopt  # @line L3
    lmis, x0, split = gamma_lmis(p, gamma)
    x = sdp_feasible(lmis, x0)
    x = sdp_center(lmis, x)  # @line L4
    r, s, _ = split(x)
    xcl = reconstruct_x(r, s)
    k = controller_lmi(p, xcl, gamma)
    return gopt, gamma, k, xcl  # @line L8
