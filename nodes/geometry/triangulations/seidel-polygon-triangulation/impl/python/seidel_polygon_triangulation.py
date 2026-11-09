# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seidel-polygon-triangulation/. The authors are listed in prov/FY0W28.jsonl.
"""Seidel's randomized polygon triangulation.

1. Build the trapezoidal decomposition of the polygon edges by randomized
   incremental insertion, with a history DAG for point location.
2. In every trapezoid inside the polygon whose top and bottom vertices are not
   on the same side, draw the diagonal between them; the pieces are monotone.
3. Triangulate every monotone piece with the stack algorithm.

"Above" means lexicographically larger in (y, x), which is a symbolic
rotation that removes equal y values. The vertices must be distinct and given
counterclockwise, and no three of them may be collinear.
"""
import random


def key(p):
    return (p[1], p[0])


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


class Node:
    """A DAG node. A leaf holds a trapezoid; inner nodes test a point or a segment."""

    __slots__ = ("kind", "val", "a", "b", "trap")

    def __init__(self, trap):
        self.kind = "leaf"
        self.trap = trap      # (top, bot, left, right): vertex, vertex, edge, edge
        self.val = self.a = self.b = None

    def make_y(self, r, above, below):
        self.kind, self.val, self.a, self.b, self.trap = "y", r, above, below, None

    def make_s(self, s, left, right):
        self.kind, self.val, self.a, self.b, self.trap = "s", s, left, right, None


class Trapezoidation:
    def __init__(self, pts):
        self.p = pts
        n = len(pts)
        self.seg = []
        for i in range(n):
            u, v = i, (i + 1) % n
            hi, lo = (u, v) if key(pts[u]) > key(pts[v]) else (v, u)
            self.seg.append((hi, lo))
        self.root = Node((None, None, None, None))
        self.present = set()

    def above(self, i, j):
        return key(self.p[i]) > key(self.p[j])

    def left_of(self, s, i):
        hi, lo = self.seg[s]
        return orient(self.p[lo], self.p[hi], self.p[i]) > 0

    def locate(self, i):
        node = self.root
        while node.kind != "leaf":  # @line L4
            if node.kind == "y":
                node = node.a if self.above(i, node.val) else node.b
            else:
                node = node.a if self.left_of(node.val, i) else node.b
        return node

    def inside_span(self, s, i):
        hi, lo = self.seg[s]
        return self.above(hi, i) and self.above(i, lo)

    def new_is_left(self, s, t):
        """Is the new segment s left of the old segment t, where their spans overlap?"""
        shi, slo = self.seg[s]
        thi, tlo = self.seg[t]
        for q in (slo, shi):
            if q not in (thi, tlo) and self.inside_span(t, q):
                return self.left_of(t, q)
        for q in (tlo, thi):
            if q not in (shi, slo) and self.inside_span(s, q):
                return not self.left_of(s, q)
        raise ValueError("overlapping segments")

    def crossed(self, s):
        """All leaves whose trapezoid meets the open segment s."""
        hi, lo = self.seg[s]
        out, seen, stack = [], set(), [self.root]
        while stack:
            node = stack.pop()
            if id(node) in seen:
                continue
            seen.add(id(node))
            if node.kind == "leaf":
                out.append(node)
            elif node.kind == "y":
                r = node.val
                if not self.above(hi, r):
                    stack.append(node.b)
                elif not self.above(r, lo):
                    stack.append(node.a)
                else:
                    stack.append(node.a)
                    stack.append(node.b)
            else:
                stack.append(node.a if self.new_is_left(s, node.val) else node.b)
        return out

    def add_point(self, i):
        if i in self.present:
            return
        self.present.add(i)
        leaf = self.locate(i)
        top, bot, left, right = leaf.trap
        leaf.make_y(i, Node((top, i, left, right)), Node((i, bot, left, right)))  # @line L5

    def insert(self, s):
        hi, lo = self.seg[s]
        self.add_point(hi)  # @line L3
        self.add_point(lo)
        leaves = self.crossed(s)  # @line L6
        leaves.sort(key=lambda nd: key(self.p[nd.trap[0]]), reverse=True)
        left_piece = right_piece = None
        for k, leaf in enumerate(leaves):
            top, bot, left, right = leaf.trap
            if k > 0 and self.left_of(s, top):
                right_piece.trap = (right_piece.trap[0], bot, s, right)  # @line L8
            else:
                right_piece = Node((top, bot, s, right))  # @line L7
            if k > 0 and not self.left_of(s, top):
                left_piece.trap = (left_piece.trap[0], bot, left, s)  # @line L8
            else:
                left_piece = Node((top, bot, left, s))  # @line L7
            leaf.make_s(s, left_piece, right_piece)  # @line L9

    def trapezoids(self):
        out, seen, stack = [], set(), [self.root]
        while stack:
            node = stack.pop()
            if id(node) in seen:
                continue
            seen.add(id(node))
            if node.kind == "leaf":
                out.append(node.trap)
            else:
                stack.append(node.a)
                stack.append(node.b)
        return out


