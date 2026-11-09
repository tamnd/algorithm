# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lawson-flip-algorithm/. The authors are listed in prov/024GPG.jsonl.

Point = tuple[int, int]
Triangle = tuple[int, int, int]
GHOST = -1


def orient(a: Point, b: Point, c: Point) -> int:
    """Sign of (b - a) x (c - a): 1 for a left turn, -1 for a right turn, 0 when collinear."""
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (d > 0) - (d < 0)


def incircle(a: Point, b: Point, c: Point, d: Point) -> int:
    """For a, b, c counterclockwise: 1 if d is strictly inside their circumcircle, 0 on it, -1 outside."""
    adx, ady = a[0] - d[0], a[1] - d[1]
    bdx, bdy = b[0] - d[0], b[1] - d[1]
    cdx, cdy = c[0] - d[0], c[1] - d[1]
    det = ((adx * adx + ady * ady) * (bdx * cdy - cdx * bdy)
           + (bdx * bdx + bdy * bdy) * (cdx * ady - adx * cdy)
           + (cdx * cdx + cdy * cdy) * (adx * bdy - bdx * ady))
    return (det > 0) - (det < 0)


def sweep_triangulation(pts: list[Point]) -> list[Triangle]:
    """Some triangulation of the distinct points pts (all of them vertices), by a sweep in (x, y) order.

    Returns counterclockwise index triples into pts, or [] when the points are collinear.
    Each new point is the lexicographic maximum so far, so it is outside the current hull; it is joined to
    every hull edge it sees strictly. The walk along the hull is amortized O(1), so the cost is O(n log n).
    """
    order = sorted(range(len(pts)), key=lambda i: pts[i])
    first = next((k for k in range(2, len(order)) if orient(pts[order[0]], pts[order[1]], pts[order[k]]) != 0), None)
    if first is None:
        return []
    tri: dict[int, Triangle] = {}
    edge: dict[tuple[int, int], int] = {}
    counter = [0]

    def add(t: Triangle) -> None:
        u, v, w = t
        if u == GHOST:
            u, v, w = v, w, u
        elif v == GHOST:
            u, v, w = w, u, v
        tri[counter[0]] = (u, v, w)
        edge[(u, v)] = edge[(v, w)] = edge[(w, u)] = counter[0]
        counter[0] += 1

    apex = order[first]
    chain = order[:first]  # collinear and sorted along their line
    up = orient(pts[chain[0]], pts[chain[1]], pts[apex]) > 0
    for a, b in zip(chain, chain[1:]):
        add((a, b, apex) if up else (b, a, apex))
        add((b, a, GHOST) if up else (a, b, GHOST))
    ends = (chain[-1], apex, chain[0]) if up else (chain[0], apex, chain[-1])
    add((ends[1], ends[0], GHOST))
    add((ends[2], ends[1], GHOST))
    last = apex
    for i in order[first + 1:]:
        p = pts[i]
        start = next(edge[e] for e in ((last, GHOST), (GHOST, last))
                     if orient(pts[tri[edge[e]][0]], pts[tri[edge[e]][1]], p) > 0)
        seen = {start}
        stack = [start]
        while stack:
            u, v, _ = tri[stack.pop()]
            for e in ((GHOST, v), (u, GHOST)):
                nb = edge[e]
                a, b, _ = tri[nb]
                if nb not in seen and orient(pts[a], pts[b], p) > 0:
                    seen.add(nb)
                    stack.append(nb)
        bound = []
        for tid in seen:
            u, v, w = tri[tid]
            for x, y in ((u, v), (v, w), (w, u)):
                if edge[(y, x)] not in seen:
                    bound.append((x, y))
        for tid in seen:
            u, v, w = tri.pop(tid)
            del edge[(u, v)], edge[(v, w)], edge[(w, u)]
        for x, y in bound:
            add((x, y, i))
        last = i
    return [t for t in tri.values() if t[2] != GHOST]


def lawson_flip(points: list[Point]) -> list[tuple[Point, Point, Point]]:
    """Return a Delaunay triangulation of the points by Lawson's edge flips, as counterclockwise triples.

    Duplicates are removed; collinear input gives []. The start is the sweep triangulation; then every
    interior edge that is not locally Delaunay is flipped, until none is left. With cocircular points the
    result is one of the Delaunay triangulations. Coordinates must be int or Fraction.
    Cost: O(n log n) for the start and at most n(n - 1)/2 flips, each O(1) (expected, as the edges are kept in a
    dict), so O(n^2) time in the worst case; O(n) space.
    """
    pts = list(dict.fromkeys(points))
    tris = sweep_triangulation(pts)  # @line L1
    edge: dict[tuple[int, int], Triangle] = {}
    for t in tris:
        a, b, c = t
        edge[(a, b)] = edge[(b, c)] = edge[(c, a)] = t
    stack = [e for e in edge if e[0] < e[1] and (e[1], e[0]) in edge]  # @line L2
    queued = set(stack)  # each undirected edge is on the stack at most once, so the stack has O(n) size
    while stack:  # @line L3
        a, b = stack.pop()  # @line L4
        queued.discard((a, b))
        if (a, b) not in edge or (b, a) not in edge:
            continue  # the edge was flipped away
        t1, t2 = edge[(a, b)], edge[(b, a)]
        c = next(v for v in t1 if v not in (a, b))
        d = next(v for v in t2 if v not in (a, b))
        if incircle(pts[a], pts[b], pts[c], pts[d]) > 0:  # @line L5
            for t in (t1, t2):  # @line L6
                x, y, z = t
                del edge[(x, y)], edge[(y, z)], edge[(z, x)]
            for t in ((a, d, c), (d, b, c)):
                x, y, z = t
                edge[(x, y)] = edge[(y, z)] = edge[(z, x)] = t
            for u, v in ((a, d), (d, b), (b, c), (c, a)):  # @line L7
                key = (u, v) if u < v else (v, u)
                if key not in queued:
                    queued.add(key)
                    stack.append(key)
    out = {edge[e] for e in edge}
    return sorted((pts[a], pts[b], pts[c]) for a, b, c in out)  # @line L8
