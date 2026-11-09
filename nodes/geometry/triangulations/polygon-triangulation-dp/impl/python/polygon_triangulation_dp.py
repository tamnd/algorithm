# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polygon-triangulation-dp/. The authors are listed in prov/2ZMWQH.jsonl.

from typing import Callable

Point = tuple[int, int]
Weight = Callable[[int, int, int], object]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of pqr: positive for a left turn. Exact for int and Fraction."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def _on_segment(p: Point, a: Point, b: Point) -> bool:
    return (orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def is_diagonal(q: list[Point], i: int, j: int) -> bool:
    """True when q[i]q[j] is a diagonal of the counterclockwise simple polygon q."""
    n = len(q)
    a, b = q[i], q[j]
    for k in range(n):  # @line L9
        if k != i and k != j and _on_segment(q[k], a, b):
            return False
        c, d = q[k], q[(k + 1) % n]
        if orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0:
            return False
    prv, nxt = q[i - 1], q[(i + 1) % n]  # @line L10
    if orient(prv, a, nxt) > 0:  # convex corner: b strictly inside the cone
        return orient(a, b, prv) > 0 and orient(b, a, nxt) > 0
    return not (orient(a, b, nxt) >= 0 and orient(b, a, prv) >= 0)


def _ccw_order(poly: list[Point]) -> list[int]:
    n = len(poly)
    area2 = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    if area2 == 0:
        raise ValueError("the polygon has zero area, so it is not simple")
    return list(range(n)) if area2 > 0 else list(range(n - 1, -1, -1))


def _valid_pairs(poly: list[Point], order: list[int]) -> list[list[bool]]:
    n = len(order)
    q = [poly[v] for v in order]
    ok = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            ok[i][j] = j == i + 1 or (i == 0 and j == n - 1) or is_diagonal(q, i, j)
    return ok


def optimal_triangulation(poly: list[Point], weight: Weight) -> tuple[object, list[tuple[int, int, int]]]:
    """Minimum total weight triangulation of a simple polygon.

    weight(a, b, c) is the cost of the triangle with vertex indices a, b, c (indices into poly,
    in counterclockwise order of the triangle). Costs must support + and <. Returns the least
    total cost and the n - 2 counterclockwise index triangles of one optimal triangulation.
    """
    n = len(poly)
    if n < 3:
        return 0, []
    order = _ccw_order(poly)  # @line L1
    ok = _valid_pairs(poly, order)  # @line L2
    cost: list[list[object]] = [[None] * n for _ in range(n)]
    split = [[-1] * n for _ in range(n)]
    for i in range(n - 1):  # @line L3
        cost[i][i + 1] = 0
    for d in range(2, n):  # @line L4
        for i in range(n - d):  # @line L5
            j = i + d
            if not ok[i][j]:
                continue
            best, arg = None, -1
            for k in range(i + 1, j):  # @line L6
                if ok[i][k] and ok[k][j] and cost[i][k] is not None and cost[k][j] is not None:
                    c = cost[i][k] + cost[k][j] + weight(order[i], order[k], order[j])
                    if best is None or c < best:
                        best, arg = c, k
            cost[i][j], split[i][j] = best, arg
    tris: list[tuple[int, int, int]] = []
    stack = [(0, n - 1)]  # @line L7
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        k = split[i][j]
        tris.append((order[i], order[k], order[j]))
        stack.append((i, k))
        stack.append((k, j))
    return cost[0][n - 1], tris  # @line L8


def count_triangulations(poly: list[Point]) -> int:
    """Number of triangulations of a simple polygon, by the same recurrence with sums."""
    n = len(poly)
    if n < 3:
        return 0
    order = _ccw_order(poly)
    ok = _valid_pairs(poly, order)
    cnt = [[0] * n for _ in range(n)]
    for i in range(n - 1):
        cnt[i][i + 1] = 1
    for d in range(2, n):
        for i in range(n - d):
            j = i + d
            if ok[i][j]:
                cnt[i][j] = sum(cnt[i][k] * cnt[k][j] for k in range(i + 1, j) if ok[i][k] and ok[k][j])
    return cnt[0][n - 1]