def trapezoidal_decomposition(pts, rng=None):
    """The trapezoids (top, bot, left, right) of the polygon, inside ones only."""
    rng = rng or random.Random(0)
    tz = Trapezoidation(pts)
    order = list(range(len(pts)))
    rng.shuffle(order)  # @line L1
    for s in order:  # @line L2
        tz.insert(s)
    inside = []
    for top, bot, left, right in tz.trapezoids():
        if left is not None and tz.seg[left][0] == left:  # @line L10
            inside.append((top, bot, left, right))
    return tz, inside


def monotone_diagonals(tz, inside):
    """One diagonal per inside trapezoid whose top and bottom are on different sides."""
    diags = set()
    for top, bot, left, right in inside:
        if {top, bot} <= set(tz.seg[left]) or {top, bot} <= set(tz.seg[right]):  # @line L11
            continue
        diags.add((min(top, bot), max(top, bot)))  # @line L12
    return diags


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
        items = []
        for v in lst:
            dx, dy = pts[v][0] - ux, pts[v][1] - uy
            items.append((v, _half(dx, dy), dx, dy))
        # insertion sort by angle with an exact comparator
        ordered = []
        for it in items:
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
    seen = set()
    out = []
    for u in nbr:
        for v in nbr[u]:
            if (u, v) in seen:
                continue
            cyc = []
            a, b = u, v
            while (a, b) not in seen:
                seen.add((a, b))
                cyc.append(a)
                ring = nbr[b]
                c = ring[(rank[(b, a)] - 1) % len(ring)]
                a, b = b, c
            area2 = sum(orient(pts[cyc[0]], pts[cyc[i]], pts[cyc[i + 1]]) for i in range(1, len(cyc) - 1))
            if area2 > 0:
                out.append(cyc)
    return out


def triangulate_monotone(pts, poly):
    """Stack triangulation of a CCW polygon that is monotone in (y, x) order."""
    m = len(poly)
    if m == 3:
        return [tuple(poly)]
    t = max(range(m), key=lambda i: key(pts[poly[i]]))
    b = min(range(m), key=lambda i: key(pts[poly[i]]))
    side = {}
    i = (t + 1) % m
    while i != b:
        side[poly[i]] = 0          # left chain, walked downward
        i = (i + 1) % m
    i = (b + 1) % m
    while i != t:
        side[poly[i]] = 1          # right chain, walked upward
        i = (i + 1) % m
    side[poly[t]] = side[poly[b]] = 2
    order = sorted(poly, key=lambda v: key(pts[v]), reverse=True)  # @line L13
    tris = []

    def emit(a, c, d):
        if orient(pts[a], pts[c], pts[d]) < 0:
            c, d = d, c
        tris.append((a, c, d))

    stack = [order[0], order[1]]
    for j in range(2, m - 1):
        u = order[j]
        if side[u] != side[stack[-1]]:  # @line L14
            while len(stack) > 1:
                v = stack.pop()
                emit(u, v, stack[-1])
            stack = [order[j - 1], u]
        else:
            last = stack.pop()  # @line L15
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
    while len(stack) > 1:  # @line L16
        v = stack.pop()
        emit(u, v, stack[-1])
    return tris


def seidel_triangulation(pts, seed=0):
    """Triangles (i, j, k), counterclockwise, of the CCW simple polygon pts."""
    n = len(pts)
    if n < 3:
        raise ValueError("a polygon needs at least 3 vertices")
    tz, inside = trapezoidal_decomposition(pts, random.Random(seed))
    diags = monotone_diagonals(tz, inside)
    edges = [(i, (i + 1) % n) for i in range(n)] + sorted(diags)
    tris = []
    for piece in faces(pts, edges):
        tris.extend(triangulate_monotone(pts, piece))  # @line L17
    return tris
