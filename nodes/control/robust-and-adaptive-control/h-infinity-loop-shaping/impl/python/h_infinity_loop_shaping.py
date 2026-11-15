# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/h-infinity-loop-shaping/. The authors are listed in prov/5JS87D.jsonl.

"""H-infinity loop shaping (McFarlane and Glover 1992).

A system is a tuple (A, B, C, D) of lists of rows. The shaped plant
Gs = W2 G W1 must have D = 0 here, as in the simplest form of the
formulas. The robust stabilization step follows Glover and McFarlane
(1989) in the form of Skogestad and Postlethwaite (2005, section 9.4):

    GCARE  A Z + Z A^T - Z C^T C Z + B B^T = 0
    GFARE  A^T X + X A - X B B^T X + C^T C = 0
    gamma_min = sqrt(1 + rho(X Z)),  eps_max = 1 / gamma_min

The central controller of that book is for positive feedback, u = Ks y.
The function controller() returns it in the negative feedback form of
this site, u = -C y (so C = -Ks), with the loop L = G C.
"""

import math

from ctlmat import (
    add, block, charpoly, det, eye, inv, mul, norm2, polyroots, scale, solve,
    sub, transpose, zeros,
)

__all__ = [
    "riccati", "is_hurwitz", "gamma_min", "controller", "series",
    "feedback_a", "margin_at", "stability_margin", "loop_shaping_design",
]


def _flo(a):
    return [[float(v) for v in row] for row in a]


def _big(a):
    return max((abs(v) for row in a for v in row), default=0.0)


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


def riccati(a, r, q):
    """Stabilizing X of A^T X + X A + X R X + Q = 0 (A + R X Hurwitz), or None.

    The stable invariant subspace of [[A, R], [-Q, -A^T]] is the kernel of
    sign(H) + I, and it is the range of [I; X].
    """
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
    if _big(res) > 1e-8 * size or not is_hurwitz(add(a, mul(r, x))):
        return None
    return x


def _rho(m):
    return max(abs(v) for v in polyroots(charpoly(_flo(m))))


def gamma_min(gs):
    """Return (gamma_min, X, Z) for the shaped plant gs = (A, B, C, 0)."""
    a, b, c, d = (_flo(m) for m in gs)
    if _big(d) != 0.0:
        raise ValueError("this implementation needs D = 0")
    z = riccati(transpose(a), scale(-1.0, mul(transpose(c), c)), mul(b, transpose(b)))  # @line L2
    x = riccati(a, scale(-1.0, mul(b, transpose(b))), mul(transpose(c), c))  # @line L3
    if x is None or z is None:
        raise ValueError("the shaped plant must be stabilizable and detectable")
    return math.sqrt(1.0 + _rho(mul(x, z))), x, z  # @line L4


def controller(gs, gamma):
    """Return the central controller (A_K, B_K, C_K, D_K) for u = -C y.

    gamma must be larger than gamma_min. Then the loop of gs and C is
    internally stable and ||[C; I] (I + gs C)^-1 [I, gs]||_inf <= gamma.
    """
    gmin, x, z = gamma_min(gs)
    if not gamma > gmin:
        raise ValueError("gamma must exceed gamma_min")
    a, b, c, _ = (_flo(m) for m in gs)
    n = len(a)
    g2 = gamma * gamma
    l = add(scale(1.0 - g2, eye(n)), mul(x, z))  # @line L6
    lti = inv(transpose(l))
    bk = scale(g2, mul(mul(lti, z), transpose(c)))  # @line L7
    ak = add(sub(a, mul(mul(b, transpose(b)), x)), mul(bk, c))
    ck = mul(transpose(b), x)
    # Positive feedback Ks = (ak, bk, ck, 0); negative feedback C = -Ks.
    return ak, bk, scale(-1.0, ck), zeros(len(ck), len(c))  # @line L8


def series(s1, s2):
    """Return s2 s1: the input goes through s1 first, then through s2."""
    a1, b1, c1, d1 = (_flo(m) for m in s1)
    a2, b2, c2, d2 = (_flo(m) for m in s2)
    if not a1:
        a = a2
        b = mul(b2, d1)
        c = c2
        return a, b, c, mul(d2, d1)
    if not a2:
        return a1, b1, mul(d2, c1), mul(d2, d1)
    a = block([[a1, zeros(len(a1), len(a2))], [mul(b2, c1), a2]])
    b = block([[b1], [mul(b2, d1)]])
    c = block([[mul(d2, c1), c2]])
    return a, b, c, mul(d2, d1)


def feedback_a(g, k):
    """State matrix of the negative feedback loop u = -K y around G (D_G = 0)."""
    ag, bg, cg, dg = (_flo(m) for m in g)
    ak, bk, ck, dk = (_flo(m) for m in k)
    if _big(dg) != 0.0:
        raise ValueError("the plant must be strictly proper")
    return block([[sub(ag, mul(mul(bg, dk), cg)), scale(-1.0, mul(bg, ck))],
                  [mul(bk, cg), ak]]) if ak else sub(ag, mul(mul(bg, dk), cg))


def _resp(sys, s):
    a, b, c, d = sys
    n = len(a)
    if n == 0:
        return [[complex(v) for v in row] for row in d]
    m = [[(s if i == j else 0.0) - a[i][j] for j in range(n)] for i in range(n)]
    return add(mul(c, solve(m, [[complex(v) for v in row] for row in b])), d)


def margin_at(g, k, w):
    """Largest singular value of [K; I] (I + G K)^-1 [I, G] at s = j w."""
    gs = _resp(tuple(_flo(m) for m in g), 1j * w)
    ks = _resp(tuple(_flo(m) for m in k), 1j * w)
    p = len(gs)
    sinv = inv(add(eye(p), mul(gs, ks)))
    left = block([[ks], [eye(p)]])
    right = block([[eye(p), gs]])
    return norm2(mul(mul(left, sinv), right))


def stability_margin(g, k, freqs):
    """b(G, K) = 1 / max over freqs of margin_at; the loop must be stable."""
    return 1.0 / max(margin_at(g, k, w) for w in freqs)


def loop_shaping_design(g, w1, w2, factor=1.1):
    """McFarlane-Glover design. Return (gamma_min, gamma, K) with K = W1 Ks W2."""
    gs = series(series(w1, g), w2)  # @line L1
    gmin = gamma_min(gs)[0]
    gamma = factor * gmin  # @line L5
    ks = controller(gs, gamma)
    k = series(series(w2, ks), w1)  # @line L9
    return gmin, gamma, k
