# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-triangulation/. The authors are listed in prov/RBTAEV.jsonl.

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of pqr: positive for a left turn. Exact for int and Fraction."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_open_segment(p: Point, q: Point, r: Point) -> bool:
    """True if r lies strictly between p and q on the segment pq."""
    if r == p or r == q or orient(p, q, r) != 0:
        return False
    return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])


def crosses(a: Point, b: Point, c: Point, d: Point) -> bool:
    """True if the open segments ab and cd meet. The segments share no end point, and no
    input point lies inside either one, so meeting means a proper crossing."""
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def sq_len(p: Point, q: Point):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def greedy_triangulation(points: list[Point]) -> list[tuple[int, int]]:
    """Return the edges (i, j), i < j, of the greedy triangulation in the order they were added.
    Ties in length are broken by the index pair, so the result is unique."""
    n = len(points)
    if len(set(points)) != n:
        raise ValueError("points must be distinct")
    cand = []
    for i in range(n):  # @line L1
        for j in range(i + 1, n):
            if not any(on_open_segment(points[i], points[j], points[k]) for k in range(n)):
                cand.append((sq_len(points[i], points[j]), i, j))
    cand.sort()  # @line L2
    edges: list[tuple[int, int]] = []  # @line L3
    for _, i, j in cand:  # @line L4
        a, b = points[i], points[j]
        ok = True
        for (k, l) in edges:  # @line L5
            if k in (i, j) or l in (i, j):
                continue
            if crosses(a, b, points[k], points[l]):
                ok = False
                break
        if ok:
            edges.append((i, j))  # @line L6
    return edges  # @line L7


def triangles(points: list[Point], edges: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    """The bounded faces of a triangulation given by its edges, as counterclockwise triples."""
    adj: dict[int, set[int]] = {i: set() for i in range(len(points))}
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    out = []
    for i, j in edges:
        for k in adj[i] & adj[j]:
            if k < j:
                continue
            a, b, c = (i, j, k) if orient(points[i], points[j], points[k]) > 0 else (j, i, k)
            if orient(points[a], points[b], points[c]) == 0:
                continue
            empty = True
            for m in range(len(points)):
                if m in (a, b, c):
                    continue
                p = points[m]
                if orient(points[a], points[b], p) >= 0 and orient(points[b], points[c], p) >= 0 \
                        and orient(points[c], points[a], p) >= 0:
                    empty = False
                    break
            if empty:
                out.append((a, b, c))
    return out
