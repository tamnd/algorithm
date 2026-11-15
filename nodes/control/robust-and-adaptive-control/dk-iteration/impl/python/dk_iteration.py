# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dk-iteration/. The authors are listed in prov/QSHHP3.jsonl.

"""D-K iteration with constant D scales.

The generalized plant has the normalized form of the two-Riccati page:

    x' = A x + B1 w + B2 u
    z  = C1 x + D12 u          with D12^T [C1 D12] = [0 I]
    y  = C2 x + D21 w          with [B1; D21] D21^T = [0; I]

and D11 = 0, D22 = 0. A plant is a dict with the keys "A", "B1", "B2",
"C1", "C2", "D12", "D21". The controller is wired as u = K y.

The uncertainty structure has two full complex blocks: the first nz rows
of z feed the first nw entries of w through the uncertainty Delta, and
the rest of z and w form the performance block. The D scale is
diag(d I, I) on z and diag(d I, I) on w, with d > 0. The rows of z
reached by u and the entries of w that reach y must be in the
performance block, so that scaling keeps the normalized form.

The K-step is the two-Riccati synthesis of the scaled plant (bisection
on gamma and the central controller). It repeats the code of the
two-Riccati page so that this file stands alone. The D-step minimizes the
peak over a frequency grid of the largest singular value of
D M(jw) D^-1 over log d by golden section search.
"""

import math

from ctlmat import (
    add, block, charpoly, det, eye, inv, is_pos_def, mul, norm2, polyroots,
    scale, solve, sub, transpose, zeros,
)

__all__ = [
    "riccati", "is_hurwitz", "gamma_feasible", "optimal_gamma",
    "central_controller", "closed_loop", "scale_plant", "responses",
    "scaled_peak", "d_step", "k_step", "dk_iteration",
]


def _flo(a):
    return [[float(v) for v in row] for row in a]


def _big(a):
    return max((abs(v) for row in a for v in row), default=0.0)


# ------------------------------------------- K-step: two-Riccati synthesis

def _sign(h, tol=1e-13, maxiter=100):
    n = len(h)
    z = _flo(h)
    for _ in range(maxiter):
        d = abs(det(z))
        if not d > 0.0 or not math.isfinite(d):
            return None
        mu = d ** (-1.0 / n)
        zi = inv(z)
        znew = [[0.5 * (mu * z[i][j] + zi[i][j] / mu) for j in range(n)] for i in range(n)]
        diff = _big(sub(znew, z))
        z = znew
        if diff <= tol * max(1.0, _big(z)):
            break
    if _big(sub(mul(z, z), eye(n))) > 1e-8:
        return None
    return z


def is_hurwitz(m, tol=1e-9):
    """Return True if every eigenvalue of m has real part below -tol."""
    return max(r.real for r in polyroots(charpoly(_flo(m)))) < -tol


def _rho(m):
    return max(abs(r) for r in polyroots(charpoly(_flo(m))))


def riccati(a, r, q):
    """Stabilizing X of A^T X + X A + X R X + Q = 0 (A + R X Hurwitz), or None."""
    n = len(a)
    a, r, q = _flo(a), _flo(r), _flo(q)
    h = block([[a, r], [scale(-1.0, q), scale(-1.0, transpose(a))]])
    w = _sign(h)
    if w is None:
        return None
    wp = add(w, eye(2 * n))
    lhs = [row[n:] for row in wp]
    rhs = [[-v for v in row[:n]] for row in wp]
    lt = transpose(lhs)
    try:
        x = solve(mul(lt, lhs), mul(lt, rhs))
    except ValueError:
        return None
    x = [[0.5 * (x[i][j] + x[j][i]) for j in range(n)] for i in range(n)]
    res = add(add(mul(transpose(a), x), mul(x, a)), add(mul(mul(x, r), x), q))
    size = 1.0 + _big(mul(transpose(a), x)) + _big(mul(mul(x, r), x)) + _big(q)
    if not math.isfinite(_big(x)) or _big(res) > 1e-7 * size:
        return None
    if not is_hurwitz(add(a, mul(r, x))):
        return None
    return x


def gamma_feasible(p, gamma):
    """The three conditions of Doyle, Glover, Khargonekar and Francis. Return (ok, X, Y)."""
    a, b1, b2, c1, c2 = (_flo(p[k]) for k in ("A", "B1", "B2", "C1", "C2"))
    g2 = 1.0 / (gamma * gamma)
    x = riccati(a, sub(scale(g2, mul(b1, transpose(b1))), mul(b2, transpose(b2))),
                mul(transpose(c1), c1))
    if x is None or not is_pos_def(x, -1e-9 * (1.0 + _big(x))):
        return False, x, None
    y = riccati(transpose(a), sub(scale(g2, mul(transpose(c1), c1)), mul(transpose(c2), c2)),
                mul(b1, transpose(b1)))
    if y is None or not is_pos_def(y, -1e-9 * (1.0 + _big(y))):
        return False, x, y
    return _rho(mul(x, y)) < gamma * gamma * (1.0 - 1e-9), x, y


