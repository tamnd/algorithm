# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadric-error-metrics/. The authors are listed in prov/HHFZ8A.jsonl.

"""Mesh simplification with quadric error metrics (Garland and Heckbert 1997).

Each triangle defines a plane p = (a, b, c, d) with a x + b y + c z + d = 0.
Its fundamental quadric is K = p p^T / (a^2 + b^2 + c^2), so that for
v = (x, y, z, 1), v^T K v is the squared distance from v to the plane. A
vertex starts with the sum of the quadrics of its triangles. The algorithm
collapses edges greedily: the cost of the edge (i, j) is v^T (Q_i + Q_j) v at
the position v that minimizes it, and a binary heap gives the cheapest edge.
After a collapse the merged vertex keeps Q_i + Q_j. Collapses that break the
link condition, or flip or flatten a triangle, are skipped.

The arithmetic is exact with Fraction coordinates (the quadric uses
1 / |n|^2, not 1 / |n|), and works with floats as well.
"""

import heapq
from fractions import Fraction
from typing import Union

Number = Union[int, float, Fraction]
Vec = tuple[Number, Number, Number]
Quadric = tuple[Number, ...]  # 10 entries: a2 ab ac ad b2 bc bd c2 cd d2


def _sub(p: Vec, q: Vec) -> Vec:
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _cross(u: Vec, v: Vec) -> Vec:
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _dot(u: Vec, v: Vec) -> Number:
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _div(a: Number, b: Number) -> Number:
    if isinstance(a, float) or isinstance(b, float):
        return a / b
    return Fraction(a) / b


def plane_quadric(p0: Vec, p1: Vec, p2: Vec) -> Quadric:
    """K = p p^T / |n|^2 for the plane of the triangle; zero for a degenerate triangle."""
    n = _cross(_sub(p1, p0), _sub(p2, p0))
    nn = _dot(n, n)
    if nn == 0:
        return (0,) * 10
    a, b, c = n
    d = -_dot(n, p0)
    s = [a, b, c, d]
    return tuple(_div(s[i] * s[j], nn) for i in range(4) for j in range(i, 4))


def add(q: Quadric, r: Quadric) -> Quadric:
    return tuple(x + y for x, y in zip(q, r))


def error(q: Quadric, v: Vec) -> Number:
    """v^T Q v with v = (x, y, z, 1)."""
    a2, ab, ac, ad, b2, bc, bd, c2, cd, d2 = q
    x, y, z = v
    return (a2 * x * x + 2 * ab * x * y + 2 * ac * x * z + 2 * ad * x
            + b2 * y * y + 2 * bc * y * z + 2 * bd * y + c2 * z * z + 2 * cd * z + d2)


def optimal_position(q: Quadric, vi: Vec, vj: Vec) -> Vec:
    """The minimizer of v^T Q v if the 3 by 3 part is invertible, else the best of vi, vj, midpoint."""
    a2, ab, ac, ad, b2, bc, bd, c2, cd, _ = q
    det = a2 * (b2 * c2 - bc * bc) - ab * (ab * c2 - bc * ac) + ac * (ab * bc - b2 * ac)
    scale = max(abs(x) for x in (a2, b2, c2)) or 1
    if det != 0 and not (isinstance(det, float) and abs(det) < 1e-10 * scale ** 3):  # @line L11
        # Cramer's rule for A v = -(ad, bd, cd)
        r = (-ad, -bd, -cd)
        dx = r[0] * (b2 * c2 - bc * bc) - ab * (r[1] * c2 - bc * r[2]) + ac * (r[1] * bc - b2 * r[2])
        dy = a2 * (r[1] * c2 - bc * r[2]) - r[0] * (ab * c2 - bc * ac) + ac * (ab * r[2] - r[1] * ac)
        dz = a2 * (b2 * r[2] - r[1] * bc) - ab * (ab * r[2] - r[1] * ac) + r[0] * (ab * bc - b2 * ac)
        return (_div(dx, det), _div(dy, det), _div(dz, det))
    mid = tuple(_div(vi[t] + vj[t], 2) for t in range(3))
    return min((vi, vj, mid), key=lambda v: error(q, v))


