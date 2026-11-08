# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kirkpatrick-seidel/. The authors are listed in prov/TZPPQ8.jsonl.

from fractions import Fraction
from typing import TypeVar

Point = tuple[int, int]
T = TypeVar("T", int, Fraction)


def select(values: list[T], k: int) -> T:
    """Return the k-th smallest value (k from 0) by the median-of-medians method.

    Precondition: 0 <= k < len(values). Cost: O(len(values)) comparisons in the worst case;
    the recursion depth is O(log len(values)).
    """
    while True:
        if len(values) <= 10:
            return sorted(values)[k]
        groups = [sorted(values[i : i + 5]) for i in range(0, len(values), 5)]
        medians = [g[(len(g) - 1) // 2] for g in groups]
        pivot = select(medians, (len(medians) - 1) // 2)
        less = [v for v in values if v < pivot]
        equal = sum(1 for v in values if v == pivot)
        if k < len(less):
            values = less
        elif k < len(less) + equal:
            return pivot
        else:
            k -= len(less) + equal
            values = [v for v in values if v > pivot]


def bridge(c: list[Point], m: T) -> tuple[Point, Point]:
    """Return the lower hull edge (l, r) of c with l.x <= m < r.x.

    Precondition: the points of c have distinct x, and min x <= m < max x.
    The returned ends are the leftmost and the rightmost points of c on the bridge line.
    Cost: O(len(c)) time, since each round removes at least a quarter of the points.
    """
    c = list(c)  # @line L12
    while True:  # @line L13
        if len(c) == 2:  # @line L14
            return (c[0], c[1]) if c[0][0] < c[1][0] else (c[1], c[0])
        pairs = []  # @line L15
        rest = [c[-1]] if len(c) % 2 else []
        for i in range(0, len(c) - 1, 2):
            p, q = (c[i], c[i + 1]) if c[i][0] < c[i + 1][0] else (c[i + 1], c[i])
            pairs.append((p, q, Fraction(q[1] - p[1], q[0] - p[0])))
        k = select([s for _, _, s in pairs], (len(pairs) - 1) // 2)  # @line L16
        low = min(p[1] - k * p[0] for p in c)  # @line L17
        contact = [p for p in c if p[1] - k * p[0] == low]
        left, right = min(contact), max(contact)
        if left[0] <= m < right[0]:  # @line L18
            return left, right
        if right[0] <= m:  # @line L19 (the bridge is steeper than k)
            c = rest + [q for p, q, s in pairs if s <= k] + [x for p, q, s in pairs if s > k for x in (p, q)]
        else:  # @line L20 (the bridge is less steep than k)
            c = rest + [p for p, q, s in pairs if s >= k] + [x for p, q, s in pairs if s < k for x in (p, q)]


def lower_hull(s: list[Point]) -> list[Point]:
    """Return the lower hull of s from its lowest leftmost to its lowest rightmost point.

    Precondition: s is nonempty and has no duplicates. Cost: O(n log h) time for n points and
    h output vertices; the explicit stack holds O(log n) tasks.
    """
    lowest: dict[int, Point] = {}  # @line L4
    for p in s:
        if p[0] not in lowest or p[1] < lowest[p[0]][1]:
            lowest[p[0]] = p
    t = list(lowest.values())
    a, b = min(t), max(t)  # @line L5
    out: list[Point] = []
    stack: list[tuple[Point, Point, list[Point]]] = [(a, b, t)]  # @line L6
    while stack:
        a, b, t = stack.pop()
        if a == b:  # @line L7
            out.append(a)
            continue
        m = select([p[0] for p in t], (len(t) + 1) // 2 - 1)  # @line L8
        l, r = bridge(t, m)  # @line L9
        t_l = [p for p in t if p[0] <= l[0]]  # @line L10
        t_r = [p for p in t if p[0] >= r[0]]
        stack.append((r, b, t_r))  # @line L11
        stack.append((a, l, t_l))
    return out


def kirkpatrick_seidel(points: list[Point]) -> list[Point]:
    """Return the vertices of the convex hull of points in counterclockwise order.

    The first vertex is the lexicographically smallest point. Duplicates and points in the
    middle of a hull edge are dropped; with all points collinear the result is the two end
    points. Coordinates must be int or Fraction (exact).
    Cost: O(n log h) time for n points and h hull vertices, O(n) extra space.
    """
    s = list(set(points))  # @line L1
    if len(s) <= 1:
        return s
    lower = lower_hull(s)  # @line L2
    upper = [(-x, -y) for x, y in lower_hull([(-x, -y) for x, y in s])]
    if upper[0] == lower[-1]:  # @line L3
        upper = upper[1:]
    if upper and upper[-1] == lower[0]:
        upper = upper[:-1]
    return lower + upper