def optimal_gamma(p, rtol=1e-5):
    """Bisection for the smallest gamma that passes gamma_feasible."""
    lo, hi = 0.0, 1.0
    while not gamma_feasible(p, hi)[0]:
        lo, hi = hi, 2.0 * hi
        if hi > 1e8:
            raise ValueError("no gamma below 1e8 passes the test")
    while hi - lo > rtol * hi:
        g = 0.5 * (lo + hi)
        if gamma_feasible(p, g)[0]:
            hi = g
        else:
            lo = g
    return hi


def central_controller(p, gamma):
    """(A_K, B_K, C_K, D_K) of the central controller at gamma."""
    ok, x, y = gamma_feasible(p, gamma)
    if not ok:
        raise ValueError("gamma does not pass the three conditions")
    a, b1, b2, c2 = (_flo(p[k]) for k in ("A", "B1", "B2", "C2"))
    n = len(a)
    g2 = 1.0 / (gamma * gamma)
    f = scale(-1.0, mul(transpose(b2), x))
    l = scale(-1.0, mul(y, transpose(c2)))
    z = inv(sub(eye(n), scale(g2, mul(y, x))))
    ak = add(add(a, scale(g2, mul(mul(b1, transpose(b1)), x))), add(mul(b2, f), mul(mul(z, l), c2)))
    return ak, scale(-1.0, mul(z, l)), f, zeros(len(f), len(c2))


def closed_loop(p, k):
    """(A, B, C, D) of the map w -> z with u = K y."""
    a, b1, b2, c1, c2, d12, d21 = (_flo(p[s]) for s in ("A", "B1", "B2", "C1", "C2", "D12", "D21"))
    ak, bk, ck, dk = (_flo(m) for m in k)
    acl = block([[add(a, mul(mul(b2, dk), c2)), mul(b2, ck)], [mul(bk, c2), ak]])
    bcl = block([[add(b1, mul(mul(b2, dk), d21))], [mul(bk, d21)]])
    ccl = block([[add(c1, mul(mul(d12, dk), c2)), mul(d12, ck)]])
    return acl, bcl, ccl, mul(mul(d12, dk), d21)


# ------------------------------------------------------------ the D scales

def scale_plant(p, d, nz, nw):
    """Plant with z1 -> d z1 (first nz rows of z) and w1 -> w1 / d (first nw entries of w)."""
    q = {k: _flo(v) for k, v in p.items()}
    q["C1"] = [[(d if i < nz else 1.0) * v for v in row] for i, row in enumerate(q["C1"])]
    q["D12"] = [[(d if i < nz else 1.0) * v for v in row] for i, row in enumerate(q["D12"])]
    q["B1"] = [[v / d if j < nw else v for j, v in enumerate(row)] for row in q["B1"]]
    q["D21"] = [[v / d if j < nw else v for j, v in enumerate(row)] for row in q["D21"]]
    return q


def responses(sys, freqs):
    """The complex matrices M(j w) = C (j w I - A)^-1 B + D for w in freqs."""
    a, b, c, d = sys
    n = len(a)
    bc = [[complex(v) for v in row] for row in b]
    out = []
    for w in freqs:
        m = [[(1j * w if i == j else 0.0) - a[i][j] for j in range(n)] for i in range(n)]
        out.append(add(mul(c, solve(m, bc)), d))
    return out


def scaled_peak(ms, d, nz, nw):
    """max over the grid of the largest singular value of D M D^-1."""
    best = 0.0
    for m in ms:
        sm = [[v * (d if i < nz else 1.0) / (d if j < nw else 1.0) for j, v in enumerate(row)]
              for i, row in enumerate(m)]
        best = max(best, norm2(sm))
    return best


def d_step(ms, nz, nw, lo=-8.0, hi=8.0, tol=1e-6):
    """Golden section search on log d. Return (d, peak)."""
    f = (lambda t: scaled_peak(ms, math.exp(t), nz, nw))
    r = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = lo, hi
    x1, x2 = b - r * (b - a), a + r * (b - a)
    f1, f2 = f(x1), f(x2)
    while b - a > tol:  # @line L6
        if f1 <= f2:
            b, x2, f2 = x2, x1, f1
            x1 = b - r * (b - a)
            f1 = f(x1)
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + r * (b - a)
            f2 = f(x2)
    t = x1 if f1 <= f2 else x2
    return math.exp(t), min(f1, f2)  # @line L7


def k_step(p, d, nz, nw, backoff=1.02):
    """Two-Riccati synthesis on the scaled plant. Return (gamma_opt, gamma, K)."""
    ps = scale_plant(p, d, nz, nw)  # @line L3
    gopt = optimal_gamma(ps)
    g = backoff * gopt
    return gopt, g, central_controller(ps, g)  # @line L4


def dk_iteration(p, nz, nw, freqs, iters=6, backoff=1.02, rtol=1e-3):
    """Return (K, d, history). history[i] = (gamma_opt of K-step, peak after D-step, d)."""
    d = 1.0  # @line L1
    history = []
    best = None
    for _ in range(iters):  # @line L2
        gopt, g, k = k_step(p, d, nz, nw, backoff)
        ms = responses(closed_loop(p, k), freqs)  # @line L5
        d, peak = d_step(ms, nz, nw)
        history.append((gopt, peak, d))
        if best is None or peak < best[0]:
            best = (peak, k, d)
        if len(history) > 1 and history[-2][1] - peak <= rtol * peak:  # @line L8
            break
    return best[1], best[2], history  # @line L9
