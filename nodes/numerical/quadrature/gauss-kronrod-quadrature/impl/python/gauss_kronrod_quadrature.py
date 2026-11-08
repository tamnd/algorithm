# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-kronrod-quadrature/. The authors are listed in prov/Q6XB94.jsonl.

"""Gauss-Kronrod quadrature: an n-point Gauss-Legendre rule extended by n + 1 nodes.

The Kronrod nodes are the zeros of the Stieltjes polynomial E_{n+1}, defined by
the orthogonality integral E_{n+1}(x) P_n(x) x^k dx = 0 for k = 0..n. Written in the
Legendre basis, E_{n+1} = sum c_j P_j, these conditions are triangular in the c_j,
and the coefficients are computed exactly with Fractions from Adams' formula for
the integral of a product of three Legendre polynomials. The 2n + 1 point rule is
interpolatory with degree 3n + 1 (3n + 2 for odd n); the difference between the
Gauss and the Kronrod value drives the QUADPACK error estimate, which is a
heuristic. The adaptive driver bisects the panel with the largest estimate.
"""

import heapq
import math
from fractions import Fraction
from functools import lru_cache
from typing import Callable, List, Sequence, Tuple

EPS = 2.0 ** -52
UFLOW = 2.2250738585072014e-308


def _a(m: int) -> Fraction:
    """A(m) = (2m)! / (2^m m!)^2 = binom(2m, m) / 4^m."""
    return Fraction(math.comb(2 * m, m), 4 ** m)


def legendre_triple(l: int, m: int, n: int) -> Fraction:
    """Integral of P_l P_m P_n over [-1, 1] (Adams 1878). Exact."""
    if (l + m + n) % 2 or l > m + n or m > l + n or n > l + m:
        return Fraction(0)
    s = (l + m + n) // 2
    return Fraction(2, l + m + n + 1) * _a(s - l) * _a(s - m) * _a(s - n) / _a(s)


@lru_cache(maxsize=None)
def stieltjes_coefficients(n: int) -> Tuple[Fraction, ...]:
    """c_0..c_{n+1} with c_{n+1} = 1 such that E_{n+1} = sum c_j P_j is orthogonal to P_n P_k, k <= n."""
    c = [Fraction(0)] * (n + 2)
    c[n + 1] = Fraction(1)
    for k in range(n + 1):  # condition k fixes c_{n-k}; the integral of P_k P_n P_j vanishes for j < n - k
        j0 = n - k
        s = sum((c[j] * legendre_triple(k, n, j) for j in range(j0 + 1, n + 2)), Fraction(0))
        c[j0] = -s / legendre_triple(k, n, j0)
    return tuple(c)


def legendre_series(c: Sequence[float], x: float) -> float:
    """sum c_j P_j(x) by the forward three-term recurrence (stable on [-1, 1])."""
    p_prev, p = 1.0, x
    total = c[0] + (c[1] * x if len(c) > 1 else 0.0)
    for k in range(1, len(c) - 1):
        p_prev, p = p, ((2 * k + 1) * x * p - k * p_prev) / (k + 1)
        total += c[k + 1] * p
    return total


def _legendre_pair(n: int, x: float) -> Tuple[float, float]:
    p_prev, p = 1.0, x
    if n == 0:
        return 1.0, 0.0
    for k in range(1, n):
        p_prev, p = p, ((2 * k + 1) * x * p - k * p_prev) / (k + 1)
    return p, p_prev


def _bisect_root(g: Callable[[float], float], lo: float, hi: float) -> float:
    glo = g(lo)
    if glo == 0.0:
        return lo
    if (glo < 0.0) == (g(hi) < 0.0):
        raise ArithmeticError("no sign change: the interlacing property failed")
    while True:
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            return mid
        gm = g(mid)
        if gm == 0.0:
            return mid
        if (gm < 0.0) == (glo < 0.0):
            lo, glo = mid, gm
        else:
            hi = mid


def gauss_legendre(n: int) -> Tuple[List[float], List[float]]:
    """Gauss-Legendre nodes (increasing) and weights by bisection in Bruns' brackets."""
    xs = []
    for i in range(1, n + 1):
        lo = math.cos(i * math.pi / (n + 0.5))
        hi = math.cos((i - 0.5) * math.pi / (n + 0.5))
        xs.append(_bisect_root(lambda t: _legendre_pair(n, t)[0], lo, hi))
    xs.sort()
    xs = [0.5 * (xs[i] - xs[n - 1 - i]) for i in range(n)]  # exact symmetry
    ws = []
    for x in xs:
        p, q = _legendre_pair(n, x)
        dp = n * (q - x * p) / ((1.0 - x) * (1.0 + x))
        ws.append(2.0 / ((1.0 - x) * (1.0 + x) * dp * dp))
    return xs, ws


def _solve(a: List[List[float]], b: List[float]) -> List[float]:
    """Gaussian elimination with partial pivoting. O(m^3)."""
    m = len(b)
    a = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(m):
        piv = max(range(col, m), key=lambda r: abs(a[r][col]))
        a[col], a[piv] = a[piv], a[col]
        for r in range(col + 1, m):
            f = a[r][col] / a[col][col]
            if f != 0.0:
                for cc in range(col, m + 1):
                    a[r][cc] -= f * a[col][cc]
    x = [0.0] * m
    for r in range(m - 1, -1, -1):
        x[r] = (a[r][m] - math.fsum(a[r][cc] * x[cc] for cc in range(r + 1, m))) / a[r][r]
    return x


