# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-polygon-triangulation/. The authors are listed in prov/HPKK4H.jsonl.
"""The last stage of Chazelle's triangulation: from the visibility map to triangles.

Chazelle computes the horizontal visibility map of a simple polygon in linear
time; that part is far too intricate for a reference implementation. Here the
map is computed by brute force, one ray at a time, and the rest follows the
linear-time conversion that Chazelle's algorithm ends with:

1. Read the inside trapezoids off the map.
2. Join the top and bottom vertex of every trapezoid when they are not
   adjacent. Every piece is then a monotone mountain: a monotone polygon one
   of whose chains is a single edge.
3. Triangulate every mountain by cutting off convex chain vertices.

"Above" is lexicographic in (y, x). The vertices must be distinct and given
counterclockwise, and no three of them may be collinear.
"""


def key(p):
    return (p[1], p[0])


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


class Polygon:
    """Edge i joins vertex i and vertex i + 1; seg[i] = (upper end, lower end)."""

    def __init__(self, pts):
        self.p = pts
        self.n = n = len(pts)
        self.seg = []
        for i in range(n):
            u, v = i, (i + 1) % n
            self.seg.append((u, v) if key(pts[u]) > key(pts[v]) else (v, u))

    def above(self, i, j):
        return key(self.p[i]) > key(self.p[j])

    def left_of(self, s, q):
        hi, lo = self.seg[s]
        return orient(self.p[lo], self.p[hi], self.p[q]) > 0

    def spans(self, s, q):
        hi, lo = self.seg[s]
        return self.above(hi, q) and self.above(q, lo)

    def is_left(self, a, b):
        """Edges a and b span a common height and do not cross: is a left of b there?"""
        for q in self.seg[a]:
            if q not in self.seg[b] and self.spans(b, q):
                return self.left_of(b, q)
        for q in self.seg[b]:
            if q not in self.seg[a] and self.spans(a, q):
                return not self.left_of(a, q)
        raise ValueError("overlapping edges")


def visibility_map(P):
    """hit[v] = (edge hit by the left chord or None, edge hit by the right chord or None)."""
    n = P.n
    hit = []
    for v in range(n):  # @line L1
        u, w = (v - 1) % n, (v + 1) % n
        ua, wa = P.above(u, v), P.above(w, v)
        if ua != wa:
            want_l, want_r = wa, ua  # @line L2
        else:
            reflex = orient(P.p[u], P.p[v], P.p[w]) < 0
            want_l = want_r = reflex
        best_l = best_r = None
        for s in range(n):
            if not P.spans(s, v):
                continue
            if P.left_of(s, v):                 # s is right of v
                if want_r and (best_r is None or P.is_left(s, best_r)):
                    best_r = s  # @line L3
            elif want_l and (best_l is None or P.is_left(best_l, s)):
                best_l = s
        hit.append((best_l, best_r))
    return hit


def trapezoids(P, hit):
    """Inside trapezoids as (top, bottom, left edge, right edge)."""
    n = P.n
    ends = {s: [] for s in range(n)}
    for v, (l, r) in enumerate(hit):
        if l is not None:
            ends[l].append(v)
        if r is not None:
            ends[r].append(v)
    walls = ({}, {})
    for s in range(n):
        hi, lo = P.seg[s]
        chain = [hi] + sorted(ends[s], key=lambda v: key(P.p[v]), reverse=True) + [lo]
        side = walls[0] if hi == s else walls[1]   # downward edges are left walls
        for k in range(len(chain) - 1):
            side[(chain[k], chain[k + 1])] = s  # @line L4
    if set(walls[0]) != set(walls[1]):
        raise ValueError("left and right walls do not match")
    return [(t, b, walls[0][(t, b)], walls[1][(t, b)]) for (t, b) in walls[0]]


def diagonals(P, traps):
    n = P.n
    return {(min(t, b), max(t, b)) for t, b, _, _ in traps if (t - b) % n not in (1, n - 1)}  # @line L5


def _half(dx, dy):
    return 0 if dy > 0 or (dy == 0 and dx > 0) else 1


def faces(pts, edges):
    """Inner faces of a plane graph that subdivides a CCW polygon, as CCW vertex lists."""
    nbr = {i: [] for i in range(len(pts))}
    for u, v in edges:
        nbr[u].append(v)
        nbr[v].append(u)
    rank = {}
    for u, lst in nbr.items():
        ux, uy = pts[u]
        ordered = []
        for v in lst:
            dx, dy = pts[v][0] - ux, pts[v][1] - uy
            it = (v, _half(dx, dy), dx, dy)
            k = len(ordered)
            while k > 0:
                o = ordered[k - 1]
                if o[1] < it[1] or (o[1] == it[1] and o[2] * it[3] - o[3] * it[2] > 0):
                    break
                k -= 1
            ordered.insert(k, it)
        nbr[u] = [it[0] for it in ordered]
        for idx, it in enumerate(ordered):
            rank[(u, it[0])] = idx
    seen, out = set(), []
    for u in nbr:
        for v in nbr[u]:
            if (u, v) in seen:
                continue
            cyc, a, b = [], u, v
            while (a, b) not in seen:
                seen.add((a, b))
                cyc.append(a)
                ring = nbr[b]
                a, b = b, ring[(rank[(b, a)] - 1) % len(ring)]
            if sum(orient(pts[cyc[0]], pts[cyc[i]], pts[cyc[i + 1]]) for i in range(1, len(cyc) - 1)) > 0:
                out.append(cyc)
    return out


def mountain_chain(pts, poly):
    """The chain of a monotone mountain from top to bottom, and +1 if it runs counterclockwise."""
    m = len(poly)
    t = max(range(m), key=lambda i: key(pts[poly[i]]))
    b = min(range(m), key=lambda i: key(pts[poly[i]]))
    if (b - t) % m == 1:                     # base t -> b, the chain runs b -> ... -> t
        chain = [poly[(t - k) % m] for k in range(m)]
        return chain, -1
    if (t - b) % m == 1:                     # base b -> t, the chain runs t -> ... -> b
        chain = [poly[(t + k) % m] for k in range(m)]
        return chain, 1
    raise ValueError("not a monotone mountain")


def triangulate_mountain(pts, poly):
    chain, sign = mountain_chain(pts, poly)  # @line L6
    tris, stack = [], []
    for u in chain:
        stack.append(u)  # @line L7
        while len(stack) >= 3 and sign * orient(pts[stack[-3]], pts[stack[-2]], pts[stack[-1]]) > 0:
            a, c, d = stack[-3], stack[-2], stack[-1]
            tris.append((a, c, d) if sign > 0 else (a, d, c))  # @line L8
            del stack[-2]
    if len(stack) != 2:
        raise ValueError("not a monotone mountain")
    return tris


def triangulate(pts):
    """Triangles (i, j, k), counterclockwise, of the CCW simple polygon pts."""
    n = len(pts)
    if n < 3:
        raise ValueError("a polygon needs at least 3 vertices")
    P = Polygon(pts)
    diags = diagonals(P, trapezoids(P, visibility_map(P)))
    tris = []
    for piece in faces(pts, [(i, (i + 1) % n) for i in range(n)] + sorted(diags)):
        tris.extend(triangulate_mountain(pts, piece))  # @line L9
    return tris
