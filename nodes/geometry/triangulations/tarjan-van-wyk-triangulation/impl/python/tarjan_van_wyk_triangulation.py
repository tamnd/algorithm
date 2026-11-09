# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-van-wyk-triangulation/. The authors are listed in prov/GNAQSY.jsonl.
"""Polygon triangulation through the horizontal visibility map.

Tarjan and Van Wyk compute the visibility map of a simple polygon in
O(n log log n) time and then triangulate in linear time. This module keeps
the same pipeline but computes the visibility map with a plain sweep:

1. Sweep the vertices from top to bottom with the edges that cross the sweep
   line in left-to-right order. At each vertex record the nearest edge to the
   left and to the right, for each horizontal ray that starts into the interior.
2. Read the inside trapezoids off the map: along every edge directed downward,
   consecutive chord end points bound one trapezoid.
3. Join the top and bottom vertex of every trapezoid when they are not
   adjacent; the pieces are monotone and are triangulated with a stack.

"Above" is lexicographic in (y, x). The vertices must be distinct and given
counterclockwise, and no three of them may be collinear.
"""


def key(p):
    return (p[1], p[0])


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


class Edges:
    """Edge i joins vertex i and vertex i + 1; seg[i] = (upper end, lower end)."""

    def __init__(self, pts):
        self.p = pts
        n = len(pts)
        self.n = n
        self.seg = []
        for i in range(n):
            u, v = i, (i + 1) % n
            self.seg.append((u, v) if key(pts[u]) > key(pts[v]) else (v, u))

    def above(self, i, j):
        return key(self.p[i]) > key(self.p[j])

    def left_of(self, s, q):
        """Is vertex q left of the upward line of edge s?"""
        hi, lo = self.seg[s]
        return orient(self.p[lo], self.p[hi], self.p[q]) > 0

    def spans(self, s, q):
        hi, lo = self.seg[s]
        return self.above(hi, q) and self.above(q, lo)

    def downward(self, s):
        return self.seg[s][0] == s

    def chord_sides(self, v):
        """Which horizontal rays from v start into the interior: (left, right)."""
        n = self.n
        u, w = (v - 1) % n, (v + 1) % n
        ua, wa = self.above(u, v), self.above(w, v)
        if ua and not wa:
            return False, True        # boundary goes down through v, interior east
        if wa and not ua:
            return True, False        # boundary goes up through v, interior west
        reflex = orient(self.p[u], self.p[v], self.p[w]) < 0
        return reflex, reflex         # split or merge: both; start or end: none


def sweep_visibility(pts):
    """hit[v] = (edge hit by the left chord or None, edge hit by the right chord or None)."""
    E = Edges(pts)
    n = len(pts)
    starting = {v: [] for v in range(n)}
    for s in range(n):
        starting[E.seg[s][0]].append(s)
    order = sorted(range(n), key=lambda v: key(pts[v]), reverse=True)  # @line L1
    active = []
    hit = [(None, None)] * n
    for v in order:  # @line L2
        active = [s for s in active if E.seg[s][1] != v]  # @line L3
        lo, hi = 0, len(active)
        while lo < hi:  # @line L4
            mid = (lo + hi) // 2
            if E.left_of(active[mid], v):
                hi = mid
            else:
                lo = mid + 1
        want_l, want_r = E.chord_sides(v)
        left = active[lo - 1] if want_l and lo > 0 else None  # @line L5
        right = active[lo] if want_r and lo < len(active) else None
        hit[v] = (left, right)
        new = starting[v]
        if len(new) == 2:
            a, b = new
            if not E.left_of(b, E.seg[a][1]):
                a, b = b, a
            new = [a, b]
        active[lo:lo] = new  # @line L6
    return E, hit


def trapezoids(E, hit):
    """Inside trapezoids as (top, bottom, left edge, right edge)."""
    n = E.n
    on_edge = {s: [] for s in range(n)}
    for v in range(n):
        left, right = hit[v]
        if left is not None:
            on_edge[left].append(v)
        if right is not None:
            on_edge[right].append(v)

    def runs(s):
        hi, lo = E.seg[s]
        pts = sorted(on_edge[s], key=lambda v: key(E.p[v]), reverse=True)
        chain = [hi] + pts + [lo]  # @line L7
        return [(chain[k], chain[k + 1]) for k in range(len(chain) - 1)]

    left_side, right_side = {}, {}
    for s in range(n):
        side = left_side if E.downward(s) else right_side
        for tb in runs(s):
            if tb in side:
                raise ValueError("two trapezoids with the same top and bottom")
            side[tb] = s
    if set(left_side) != set(right_side):
        raise ValueError("left and right walls do not match")
    return [(t, b, left_side[(t, b)], right_side[(t, b)]) for (t, b) in left_side]  # @line L8


def diagonals(E, traps):
    n = E.n
    out = set()
    for t, b, _, _ in traps:
        if (t - b) % n in (1, n - 1):
            continue
        out.add((min(t, b), max(t, b)))  # @line L9
    return out


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


def triangulate_monotone(pts, poly):
    """Stack triangulation of a CCW polygon that is monotone in (y, x) order."""
    m = len(poly)
    if m == 3:
        return [tuple(poly)]
    t = max(range(m), key=lambda i: key(pts[poly[i]]))
    b = min(range(m), key=lambda i: key(pts[poly[i]]))
    side = {poly[t]: 2, poly[b]: 2}
    i = (t + 1) % m
    while i != b:
        side[poly[i]] = 0
        i = (i + 1) % m
    i = (b + 1) % m
    while i != t:
        side[poly[i]] = 1
        i = (i + 1) % m
    order = sorted(poly, key=lambda v: key(pts[v]), reverse=True)  # @line L10
    tris = []

    def emit(a, c, d):
        if orient(pts[a], pts[c], pts[d]) < 0:
            c, d = d, c
        tris.append((a, c, d))

    stack = [order[0], order[1]]
    for j in range(2, m - 1):
        u = order[j]
        if side[u] != side[stack[-1]]:  # @line L11
            while len(stack) > 1:
                v = stack.pop()
                emit(u, v, stack[-1])
            stack = [order[j - 1], u]
        else:
            last = stack.pop()  # @line L12
            while stack:
                o = orient(pts[stack[-1]], pts[last], pts[u])
                if (o > 0) if side[u] == 0 else (o < 0):
                    emit(u, last, stack[-1])
                    last = stack.pop()
                else:
                    break
            stack.append(last)
            stack.append(u)
    u = order[m - 1]
    while len(stack) > 1:  # @line L13
        v = stack.pop()
        emit(u, v, stack[-1])
    return tris


def triangulate(pts):
    """Triangles (i, j, k), counterclockwise, of the CCW simple polygon pts."""
    n = len(pts)
    if n < 3:
        raise ValueError("a polygon needs at least 3 vertices")
    E, hit = sweep_visibility(pts)
    diags = diagonals(E, trapezoids(E, hit))
    tris = []
    for piece in faces(pts, [(i, (i + 1) % n) for i in range(n)] + sorted(diags)):
        tris.extend(triangulate_monotone(pts, piece))  # @line L14
    return tris