@lru_cache(maxsize=None)
def kronrod_rule(n: int) -> Tuple[Tuple[float, ...], Tuple[float, ...], Tuple[float, ...]]:
    """(nodes, Kronrod weights, Gauss weights) on [-1, 1] for the (2n+1)-point extension of G_n.

    Nodes are increasing; Gauss weights are 0 at the Kronrod-only nodes. Precondition: n >= 1.
    Cost: exact Fraction work polynomial in n for E_{n+1}, O(n^2) for its zeros, O(n^3) for the weights.
    """
    if n < 1:
        raise ValueError("need n >= 1")
    gx, gw = gauss_legendre(n)
    c = [float(t) for t in stieltjes_coefficients(n)]
    def e(t):
        return legendre_series(c, t)
    edges = [-1.0] + gx + [1.0]
    kx = [_bisect_root(e, edges[i], edges[i + 1]) for i in range(n + 1)]
    kx = [0.5 * (kx[i] - kx[n - i]) for i in range(n + 1)]
    nodes = sorted(gx + kx)
    gmap = dict(zip(gx, gw))
    # interpolatory weights: sum_i W_i P_k(y_i) = integral of P_k = 2 [k = 0], k = 0..2n
    rows = []
    for k in range(2 * n + 1):
        rows.append([_legendre_pair(k, y)[0] if k > 0 else 1.0 for y in nodes])
    rhs = [2.0] + [0.0] * (2 * n)
    wk = _solve(rows, rhs)
    m = len(nodes)
    wk = [0.5 * (wk[i] + wk[m - 1 - i]) for i in range(m)]
    return tuple(nodes), tuple(wk), tuple(gmap.get(y, 0.0) for y in nodes)


def gk_panel(f: Callable[[float], float], a: float, b: float, n: int = 7) -> Tuple[float, float, float, bool]:
    """(Kronrod value, QUADPACK error estimate, Gauss value, estimate is at the rounding floor) on [a, b].

    2n + 1 evaluations of f, none at the endpoints.
    """
    # @line L1
    # @line L2
    y, wk, wg = kronrod_rule(n)
    # @line L3
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    fv = [f(c + h * t) for t in y]
    # @line L4
    resk = math.fsum(w * v for w, v in zip(wk, fv))
    resg = math.fsum(w * v for w, v in zip(wg, fv))
    # @line L5
    mean = 0.5 * resk
    resabs = abs(h) * math.fsum(w * abs(v) for w, v in zip(wk, fv))
    resasc = abs(h) * math.fsum(w * abs(v - mean) for w, v in zip(wk, fv))
    err = abs((resk - resg) * h)
    if resasc != 0.0 and err != 0.0:
        err = resasc * min(1.0, (200.0 * err / resasc) ** 1.5)
    floor = 50.0 * EPS * resabs if resabs > UFLOW / (50.0 * EPS) else 0.0
    err = max(floor, err)
    # @line L6
    return resk * h, err, resg * h, err == floor


def integrate(f: Callable[[float], float], a: float, b: float, tol: float = 1e-10, rel: float = 0.0,
              n: int = 7, limit: int = 500) -> Tuple[float, float, int, str]:
    """Globally adaptive Gauss-Kronrod quadrature (QUADPACK QAG style).

    Stops when the summed error estimate is at most max(tol, rel |value|).
    Returns (value, error estimate, evaluations, status); status is "ok", "limit"
    (the panel budget ran out) or "roundoff" (the worst panel is too small to split, or its
    estimate is already the rounding floor 50 eps sum |w f|, so splitting cannot help).
    """
    if a == b:
        return 0.0, 0.0, 0, "ok"
    per = 2 * n + 1
    # @line L7
    q, e, _, fl = gk_panel(f, a, b, n)
    heap = [(-e, 0, a, b, q, fl)]
    total, errsum, evals, counter = q, e, per, 1
    status = "ok"
    # @line L8
    while errsum > max(tol, rel * abs(total)):
        if len(heap) >= limit:
            status = "limit"
            break
        # @line L9
        neg_e, _, l, r, ql, at_floor = heapq.heappop(heap)
        m = 0.5 * (l + r)
        if at_floor or not (min(l, r) < m < max(l, r)) or abs(r - l) <= 1000.0 * EPS * max(abs(l), abs(r)):
            heapq.heappush(heap, (neg_e, counter, l, r, ql, at_floor))
            status = "roundoff"
            break
        q1, e1, _, f1 = gk_panel(f, l, m, n)
        q2, e2, _, f2 = gk_panel(f, m, r, n)
        evals += 2 * per
        # @line L10
        heapq.heappush(heap, (-e1, counter, l, m, q1, f1))
        heapq.heappush(heap, (-e2, counter + 1, m, r, q2, f2))
        counter += 2
        total += q1 + q2 - ql
        errsum += e1 + e2 + neg_e
    # @line L11
    total = math.fsum(p[4] for p in heap)
    errsum = math.fsum(-p[0] for p in heap)
    return total, errsum, evals, status
