# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cubic-spline-interpolation/. The authors are listed in prov/1BZ0EX.jsonl.

"""Natural and clamped cubic spline interpolation through the second derivatives."""

from bisect import bisect_right
from typing import Any, List, Optional, Sequence


def _sorted(xs, ys):
    if len(xs) < 2 or len(xs) != len(ys):
        raise ValueError("need at least two knots and as many values")
    if len(set(xs)) != len(xs):
        raise ValueError("the knots must be distinct")
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    return [xs[i] for i in order], [ys[i] for i in order]


def spline_moments(xs: Sequence[Any], ys: Sequence[Any], da: Optional[Any] = None,
                   db: Optional[Any] = None) -> List[Any]:
    """Return M_k = s''(x_k) for increasing knots xs.

    Natural end conditions (s'' = 0 at both ends) unless the end slopes da and db
    are given, which gives the clamped spline. Cost: about 15n operations.
    """
    clamped = da is not None or db is not None
    if clamped and (da is None or db is None):
        raise ValueError("give both end slopes for a clamped spline")
    n = len(xs) - 1
    h, dl = [], []
    for k in range(n):  # @line L1
        h.append(xs[k + 1] - xs[k])
        dl.append((ys[k + 1] - ys[k]) / h[k])
    zero = 0 * dl[0]
    sub = [zero] * (n + 1)  # @line L2
    dia = [zero + 1] * (n + 1)
    sup = [zero] * (n + 1)
    rhs = [zero] * (n + 1)
    for k in range(1, n):  # @line L3
        sub[k], dia[k], sup[k] = h[k - 1], 2 * (h[k - 1] + h[k]), h[k]
        rhs[k] = 6 * (dl[k] - dl[k - 1])
    if clamped:  # @line L4
        dia[0], sup[0], rhs[0] = 2 * h[0], h[0], 6 * (dl[0] - da)
        sub[n], dia[n], rhs[n] = h[n - 1], 2 * h[n - 1], 6 * (db - dl[n - 1])
    # Thomas algorithm: forward elimination, then back substitution.
    for k in range(1, n + 1):  # @line L5
        m = sub[k] / dia[k - 1]
        dia[k] = dia[k] - m * sup[k - 1]
        rhs[k] = rhs[k] - m * rhs[k - 1]
    mom = [zero] * (n + 1)
    mom[n] = rhs[n] / dia[n]
    for k in range(n - 1, -1, -1):
        mom[k] = (rhs[k] - sup[k] * mom[k + 1]) / dia[k]
    return mom


def spline_eval(xs: Sequence[Any], ys: Sequence[Any], mom: Sequence[Any], t: Any) -> Any:
    """Value at t of the cubic spline with knots xs, values ys and moments mom."""
    n = len(xs) - 1
    k = min(max(bisect_right(xs, t) - 1, 0), n - 1)  # @line L6
    h = xs[k + 1] - xs[k]  # @line L7
    a = xs[k + 1] - t
    b = t - xs[k]
    cubic = (mom[k] * a * a * a + mom[k + 1] * b * b * b) / (6 * h)  # @line L8
    lin = (ys[k] / h - mom[k] * h / 6) * a + (ys[k + 1] / h - mom[k + 1] * h / 6) * b
    return cubic + lin  # @line L9


def cubic_spline_interpolation(xs: Sequence[Any], ys: Sequence[Any], t: Any,
                               da: Optional[Any] = None, db: Optional[Any] = None) -> Any:
    """Value at t of the natural (default) or clamped (da, db given) cubic spline.

    Knots may be in any order; they are sorted with their values.
    """
    sx, sy = _sorted(xs, ys)
    return spline_eval(sx, sy, spline_moments(sx, sy, da, db), t)
