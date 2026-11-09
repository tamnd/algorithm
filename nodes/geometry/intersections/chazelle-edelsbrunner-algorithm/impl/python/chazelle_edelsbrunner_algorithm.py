# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-edelsbrunner-algorithm/. The authors are listed in prov/VR6X2D.jsonl.
"""Report all intersecting pairs of n closed segments with a slab tree of staircases.

This is NOT the Chazelle-Edelsbrunner algorithm, whose data structures are far
longer. It is a compact exact relative of the optimal methods, close to the
simple O(n log^2 n + k) tree search of Balaban: the x-axis is cut into slabs at
the end points, a segment tree holds each segment at its canonical slabs, and in
every slab the long segments are peeled into staircases, sets of segments that
do not meet inside the slab and so are sorted everywhere in it. A segment that is
not a stair meets a stair, so the work spent on it is paid for by a reported pair.

All arithmetic is exact (int or Fraction). Degenerate inputs are allowed: shared
end points, collinear overlaps, vertical segments and segments of length zero.
"""

from fractions import Fraction


class Stats:
    def __init__(self):
        self.reports = 0  # reported pairs, with repetition
        self.work = 0  # segments handled by merges, splits and searches


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on(p, a, b):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_meet(a, b, c, d):
    """Do the closed segments ab and cd share a point? (a = b or c = d allowed)"""
    d1, d2, d3, d4 = orient(c, d, a), orient(c, d, b), orient(a, b, c), orient(a, b, d)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return ((d1 == 0 and _on(a, c, d)) or (d2 == 0 and _on(b, c, d))
            or (d3 == 0 and _on(c, a, b)) or (d4 == 0 and _on(d, a, b)))


