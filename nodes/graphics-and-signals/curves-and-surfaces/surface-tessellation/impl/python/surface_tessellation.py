# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-tessellation/. The authors are listed in prov/FWMAHV.jsonl.

"""Uniform tessellation of tensor product Bezier patches into triangles.

A patch is a net P[i][j] of 3D points, with i = 0..m along u and j = 0..n
along v. A patch is cut into s_u by s_v parameter cells, and each cell into two
triangles. The step counts come from a proved bound on the distance between
the patch and its triangles, and are made equal on shared edges, so that the
mesh has no cracks. On Fraction input the vertices are exact, and shared edge
vertices from two patches are the same point.
"""

import math
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

Point = Tuple
Net = Sequence[Sequence[Point]]


def _lerp(a: Point, b: Point, t) -> Point:
    return tuple(x + t * (y - x) for x, y in zip(a, b))


def _de_casteljau(points: Sequence[Point], t) -> Point:
    pts = list(points)
    for r in range(1, len(pts)):
        for i in range(len(pts) - r):
            pts[i] = _lerp(pts[i], pts[i + 1], t)
    return pts[0]


def patch_point(net: Net, u, v) -> Point:
    """S(u, v) by de Casteljau on each row of the net, then on the column of results."""
    return _de_casteljau([_de_casteljau(row, v) for row in net], u)


def _norm(p: Point) -> float:
    return math.sqrt(sum(float(x) * float(x) for x in p))


def second_derivative_bounds(net: Net) -> Tuple[float, float, float]:
    """Upper bounds (M_uu, M_uv, M_vv) on |S_uu|, |S_uv|, |S_vv| over the whole patch.

    S_uu is a Bezier patch with the control points m(m-1) times the second
    differences in i, so its norm is at most the largest norm of those points
    (convex hull property). The same holds for S_uv and S_vv.
    """
    m, n = len(net) - 1, len(net[0]) - 1
    d = lambda a, b, c: tuple(x - 2 * y + z for x, y, z in zip(a, b, c))
    q = lambda a, b, c, e: tuple(w - x - y + z for w, x, y, z in zip(a, b, c, e))
    muu = max((_norm(d(net[i][j], net[i + 1][j], net[i + 2][j]))
               for i in range(m - 1) for j in range(n + 1)), default=0.0) * m * (m - 1)
    mvv = max((_norm(d(net[i][j], net[i][j + 1], net[i][j + 2]))
               for i in range(m + 1) for j in range(n - 1)), default=0.0) * n * (n - 1)
    muv = max((_norm(q(net[i + 1][j + 1], net[i + 1][j], net[i][j + 1], net[i][j]))
               for i in range(m) for j in range(n)), default=0.0) * m * n
    return muu, muv, mvv


def chordal_bound(net: Net, su: int, sv: int) -> float:
    """A proved upper bound on |S(p) - T(p)| over the patch, where T is the triangulation."""
    muu, muv, mvv = second_derivative_bounds(net)
    hu, hv = 1 / su, 1 / sv
    return (muu * hu * hu + 2 * muv * hu * hv + mvv * hv * hv) / 8


def steps_for_tolerance(net: Net, tol: float) -> Tuple[int, int]:
    """The smallest (s_u, s_v) of this simple rule that makes chordal_bound <= tol.

    2 M_uv h_u h_v <= M_uv (h_u^2 + h_v^2), so it is enough that
    (M_uu + M_uv) h_u^2 <= 4 tol and (M_vv + M_uv) h_v^2 <= 4 tol.
    """
    muu, muv, mvv = second_derivative_bounds(net)  # @line L1
    su = max(1, math.ceil(math.sqrt((muu + muv) / (4 * tol))))  # @line L2
    sv = max(1, math.ceil(math.sqrt((mvv + muv) / (4 * tol))))
    return su, sv


