# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cubic-hermite-spline/. The authors are listed in prov/667FMQ.jsonl.

"""Piecewise cubic Hermite interpolation with given or estimated slopes."""

from bisect import bisect_right
from typing import Any, List, Sequence, Tuple


def _sorted_data(xs, ys, ds=None) -> Tuple[list, list, list]:
    if len(xs) < 2 or len(xs) != len(ys) or (ds is not None and len(ds) != len(xs)):
        raise ValueError("need at least two knots and matching lengths")
    if len(set(xs)) != len(xs):
        raise ValueError("the knots must be distinct")
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    return ([xs[i] for i in order], [ys[i] for i in order],
            None if ds is None else [ds[i] for i in order])


def hermite_eval_sorted(xs: Sequence[Any], ys: Sequence[Any], ds: Sequence[Any], t: Any) -> Any:
    """Evaluate the C^1 piecewise cubic with s(x_k) = y_k, s'(x_k) = d_k.

    xs must be strictly increasing. Outside [x_0, x_n] the end cubic is extended.
    Cost: O(log n) comparisons and 24 arithmetic operations.
    """
    n = len(xs) - 1
    k = min(max(bisect_right(xs, t) - 1, 0), n - 1)  # @line L1
    h = xs[k + 1] - xs[k]  # @line L2
    s = (t - xs[k]) / h  # @line L3
    h00 = (1 + 2 * s) * (1 - s) ** 2  # @line L4
    h10 = s * (1 - s) ** 2
    h01 = s * s * (3 - 2 * s)  # @line L5
    h11 = s * s * (s - 1)
    return h00 * ys[k] + h * h10 * ds[k] + h01 * ys[k + 1] + h * h11 * ds[k + 1]  # @line L6


def cubic_hermite_spline(xs: Sequence[Any], ys: Sequence[Any], ds: Sequence[Any], t: Any) -> Any:
    """Value at t of the cubic Hermite spline through (x_k, y_k) with slopes d_k.

    The knots may be given in any order; they are sorted together with the data.
    """
    sx, sy, sd = _sorted_data(xs, ys, ds)
    return hermite_eval_sorted(sx, sy, sd, t)


def three_point_slopes(xs: Sequence[Any], ys: Sequence[Any]) -> List[Any]:
    """Bessel slopes: d_k is the slope at x_k of the parabola through three
    consecutive points (the first or last three at the ends). Two knots give
    the slope of the chord. xs must be strictly increasing."""
    n = len(xs) - 1
    if n == 1:
        m = (ys[1] - ys[0]) / (xs[1] - xs[0])
        return [m, m]

    def parabola_slope(i, at):
        # derivative at xs[at] of the quadratic through points i, i+1, i+2
        a, b, c = xs[i], xs[i + 1], xs[i + 2]
        fa, fb, fc = ys[i], ys[i + 1], ys[i + 2]
        d1 = (fb - fa) / (b - a)
        d2 = (fc - fb) / (c - b)
        dd = (d2 - d1) / (c - a)
        x = xs[at]
        return d1 + dd * ((x - a) + (x - b))

    ds = [parabola_slope(0, 0)]
    for k in range(1, n):
        ds.append(parabola_slope(k - 1, k))
    ds.append(parabola_slope(n - 2, n))
    return ds
