# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conformal-prediction/. The authors are listed in prov/83RAAM.jsonl.

from fractions import Fraction
from typing import Callable, Iterable, List, Optional, Sequence, Tuple

Point = Tuple[object, object]  # (x, y)
Scores = Callable[[List[Point]], List[object]]


def level(alpha) -> Fraction:
    """alpha as an exact fraction; a float is read as the decimal it prints as (0.1 is 1/10)."""
    a = Fraction(str(alpha)) if isinstance(alpha, float) else Fraction(alpha)
    if not 0 < a < 1:
        raise ValueError("alpha must be in (0, 1)")
    return a


def conformal_p_value(r: Sequence) -> Fraction:
    """#{i : R_i >= R_last} / len(R), the conformal p-value of the last score."""
    return Fraction(sum(1 for v in r if v >= r[-1]), len(r))


def smoothed_p_value(r: Sequence, u) -> object:
    """(#{R_i > R_last} + u #{R_i = R_last}) / len(R), with u uniform on [0, 1]."""
    greater = sum(1 for v in r if v > r[-1])
    equal = sum(1 for v in r if v == r[-1])
    return (greater + u * equal) / len(r)


def full_conformal_set(
    data: Sequence[Point],
    x_new: object,
    candidates: Iterable,
    scores: Scores,
    alpha,
) -> list:
    """The candidates y whose conformal p-value at (x_new, y) is larger than alpha."""
    alpha = level(alpha)
    accepted = []  # @line L1
    for y in candidates:  # @line L2
        bag = list(data) + [(x_new, y)]  # @line L3
        r = scores(bag)  # @line L4
        p = conformal_p_value(r)  # @line L5
        if p > alpha:  # @line L6
            accepted.append(y)
    return accepted  # @line L7


# Nonconformity scores. Each one is a symmetric function of the bag: it refits on all
# n + 1 points, so permuting the bag permutes the scores in the same way.


def mean_scores(bag: List[Point]) -> list:
    """|y_i - mean of the y in the bag|; x is ignored."""
    ys = _numbers([y for _, y in bag])
    m = sum(ys) / len(ys)
    return [abs(y - m) for y in ys]


def least_squares_line(points: Sequence[Point]) -> Tuple[object, object]:
    """Intercept and slope of the least squares line through the points."""
    n = len(points)
    vals = _numbers([x for x, _ in points] + [y for _, y in points])
    xs, ys = vals[:n], vals[n:]
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    return my - slope * mx, slope


def least_squares_scores(bag: List[Point]) -> list:
    """|residual| of each point from the least squares line fitted on the whole bag."""
    a, b = least_squares_line(bag)
    pts = _numbers([v for p in bag for v in p])
    return [abs(pts[2 * i + 1] - a - b * pts[2 * i]) for i in range(len(bag))]


def nearest_neighbour_scores(bag: List[Point]) -> list:
    """Distance to the nearest point with the same label over the distance to the nearest
    point with another label (Vovk, Gammerman and Shafer). x is a number, labels are hashable.
    A point with no other point of its label gets an infinite score."""
    inf = float("inf")
    out = []
    for i, (x, y) in enumerate(bag):
        same = min((abs(x - u) for j, (u, v) in enumerate(bag) if j != i and v == y), default=inf)
        other = min((abs(x - u) for u, v in bag if v != y), default=inf)
        if same == inf or other == 0:
            out.append(inf if same > 0 else 0)
        elif other == inf:
            out.append(0)
        else:
            out.append(Fraction(same) / Fraction(other))
    return out


# Exact full conformal set for the least squares score. The residuals of the bag are
# affine in the candidate y: r_i(y) = a_i + b_i y, so the p-value only changes where
# |r_i(y)| = |r_last(y)|. Evaluating it at those roots and between them gives the set.


def _numbers(values: Sequence) -> list:
    """Fractions if every value is exact, floats otherwise."""
    if all(isinstance(v, (int, Fraction)) for v in values):
        return [Fraction(v) for v in values]
    return [float(v) for v in values]


def least_squares_affine_residuals(data: Sequence[Point], x_new) -> Tuple[list, list]:
    """a, b with r_i(y) = a_i + b_i y the residual of point i (the new point last) from the
    least squares line fitted on the data and (x_new, y)."""
    m = len(data) + 1
    vals = _numbers([x for x, _ in data] + [x_new] + [y for _, y in data] + [0])
    xs, ys = vals[:m], vals[m:]
    mx = sum(xs) / m
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        raise ValueError("the x values must not all be equal")

    def h(i, j):  # the hat matrix of the least squares line
        return (1 + m * (xs[i] - mx) * (xs[j] - mx) / sxx) / m

    a = [ys[i] - sum(h(i, j) * ys[j] for j in range(m)) for i in range(m)]
    b = [(1 if i == m - 1 else 0) - h(i, m - 1) for i in range(m)]
    return a, b


def _count(a, b, y) -> int:
    last = abs(a[-1] + b[-1] * y)
    return sum(1 for ai, bi in zip(a, b) if abs(ai + bi * y) >= last)


def full_conformal_least_squares(
    data: Sequence[Point], x_new, alpha
) -> List[Tuple[Optional[object], Optional[object]]]:
    """The exact full conformal set for least_squares_scores, as closed intervals [lo, hi].
    None stands for an infinite end. The set is a union of these intervals."""
    alpha = level(alpha)
    a, b = least_squares_affine_residuals(data, x_new)
    m = len(a)
    roots = set()
    for ai, bi in zip(a[:-1], b[:-1]):
        for da, db in ((ai - a[-1], bi - b[-1]), (ai + a[-1], bi + b[-1])):
            if db != 0:
                roots.add(-da / db)
    roots = sorted(roots)

    def ok(y) -> bool:
        return _count(a, b, y) > alpha * m

    # pieces in order: gap, root, gap, root, ..., root, gap
    if not roots:
        return [(None, None)] if ok(0) else []
    pieces = [("gap", None, roots[0], ok(roots[0] - 1))]
    for k, r in enumerate(roots):
        pieces.append(("pt", r, r, ok(r)))
        hi = roots[k + 1] if k + 1 < len(roots) else None
        mid = (r + hi) / 2 if hi is not None else r + 1
        pieces.append(("gap", r, hi, ok(mid)))
    out = []
    current = None
    for _, lo, hi, good in pieces:
        if good:
            if current is None:
                current = [lo, hi]
            else:
                current[1] = hi
        elif current is not None:
            out.append(tuple(current))
            current = None
    if current is not None:
        out.append(tuple(current))
    return out


def in_set(intervals, y) -> bool:
    return any((lo is None or lo <= y) and (hi is None or y <= hi) for lo, hi in intervals)