def _edge_keys(net: Net):
    """The four boundary control polygons, each in a direction-free form.

    Two patches share an edge exactly when they have the same key there.
    Returned in the order v = 0, v = 1 (they use s_u), u = 0, u = 1 (they use s_v).
    """
    m, n = len(net) - 1, len(net[0]) - 1
    sides = ([net[i][0] for i in range(m + 1)], [net[i][n] for i in range(m + 1)],
             [net[0][j] for j in range(n + 1)], [net[m][j] for j in range(n + 1)])
    return [min(tuple(s), tuple(reversed(s))) for s in sides]


def consistent_steps(nets: Sequence[Net], wanted: Sequence[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Step counts that agree on every shared edge and are at least the wanted ones.

    Union-find over patch edges: the two edges of a patch that use s_u go in
    one class, the two that use s_v in another, and equal edges of different
    patches are joined. Each class takes the largest count wanted by a member.
    """
    parent: Dict = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for p, net in enumerate(nets):
        k = _edge_keys(net)
        union(("u", p), k[0])  # @line L3
        union(("u", p), k[1])
        union(("v", p), k[2])
        union(("v", p), k[3])
    best: Dict = {}
    for p, (su, sv) in enumerate(wanted):
        for tag, s in (("u", su), ("v", sv)):
            r = find((tag, p))
            best[r] = max(best.get(r, 1), s)  # @line L4
    return [(best[find(("u", p))], best[find(("v", p))]) for p in range(len(nets))]


def tessellate(nets: Sequence[Net], steps: Sequence[Tuple[int, int]]):
    """(vertices, triangles). Vertices with equal coordinates are merged.

    Each triangle is a triple of vertex indices, ordered so that its normal
    has the direction of S_u x S_v.
    """
    index: Dict[Point, int] = {}
    verts: List[Point] = []
    tris: List[Tuple[int, int, int]] = []

    def vid(p: Point) -> int:
        if p not in index:
            index[p] = len(verts)
            verts.append(p)
        return index[p]

    for net, (su, sv) in zip(nets, steps):
        g = [[vid(patch_point(net, Fraction(i, su), Fraction(j, sv))) for j in range(sv + 1)]  # @line L5 L6
             for i in range(su + 1)]
        for i in range(su):  # @line L7
            for j in range(sv):
                a, b, c, d = g[i][j], g[i + 1][j], g[i + 1][j + 1], g[i][j + 1]
                tris.append((a, b, c))  # @line L8
                tris.append((a, c, d))
    return verts, tris


def boundary_edges(tris: Sequence[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    """Directed edges whose reverse is not in the mesh. Empty for a closed, oriented mesh."""
    seen: Dict[Tuple[int, int], int] = {}
    for a, b, c in tris:
        for e in ((a, b), (b, c), (c, a)):
            seen[e] = seen.get(e, 0) + 1
    return [e for e, k in seen.items() if k != 1 or seen.get((e[1], e[0]), 0) != 1]


def euler_characteristic(verts, tris) -> int:
    edges = {frozenset(e) for a, b, c in tris for e in ((a, b), (b, c), (c, a))}
    return len(verts) - len(edges) + len(tris)


def max_deviation(net: Net, su: int, sv: int, dense: int = 8) -> float:
    """The largest |S(p) - T(p)| over dense samples p inside every triangle (float)."""
    fnet = [[tuple(float(x) for x in p) for p in row] for row in net]
    grid = [[patch_point(fnet, i / su, j / sv) for j in range(sv + 1)] for i in range(su + 1)]
    worst = 0.0
    for i in range(su):
        for j in range(sv):
            a, b, c, d = grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]
            for x in range(dense + 1):
                for y in range(dense + 1):
                    s, t = x / dense, y / dense       # local coordinates in the cell
                    if s >= t:                        # triangle (a, b, c)
                        lin = tuple(p + s * (q - p) + t * (r - q) for p, q, r in zip(a, b, c))
                    else:                             # triangle (a, c, d)
                        lin = tuple(p + t * (r - p) + s * (q - r) for p, q, r in zip(a, c, d))
                    exact = patch_point(fnet, (i + s) / su, (j + t) / sv)
                    worst = max(worst, math.dist(exact, lin))
    return worst
