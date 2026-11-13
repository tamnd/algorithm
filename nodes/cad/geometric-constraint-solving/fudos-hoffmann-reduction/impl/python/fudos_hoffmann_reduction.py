# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fudos-hoffmann-reduction/. The authors are listed in prov/G145A2.jsonl.

"""Fudos-Hoffmann bottom-up triangle reduction, for points and distances in the plane.

A cluster is a set of points whose relative placement is fixed. The reduction starts
with one cluster per distance constraint and merges three clusters that pairwise share
one point, at three different points. The solver then places the clusters in the order
of the merges, one circle-circle intersection per merge.
"""

from math import sqrt

Edge = tuple[int, int]
Merge = tuple[frozenset[int], frozenset[int], frozenset[int]]


def reduce_clusters(n: int, edges: list[Edge]) -> tuple[list[frozenset[int]], list[Merge]]:
    """Run the triangle reduction on the constraint graph (range(n), edges).

    Precondition: the edges are distinct pairs of distinct vertices in range(n), and
    the graph is Laman-sparse (every k >= 2 vertices span at most 2k - 3 edges).
    Returns the final clusters and the merges (A, B, C) in the order they were made.
    Raises ValueError if two clusters share two vertices; this can only happen if the
    graph is not Laman-sparse. Not every graph that is not sparse is detected.
    Cost: O(n + m) space and O((n + m) * (number of clusters)) time, which is O(n^2)
    for m <= 2n - 3.
    """
    members: dict[int, frozenset[int]] = {}
    of_vertex: list[set[int]] = [set() for _ in range(n)]
    seen_edges: set[frozenset[int]] = set()
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError("bad edge")
        e = frozenset((u, v))
        if e in seen_edges:
            raise ValueError("repeated edge")
        seen_edges.add(e)
        k = len(members)
        members[k] = e  # @line L1
        of_vertex[u].add(k)
        of_vertex[v].add(k)
    next_id = len(members)
    work = list(members)  # @line L2
    plan: list[Merge] = []
    while work:  # @line L3
        a = work.pop()  # @line L4
        if a not in members:
            continue
        ca = members[a]
        shared: dict[int, int] = {}  # cluster that meets A -> the vertex it shares with A
        for v in ca:  # @line L5
            for b in of_vertex[v]:
                if b == a:
                    continue
                if b in shared:  # @line L6
                    raise ValueError("over-constrained: two clusters share two points")
                shared[b] = v
        holder: dict[int, int] = {}  # vertex outside A -> a cluster that meets A and holds it
        found: tuple[int, int] | None = None
        for b, vb in shared.items():  # @line L7
            for x in members[b]:
                if x in ca:
                    continue
                c = holder.get(x)
                if c is None:
                    holder[x] = b
                    continue
                if shared[c] == vb:
                    raise ValueError("over-constrained: two clusters share two points")
                found = (b, c)
                break
            if found is not None:
                break
        if found is None:  # @line L8
            continue
        b, c = found
        cb, cc = members[b], members[c]
        plan.append((ca, cb, cc))  # @line L9
        new = ca | cb | cc
        for k in (a, b, c):  # @line L10
            for v in members.pop(k):
                of_vertex[v].discard(k)
        members[next_id] = new
        for v in new:
            of_vertex[v].add(next_id)
        work.append(next_id)
        next_id += 1
    return list(members.values()), plan  # @line L11


def is_triangle_decomposable(n: int, edges: list[Edge]) -> bool:
    """True if the reduction ends with one cluster that holds all n vertices."""
    if n == 1 and not edges:
        return True
    clusters, _ = reduce_clusters(n, edges)
    return len(clusters) == 1 and len(clusters[0]) == n


def orient(p: tuple[int, int], q: tuple[int, int], r: tuple[int, int]) -> int:
    """Sign of the orientation determinant of three integer points, computed exactly."""
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (d > 0) - (d < 0)


def _third_point(p: complex, q: complex, r1: float, r2: float, side: int) -> complex:
    """The point at distance r1 from p and r2 from q, to the left of p->q if side > 0."""
    d = abs(q - p)
    if d == 0.0:
        raise ValueError("two points of a triangle coincide")
    x = (d * d + r1 * r1 - r2 * r2) / (2.0 * d)
    h2 = r1 * r1 - x * x
    scale = max(r1, r2, d) ** 2
    if h2 < -1e-9 * scale:
        raise ValueError("no real solution: the circles do not meet")
    h = sqrt(h2) if h2 > 0.0 else 0.0
    ex = (q - p) / d
    return p + ex * complex(x, h if side > 0 else -h)


def _move(pts: dict[int, complex], u: int, w: int, pu: complex, pw: complex) -> dict[int, complex]:
    """Apply the proper rigid motion that takes pts[u], pts[w] to pu and a point on the ray to pw."""
    z = (pw - pu) / (pts[w] - pts[u])
    z /= abs(z)
    return {v: pu + z * (x - pts[u]) for v, x in pts.items()}


def solve(
    n: int,
    lengths: dict[Edge, float],
    draft: list[tuple[int, int]] | None = None,
    signs: list[int] | None = None,
) -> list[tuple[float, float]]:
    """Place n points so that |p_u - p_v| = lengths[(u, v)] for every constraint.

    Precondition: the constraint graph is triangle-decomposable and the lengths are
    positive. The root of merge i is chosen by signs[i] if signs is given, else by the
    exact orientation sign of the three shared points in the integer draft (0 counts
    as +1). Raises ValueError if the graph is not decomposable or a triangle has no
    real solution. Cost: O(n^2) for the reduction plus O(n^2) for the moves.
    """
    edges = list(lengths)
    if n == 1 and not edges:
        return [(0.0, 0.0)]
    clusters, plan = reduce_clusters(n, edges)  # @line L12
    if len(clusters) != 1 or len(clusters[0]) != n:
        raise ValueError("not triangle-decomposable")
    if signs is not None and len(signs) != len(plan):
        raise ValueError("one sign per merge is needed")
    coords: dict[frozenset[int], dict[int, complex]] = {}
    for (u, v), d in lengths.items():  # @line L13
        if not d > 0.0:
            raise ValueError("lengths must be positive")
        coords[frozenset((u, v))] = {u: 0j, v: complex(d, 0.0)}
    for i, (ca, cb, cc) in enumerate(plan):  # @line L14
        (p,) = ca & cb  # @line L15
        (q,) = ca & cc
        (r,) = cb & cc
        xa, xb, xc = coords.pop(ca), coords.pop(cb), coords.pop(cc)
        if signs is not None:
            side = signs[i]
        elif draft is not None:
            side = orient(draft[p], draft[q], draft[r]) or 1  # @line L16
        else:
            side = 1
        pr = abs(xb[r] - xb[p])
        qr = abs(xc[r] - xc[q])
        rr = _third_point(xa[p], xa[q], pr, qr, side)  # @line L17
        new = dict(xa)
        for v, x in _move(xb, p, r, xa[p], rr).items():  # @line L18
            new.setdefault(v, x)
        for v, x in _move(xc, q, r, xa[q], rr).items():  # @line L19
            new.setdefault(v, x)
        coords[ca | cb | cc] = new  # @line L20
    final = coords[clusters[0]]
    return [(final[v].real, final[v].imag) for v in range(n)]  # @line L21