class _Tree:
    def __init__(self, segs, stats):
        self.s, self.stats, self.found = segs, stats, set()
        self.X = sorted({p[0] for s in segs for p in s})
        self.idx = {x: i for i, x in enumerate(self.X)}
        self.long, self.inner = {}, {}

    # geometry of a sheared, left-to-right segment
    def y(self, i, x):
        (x1, y1), (x2, y2) = self.s[i]
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    def key(self, i, x):
        (x1, y1), (x2, y2) = self.s[i]
        return (self.y(i, x), (y2 - y1) / (x2 - x1), i)

    def clip(self, i, xb, xe):
        (x1, y1), (x2, y2) = self.s[i]
        if x1 == x2:
            return self.s[i]
        c, d = max(x1, xb), min(x2, xe)
        return (c, self.y(i, c)), (d, self.y(i, d))

    def report(self, i, j):
        self.stats.reports += 1
        self.found.add((min(i, j), max(i, j)))

    def merge(self, a, b, x):
        self.stats.work += len(a) + len(b)
        out, i, j = [], 0, 0
        while i < len(a) and j < len(b):
            if self.key(a[i], x) <= self.key(b[j], x):
                out.append(a[i]); i += 1
            else:
                out.append(b[j]); j += 1
        return out + a[i:] + b[j:]

    # the slab tree: node (lo, hi) is the strip [X[lo], X[hi]]
    def place(self, i, lo, hi):
        a, b = self.idx[self.s[i][0][0]], self.idx[self.s[i][1][0]]
        if a == b:  # a point: inner on the half-open strips [X[lo], X[hi]) that hold it
            while lo <= a < hi:
                self.inner.setdefault((lo, hi), []).append(i)
                if hi - lo == 1:
                    break
                mid = (lo + hi) // 2
                lo, hi = (lo, mid) if a < mid else (mid, hi)
            return
        stack = [(lo, hi)]
        while stack:
            lo, hi = stack.pop()
            if a <= lo and hi <= b:
                self.long.setdefault((lo, hi), []).append(i)
            elif max(lo, a) < min(hi, b):
                self.inner.setdefault((lo, hi), []).append(i)
                mid = (lo + hi) // 2
                stack += [(lo, mid), (mid, hi)]

    def split(self, L, xb, xe):
        Q, rest, pos = [], [], []
        for s in L:
            self.stats.work += 1
            if not Q or not segments_meet(*self.clip(Q[-1], xb, xe), *self.clip(s, xb, xe)):
                Q.append(s)
            else:
                rest.append(s)
                pos.append(len(Q))
        return Q, rest, pos

    def walk(self, Q, p, t, piece, xb, xe):
        """Report the stairs that meet piece, a part of t inside the strip, from position p."""
        for rng in (range(p, len(Q)), range(p - 1, -1, -1)):
            for k in rng:
                if not segments_meet(*self.clip(Q[k], xb, xe), *piece):
                    break
                self.report(Q[k], t)

    def strip(self, L, xb, xe):
        levels = []
        while len(L) > 1:  # @line L12
            Q, rest, pos = self.split(L, xb, xe)  # @line L13
            for s, p in zip(rest, pos):
                self.walk(Q, p, s, self.clip(s, xb, xe), xb, xe)
            levels.append(Q)
            L = rest
        for Q in reversed(levels):  # @line L14
            L = self.merge(Q, L, xe)
        return L

    def search(self, lo, hi, P):
        xb, xe = self.X[lo], self.X[hi]
        L = self.merge(P, self.long.get((lo, hi), []), xb)  # @line L5
        Q, rest, pos = self.split(L, xb, xe)  # @line L6
        for s, p in zip(rest, pos):  # @line L7
            self.walk(Q, p, s, self.clip(s, xb, xe), xb, xe)
        for t in self.inner.get((lo, hi), []):  # @line L8
            piece = self.clip(t, xb, xe)
            c, yc = piece[0]
            a, b = 0, len(Q)
            while a < b:
                self.stats.work += 1
                m = (a + b) // 2
                if self.y(Q[m], c) < yc:
                    a = m + 1
                else:
                    b = m
            self.walk(Q, a, t, piece, xb, xe)
        if hi - lo == 1:  # @line L9
            for z in self.inner.get((lo, hi), []):
                zy = self.s[z][0][1]
                a, b = 0, len(L)
                while a < b:
                    self.stats.work += 1
                    m = (a + b) // 2
                    if self.y(L[m], xb) < zy:
                        a = m + 1
                    else:
                        b = m
                while a < len(L) and self.y(L[a], xb) == zy:
                    self.report(L[a], z)
                    a += 1
            R = self.strip(rest, xb, xe)
        else:  # @line L10
            mid = (lo + hi) // 2
            R = self.search(mid, hi, self.search(lo, mid, rest))
        keep = set(P)  # @line L11
        return [s for s in self.merge(Q, R, xe) if s in keep]


def intersecting_pairs(segments, stats=None):
    """All pairs (i, j), i < j, of closed segments that share at least one point."""
    stats = stats if stats is not None else Stats()
    pts = [(Fraction(x), Fraction(y)) for s in segments for (x, y) in s]
    if not pts:
        return []
    xs = sorted({p[0] for p in pts})  # @line L1
    lam = 0
    if len(xs) < len(set(pts)):  # two end points share an x: shear by a small slope
        gap = min((b - a for a, b in zip(xs, xs[1:])), default=Fraction(1))
        lam = gap / (2 * max(abs(p[1]) for p in pts) + 1)
    sheared = []
    for k in range(len(segments)):
        a, b = [(x + lam * y, y) for x, y in pts[2 * k:2 * k + 2]]
        sheared.append((a, b) if a[0] <= b[0] else (b, a))
    tree = _Tree(sheared, stats)
    ends = {}  # @line L2
    for i, (a, b) in enumerate(sheared):
        for p in {a, b}:
            ends.setdefault(p, []).append(i)
    for group in ends.values():
        for u in range(len(group)):
            for v in range(u + 1, len(group)):
                tree.report(group[u], group[v])
    m = len(tree.X) - 1  # @line L3
    if m >= 1:
        for i in range(len(sheared)):
            tree.place(i, 0, m)
        for node, lst in tree.long.items():
            lst.sort(key=lambda i: tree.key(i, tree.X[node[0]]))
        tree.search(0, m, [])  # @line L4
    return sorted(tree.found)