def simplify(verts: list[Vec], tris: list[tuple[int, int, int]], target: int,
             trace: list | None = None) -> tuple[list[Vec], list[tuple[int, int, int]]]:
    """Collapse edges of a closed or open triangle mesh until at most target triangles remain.

    Returns the compacted mesh. If trace is a list, each collapse (cost, i, j)
    is appended to it in order (with the vertex numbers of the input).
    """
    pos = list(verts)
    faces: dict[int, tuple[int, int, int]] = dict(enumerate(tris))
    at: list[set[int]] = [set() for _ in verts]  # faces at each vertex
    for f, t in faces.items():
        for v in t:
            at[v].add(f)
    kq = {f: plane_quadric(*(pos[v] for v in t)) for f, t in faces.items()}  # @line L1
    zero: Quadric = (0,) * 10
    quad = [zero] * len(verts)
    for f, t in faces.items():
        for v in t:
            quad[v] = add(quad[v], kq[f])  # @line L2
    version = [0] * len(verts)
    heap: list = []
    blocked: dict = {}  # edges that failed the test of line L6, until their neighborhood changes
    blocked_at: list[set] = [set() for _ in verts]

    def push(i: int, j: int) -> None:
        if i > j:
            i, j = j, i
        q = add(quad[i], quad[j])
        v = optimal_position(q, pos[i], pos[j])
        heapq.heappush(heap, (error(q, v), i, j, version[i], version[j], v))

    def neighbors(i: int) -> set[int]:
        return {u for f in at[i] for u in faces[f]} - {i}

    def border_neighbors(i: int) -> set[int]:
        """The u such that the edge (i, u) is in exactly one face."""
        count: dict[int, int] = {}
        for f in at[i]:
            for u in faces[f]:
                if u != i:
                    count[u] = count.get(u, 0) + 1
        return {u for u, k in count.items() if k == 1}

    def valid(i: int, j: int, v: Vec) -> bool:
        shared = at[i] & at[j]
        if not shared:
            return False
        opposite = {u for f in shared for u in faces[f]} - {i, j}
        if neighbors(i) & neighbors(j) != opposite:  # the link condition, on vertices
            return False
        link_i = {frozenset(faces[f]) - {i} for f in at[i]}
        link_j = {frozenset(faces[f]) - {j} for f in at[j]}
        if link_i & link_j:  # and on edges: faces (i, u, w) and (j, u, w) would merge
            return False
        # On a mesh with a border, the border acts as one more vertex in every link.
        bi, bj = border_neighbors(i), border_neighbors(j)
        if bi and bj and j not in bi:  # two border vertices joined by an inner edge
            return False
        if bi & bj:  # border edges (i, u) and (j, u) would merge
            return False
        for f in (at[i] | at[j]) - shared:  # surviving faces must not flip or flatten
            t = faces[f]
            old = _cross(_sub(pos[t[1]], pos[t[0]]), _sub(pos[t[2]], pos[t[0]]))
            new_pts = [v if u in (i, j) else pos[u] for u in t]
            new = _cross(_sub(new_pts[1], new_pts[0]), _sub(new_pts[2], new_pts[0]))
            if _dot(old, new) <= 0:
                return False
        return True

    edges = {(min(a, b), max(a, b)) for t in faces.values() for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0]))}
    for i, j in sorted(edges):
        push(i, j)  # @line L3
    while len(faces) > target and heap:  # @line L4
        cost, i, j, vi, vj, v = heapq.heappop(heap)  # @line L5
        if vi != version[i] or vj != version[j] or not at[i] or not at[j]:
            continue  # stale entry: an end point has moved or is gone
        if not valid(i, j, v):  # @line L6
            blocked[(i, j)] = (cost, i, j, vi, vj, v)
            blocked_at[i].add((i, j))
            blocked_at[j].add((i, j))
            continue
        if trace is not None:
            trace.append((cost, i, j))
        pos[i] = v  # @line L7
        quad[i] = add(quad[i], quad[j])
        for f in at[i] & at[j]:  # @line L8
            for u in faces[f]:
                if u not in (i, j):
                    at[u].discard(f)
            del faces[f]
        for f in at[j] - at[i]:
            faces[f] = tuple(i if u == j else u for u in faces[f])
        at[i] = (at[i] | at[j]) & set(faces)
        at[j] = set()
        version[i] += 1
        version[j] += 1
        ring = neighbors(i)
        for k in sorted(ring):
            push(i, k)  # @line L9
        # The validity of an edge depends only on the faces at its two end points, so only
        # blocked edges with an end point in {i} and its neighbors can have become valid.
        for u in ring | {i, j}:
            for key in blocked_at[u]:
                entry = blocked.pop(key, None)
                if entry is not None:
                    heapq.heappush(heap, entry)
            blocked_at[u] = set()
    keep = sorted({u for t in faces.values() for u in t})
    new_index = {u: t for t, u in enumerate(keep)}
    out_tris = [tuple(new_index[u] for u in faces[f]) for f in sorted(faces)]
    return [pos[u] for u in keep], out_tris  # @line L10
