# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-quadrature/. The authors are listed in prov/AB3WK9.jsonl.

"""Globally adaptive quadrature with a Simpson pair on each panel.

Each panel [l, r] keeps five function values. S1 is Simpson's rule on the
whole panel and S2 is Simpson's rule on its two halves. The panel returns
Q = S2 + (S2 - S1)/15 and the error estimate e = |S2 - S1|/15. A priority
queue holds the panels by e. The panel with the largest e is split until the
sum of the estimates is at most the tolerance tau, or the evaluation budget is
used up, or the panel can no longer be split in floating point.

The estimate is a heuristic: it is asymptotically right for smooth f, but a
function that is small at all sample points can fool it.
"""

import heapq
import math
from typing import Callable, List, NamedTuple, Tuple

Panel = Tuple[float, int, float, float, Tuple[float, float, float, float, float], float]


class Result(NamedTuple):
    value: float
    error_estimate: float
    evaluations: int
    converged: bool


def _simpson_pair(l: float, r: float, fv: Tuple[float, float, float, float, float]) -> Tuple[float, float]:
    """Return (Q, e) for a panel with values at l, l + h/4, l + h/2, l + 3h/4, r."""
    h = r - l
    s1 = h / 6.0 * (fv[0] + 4.0 * fv[2] + fv[4])
    s2 = h / 12.0 * (fv[0] + 4.0 * fv[1] + 2.0 * fv[2] + 4.0 * fv[3] + fv[4])
    return s2 + (s2 - s1) / 15.0, abs(s2 - s1) / 15.0


def adaptive_quadrature(f: Callable[[float], float], a: float, b: float,
                        tau: float = 1e-10, max_evals: int = 100000) -> Result:
    """Integrate f over [a, b] to an estimated absolute error tau.

    Precondition: a and b are finite, f is defined on [a, b] (endpoints
    included) and returns finite floats, tau >= 0, max_evals >= 5.
    Cost: 5 + 4k evaluations of f and O(k log k) other work after k splits.
    Returns (value, error_estimate, evaluations, converged).
    """
    if not (math.isfinite(a) and math.isfinite(b)):
        raise ValueError("the interval must be finite; transform an infinite interval first")
    if a == b:  # @line L1
        return Result(0.0, 0.0, 0, True)
    if b < a:
        res = adaptive_quadrature(f, b, a, tau, max_evals)
        return Result(-res.value, res.error_estimate, res.evaluations, res.converged)
    h = b - a
    fv = (f(a), f(a + 0.25 * h), f(a + 0.5 * h), f(a + 0.75 * h), f(b))  # @line L2
    evals = 5
    q, e = _simpson_pair(a, b, fv)
    counter = 0
    heap: List[Panel] = [(-e, counter, a, b, fv, q)]  # @line L3
    total_q, total_e = q, e  # @line L4
    converged = True
    while total_e > tau:  # @line L5
        if evals + 4 > max_evals:  # @line L6
            converged = False
            break
        neg_e, _, l, r, pv, pq = heapq.heappop(heap)  # @line L7
        m = l + 0.5 * (r - l)
        x1 = l + 0.125 * (r - l)
        x3 = l + 0.375 * (r - l)
        x5 = l + 0.625 * (r - l)
        x7 = l + 0.875 * (r - l)
        if not (l < x1 < x3 < m < x5 < x7 < r):  # @line L8
            heapq.heappush(heap, (neg_e, counter, l, r, pv, pq))
            converged = False
            break
        left = (pv[0], f(x1), pv[1], f(x3), pv[2])  # @line L9
        right = (pv[2], f(x5), pv[3], f(x7), pv[4])
        evals += 4
        ql, el = _simpson_pair(l, m, left)
        qr, er = _simpson_pair(m, r, right)
        total_q += ql + qr - pq  # @line L10
        total_e = max(0.0, total_e + el + er + neg_e)
        counter += 1
        heapq.heappush(heap, (-el, counter, l, m, left, ql))  # @line L11
        counter += 1
        heapq.heappush(heap, (-er, counter, m, r, right, qr))
    value = math.fsum(p[5] for p in heap)  # @line L12
    err = math.fsum(-p[0] for p in heap)
    return Result(value, err, evals, converged and err <= tau)


def adaptive_simpson_local(f: Callable[[float], float], a: float, b: float,
                           tau: float = 1e-10, max_depth: int = 50) -> Tuple[float, int]:
    """Locally adaptive Simpson with an explicit stack.

    A panel is accepted when its estimate is at most its share of tau,
    tau * (r - l)/(b - a). Returns (value, evaluations).
    """
    if a == b:
        return 0.0, 0
    if b < a:
        v, n = adaptive_simpson_local(f, b, a, tau, max_depth)
        return -v, n
    h = b - a
    fv = (f(a), f(a + 0.25 * h), f(a + 0.5 * h), f(a + 0.75 * h), f(b))
    evals = 5
    stack = [(a, b, fv, 0)]
    parts: List[float] = []
    while stack:
        l, r, pv, depth = stack.pop()
        q, e = _simpson_pair(l, r, pv)
        if e <= tau * (r - l) / (b - a) or depth >= max_depth:
            parts.append(q)
            continue
        m = l + 0.5 * (r - l)
        left = (pv[0], f(l + 0.125 * (r - l)), pv[1], f(l + 0.375 * (r - l)), pv[2])
        right = (pv[2], f(l + 0.625 * (r - l)), pv[3], f(l + 0.875 * (r - l)), pv[4])
        evals += 4
        stack.append((m, r, right, depth + 1))
        stack.append((l, m, left, depth + 1))
    return math.fsum(parts), evals
