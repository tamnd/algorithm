# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-area-heuristic/. The authors are listed in prov/948WA8.jsonl.

"""The surface area heuristic: the SAH cost of a BVH, and the best SAH split by a full sweep.

Boxes are pairs (lo, hi) of 3-tuples of ints or Fractions, so all costs are exact.
"""

from fractions import Fraction
import math
import random

Num = int | Fraction
Vec = tuple[Num, Num, Num]
Box = tuple[Vec, Vec]


def area(b: Box | None) -> Num:
    """Surface area 2(wx wy + wy wz + wz wx) of a box; 0 for the empty box (None). Cost: O(1)."""
    if b is None:
        return 0
    w = [b[1][i] - b[0][i] for i in range(3)]
    return 2 * (w[0] * w[1] + w[1] * w[2] + w[2] * w[0])


def union(a: Box | None, b: Box) -> Box:
    if a is None:
        return b
    lo = tuple(min(a[0][i], b[0][i]) for i in range(3))
    hi = tuple(max(a[1][i], b[1][i]) for i in range(3))
    return lo, hi  # type: ignore[return-value]


def tree_cost(tree: dict, c_trav: Num = 1, c_isect: Num = 1) -> Fraction:
    """SAH cost of a tree: sum of c_trav A(v) over inner nodes and c_isect N(v) A(v) over leaves, over A(root).

    A tree is {"box": Box, "children": [tree, ...]} or {"box": Box, "count": int} for a leaf.
    Precondition: the root box has positive area. Cost: O(number of nodes), with an explicit stack.
    """
    total = Fraction(0)
    stack = [tree]
    while stack:
        v = stack.pop()
        if "children" in v:
            total += c_trav * area(v["box"])
            stack.extend(v["children"])
        else:
            total += c_isect * v["count"] * area(v["box"])
    return total / area(tree["box"])


def tree_cost_recursive_form(tree: dict, c_trav: Num = 1, c_isect: Num = 1) -> Fraction:
    """The same cost from the recurrence C(v) = c_trav + sum over children w of A(w)/A(v) C(w), C(leaf) = c_isect N.

    Precondition: every inner box has positive area. Cost: O(number of nodes); computed bottom up.
    """
    order = []
    stack = [tree]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(v.get("children", []))
    cost: dict[int, Fraction] = {}
    for v in reversed(order):  # children come after their parent in order
        if "children" in v:
            cost[id(v)] = c_trav + sum(Fraction(area(w["box"])) / area(v["box"]) * cost[id(w)] for w in v["children"])
        else:
            cost[id(v)] = Fraction(c_isect * v["count"])
    return cost[id(tree)]


def best_sweep_split(boxes: list[Box], c_trav: Num = 1, c_isect: Num = 1) -> tuple[Fraction, int, list[int]]:
    """Best SAH object split of the primitives with the given boxes, by a full sweep on each axis.

    The candidates are the n - 1 splits of the primitives sorted by box center on an axis.
    Return (cost, size of the left part, order of the primitives on the best axis), or the
    leaf (c_isect n, n, order) when no split is cheaper.
    Precondition: n >= 1 and the union of the boxes has positive area. Cost: O(n log n).
    """
    n = len(boxes)
    whole: Box | None = None
    for b in boxes:
        whole = union(whole, b)
    a_s = area(whole)
    best = (Fraction(c_isect * n), n, list(range(n)))  # @line L1
    for axis in range(3):
        order = sorted(range(n), key=lambda i: boxes[i][0][axis] + boxes[i][1][axis])
        right = [Fraction(0)] * (n + 1)  # right[i]: A(R) |R| for R = order[i:]
        acc: Box | None = None
        for i in range(n - 1, 0, -1):
            acc = union(acc, boxes[order[i]])
            right[i] = area(acc) * (n - i)
        acc = None
        for i in range(1, n):  # @line L2
            acc = union(acc, boxes[order[i - 1]])  # @line L3
            cost = c_trav + c_isect * Fraction(area(acc) * i + right[i]) / a_s  # @line L4
            if cost < best[0]:  # @line L5
                best = (cost, i, order)
    return best  # @line L6


def line_hits_box(p: list[float], u: list[float], b: tuple[list[float], list[float]]) -> bool:
    """True if the line p + t u, t real, meets the closed box b. Cost: O(1)."""
    t0, t1 = -math.inf, math.inf
    for a in range(3):
        if u[a] == 0:
            if p[a] < b[0][a] or p[a] > b[1][a]:
                return False
            continue
        ta, tb = (b[0][a] - p[a]) / u[a], (b[1][a] - p[a]) / u[a]
        t0, t1 = max(t0, min(ta, tb)), min(t1, max(ta, tb))
    return t0 <= t1


def random_line(rng: random.Random, center: list[float], radius: float) -> tuple[list[float], list[float]]:
    """A line from the motion-invariant measure, among the lines that pass within radius of center.

    The direction is uniform on the sphere, and the line passes through a point uniform on the
    disk of that radius at center, perpendicular to the direction. Cost: O(1) expected.
    """
    u = [rng.gauss(0, 1) for _ in range(3)]
    s = math.sqrt(sum(x * x for x in u))
    u = [x / s for x in u]
    h = [1.0, 0.0, 0.0] if abs(u[0]) < 0.9 else [0.0, 1.0, 0.0]
    e1 = [u[1] * h[2] - u[2] * h[1], u[2] * h[0] - u[0] * h[2], u[0] * h[1] - u[1] * h[0]]
    s = math.sqrt(sum(x * x for x in e1))
    e1 = [x / s for x in e1]
    e2 = [u[1] * e1[2] - u[2] * e1[1], u[2] * e1[0] - u[0] * e1[2], u[0] * e1[1] - u[1] * e1[0]]
    r, phi = radius * math.sqrt(rng.random()), 2 * math.pi * rng.random()
    p = [center[i] + r * (math.cos(phi) * e1[i] + math.sin(phi) * e2[i]) for i in range(3)]
    return p, u
