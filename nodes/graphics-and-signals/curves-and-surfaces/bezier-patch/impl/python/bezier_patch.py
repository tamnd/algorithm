# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bezier-patch/. The authors are listed in prov/NCXHRX.jsonl.

"""Tensor product Bezier patches.

A patch of degree (m, n) has a control net P[i][j], i = 0..m in the u
direction and j = 0..n in the v direction. Each control point is a tuple of
numbers. The code uses only +, - and *, so it runs exactly on Fraction input
and in floating point on float input.
"""

from typing import List, Sequence, Tuple

Point = Tuple
Net = Sequence[Sequence[Point]]


def lerp(a: Point, b: Point, t) -> Point:
    """The point (1 - t) a + t b."""
    s = 1 - t
    return tuple(s * x + t * y for x, y in zip(a, b))


def de_casteljau(points: Sequence[Point], t) -> Point:
    """The point at t of the Bezier curve with these control points."""
    if not points:
        raise ValueError("a Bezier curve needs at least one control point")
    level: List[Point] = list(points)
    for r in range(1, len(level)):
        for i in range(len(level) - r):
            level[i] = lerp(level[i], level[i + 1], t)
    return level[0]


def degree(net: Net) -> Tuple[int, int]:
    """The degree (m, n) of a rectangular net, after a check of its shape."""
    if not net or not net[0]:
        raise ValueError("the control net is empty")
    n1 = len(net[0])
    if any(len(row) != n1 for row in net):
        raise ValueError("the rows of the control net have different lengths")
    return len(net) - 1, n1 - 1


def patch_point(net: Net, u, v) -> Point:
    """S(u, v) by de Casteljau in each direction.

    The first pass runs the curve algorithm along the direction of lower
    degree, once for each line of the net. The second pass runs it on the
    points that the first pass made. Along v first, the cost is
    (m + 1) n (n + 1) / 2 + m (m + 1) / 2 interpolations, and this is the
    smaller of the two orders exactly when n <= m.
    """
    m, n = degree(net)
    if n <= m:  # @line L1
        col = [de_casteljau(row, v) for row in net]  # @line L2 L3
        return de_casteljau(col, u)  # @line L4
    # @line L5
    rows = [de_casteljau([net[i][j] for i in range(m + 1)], u) for j in range(n + 1)]  # @line L6 L7
    return de_casteljau(rows, v)  # @line L8


def patch_point_bilinear(net: Net, u, v) -> Point:
    """S(u, v) by the two-dimensional de Casteljau algorithm.

    Each step replaces four neighbouring points by their bilinear blend.
    After min(m, n) steps the net is a single line, and a curve step ends it.
    """
    m, n = degree(net)
    level = [list(row) for row in net]
    for _ in range(min(m, n)):
        level = [[lerp(lerp(level[i][j], level[i][j + 1], v),
                       lerp(level[i + 1][j], level[i + 1][j + 1], v), u)
                  for j in range(len(level[0]) - 1)]
                 for i in range(len(level) - 1)]
    if len(level) == 1:
        return de_casteljau(level[0], v)
    return de_casteljau([row[0] for row in level], u)


def difference_net(net: Net, du: int, dv: int) -> List[List[Point]]:
    """The net of the partial derivative of order (du, dv), with its factor."""
    m, n = degree(net)
    cur = [list(row) for row in net]
    scale = 1
    for k in range(du):
        scale *= m - k
        cur = [[tuple(y - x for x, y in zip(cur[i][j], cur[i + 1][j]))
                for j in range(len(cur[0]))] for i in range(len(cur) - 1)]
    for k in range(dv):
        scale *= n - k
        cur = [[tuple(y - x for x, y in zip(row[j], row[j + 1]))
                for j in range(len(row) - 1)] for row in cur]
    if not cur or not cur[0]:
        dim = len(net[0][0])
        return [[tuple(0 for _ in range(dim))]]
    return [[tuple(scale * x for x in p) for p in row] for row in cur]


def patch_derivative(net: Net, u, v, du: int = 1, dv: int = 0) -> Point:
    """The partial derivative of order (du, dv) of S at (u, v)."""
    return patch_point(difference_net(net, du, dv), u, v)


def split_u(net: Net, u) -> Tuple[List[List[Point]], List[List[Point]]]:
    """Split the patch at the line u = const into two patches of the same degree."""
    m, n = degree(net)
    left = [[None] * (n + 1) for _ in range(m + 1)]
    right = [[None] * (n + 1) for _ in range(m + 1)]
    for j in range(n + 1):
        level = [net[i][j] for i in range(m + 1)]
        for r in range(m + 1):
            left[r][j] = level[0]
            right[m - r][j] = level[-1]
            level = [lerp(level[i], level[i + 1], u) for i in range(len(level) - 1)]
    return left, right
