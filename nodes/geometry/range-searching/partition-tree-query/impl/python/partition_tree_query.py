# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partition-tree-query/. The authors are listed in prov/T2GH1M.jsonl.

"""Simplex and polygon range queries on a partition tree (Willard 1982; Matousek 1992).

The query range is an intersection of closed halfplanes a x + b y <= c (a triangle is three of
them). partition_tree_query walks the tree with an explicit stack: a node whose cell lies outside
one halfplane is skipped, a node whose cell lies inside all of them is counted (and its block of
points reported) at once, a crossed leaf is scanned, and a crossed internal node is opened. The
cells are convex hulls stored as lower and upper chains; extreme() finds the largest value of
a x + b y over a cell by binary search on one chain.

The module is self-contained: it carries a copy of the partition tree builder (the reweighting
construction of the partition-tree page). Arithmetic is exact on ints and Fractions.

Cost: O(l log n) per visited node for l halfplanes, plus the points of the crossed leaves and the
output; with crossing number kappa at every node the number of visited nodes is
O(r (n / leaf_size)^(log(l kappa) / log(r / 2))) for r >= 4, about sqrt(n) for good partitions.
"""

import random
from bisect import bisect_left
from fractions import Fraction
from math import isqrt
from typing import Dict, List, Optional, Sequence, Tuple

Point = Tuple[object, object]
Line = Tuple[object, object, object]  # (a, b, c): the line a x + b y = c, halfplane a x + b y <= c

OUTSIDE, INSIDE, CROSSED = 0, 1, 2


def orient(p, q, t):
    """Twice the signed area of the triangle p, q, t; positive when it turns left."""
    return (q[0] - p[0]) * (t[1] - p[1]) - (q[1] - p[1]) * (t[0] - p[0])


def hull_chains(points: Sequence[Point]) -> Tuple[List[Point], List[Point]]:
    """The lower and the upper hull, both from the leftmost-lowest point to the rightmost-highest
    point, with no three consecutive vertices collinear."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts, list(pts)
    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: List[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    upper.reverse()
    return lower, upper


def convex_hull(points: Sequence[Point]) -> List[Point]:
    """Vertices of the convex hull in counterclockwise order (one or two points if degenerate)."""
    lower, upper = hull_chains(points)
    if len(lower) <= 2 and lower == upper:
        return lower
    return lower[:-1] + upper[::-1][:-1]


def extreme(cell: Tuple[List[Point], List[Point]], a, b):
    """max of a x + b y over the convex polygon given by its two chains, in O(log h) time.

    Along the upper chain (left to right) the edge directions turn clockwise, so for b > 0 the
    increments a dx + b dy are first positive and then at most zero; the maximum is at the first
    edge whose increment is at most zero. The lower chain plays this role for b < 0."""
    lower, upper = cell
    if b == 0:  # @line L9
        return max(a * lower[0][0], a * lower[-1][0])
    chain = upper if b > 0 else lower  # @line L10
    lo, hi = 0, len(chain) - 1
    while lo < hi:  # @line L11
        mid = (lo + hi) // 2
        inc = a * (chain[mid + 1][0] - chain[mid][0]) + b * (chain[mid + 1][1] - chain[mid][1])
        if inc <= 0:
            hi = mid
        else:
            lo = mid + 1
    return a * chain[lo][0] + b * chain[lo][1]  # @line L12


def line_through(p: Point, q: Point) -> Line:
    """The line through two distinct points."""
    a = q[1] - p[1]
    b = p[0] - q[0]
    return (a, b, a * p[0] + b * p[1])


def value(h: Line, p: Point):
    return h[0] * p[0] + h[1] * p[1] - h[2]


def crosses(h: Line, hull: Sequence[Point]) -> bool:
    """True if the line meets the closed convex polygon and does not contain it."""
    vals = [value(h, v) for v in hull]
    lo, hi = min(vals), max(vals)
    return lo <= 0 <= hi and not (lo == 0 and hi == 0)


def classify(cell, constraints: Sequence[Line]) -> int:
    """OUTSIDE if the cell misses the range, INSIDE if it lies in it, else CROSSED."""
    inside = True
    for a, b, c in constraints:
        if -extreme(cell, -a, -b) > c:  # even the smallest value of a x + b y exceeds c
            return OUTSIDE
        if extreme(cell, a, b) > c:
            inside = False
    return INSIDE if inside else CROSSED


def triangle_constraints(p: Point, q: Point, t: Point) -> List[Line]:
    """The three closed halfplanes whose intersection is the triangle p, q, t."""
    o = orient(p, q, t)
    if o == 0:
        raise ValueError("degenerate triangle")
    if o < 0:
        q, t = t, q
    out = []
    for u, v in ((p, q), (q, t), (t, p)):
        a = v[1] - u[1]
        b = u[0] - v[0]
        out.append((a, b, a * u[0] + b * u[1]))  # left of u -> v, or on it
    return out


def _intersection_x(g: Line, h: Line):
    det = g[0] * h[1] - h[0] * g[1]
    if det == 0:
        return None
    return Fraction(g[2] * h[1] - h[2] * g[1]) / det


def _sign(x) -> int:
    return (x > 0) - (x < 0)


def _draw(weights: List[int], t: int, rng: random.Random) -> List[int]:
    """t indices drawn with replacement, index j with probability weights[j] / sum."""
    prefix = []
    total = 0
    for w in weights:
        total += w
        prefix.append(total)
    return [bisect_left(prefix, rng.randrange(total) + 1) for _ in range(t)]


def _cells(rest: List[int], pts: Sequence[Point], lines: List[Line]) -> Dict[tuple, List[int]]:
    """Group points by their face in the arrangement of the lines and the vertical lines through
    the vertices; each group lies in one convex region that no drawn line crosses."""
    xs = set()
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            x = _intersection_x(lines[i], lines[j])
            if x is not None:
                xs.add(x)
    xs = sorted(xs)
    groups: Dict[tuple, List[int]] = {}
    for i in rest:
        p = pts[i]
        k = bisect_left(xs, p[0])
        slab = 2 * k + 1 if k < len(xs) and xs[k] == p[0] else 2 * k
        key = (slab,) + tuple(_sign(value(h, p)) for h in lines)
        groups.setdefault(key, []).append(i)
    return groups


def simplicial_partition(idx: List[int], pts: Sequence[Point], r: int, rng: random.Random,
                         tests: int = 64) -> List[List[int]]:
    """Split m >= 2 indices into q <= max(r, 2) classes: q - 1 classes of s points and the rest."""
    m = len(idx)
    s = -(-m // r)
    q = m // s  # the number of classes
    if q < 2:
        s, q = m // 2, 2
    distinct = sorted(set(pts[i] for i in idx))
    test: List[Line] = []
    d = len(distinct)
    if d >= 2:
        if d * (d - 1) // 2 <= tests:
            test = [line_through(distinct[i], distinct[j]) for i in range(d) for j in range(i + 1, d)]
        else:
            while len(test) < tests:
                i, j = rng.sample(range(d), 2)
                test.append(line_through(distinct[i], distinct[j]))
    weight = [1] * len(test)
    rest = sorted(idx, key=lambda i: (pts[i][0], pts[i][1], i))
    classes: List[List[int]] = []
    while len(classes) < q - 1:
        t = max(1, isqrt(len(rest) // s)) if test else 0
        while True:
            drawn = [test[j] for j in _draw(weight, t, rng)] if t > 0 else []
            groups = [g for g in _cells(rest, pts, drawn).values() if len(g) >= s]
            if groups:
                break
            t //= 2
        best = None
        for g in groups:
            a = g[0]
            cls = sorted(g, key=lambda i: ((pts[i][0] - pts[a][0]) ** 2 + (pts[i][1] - pts[a][1]) ** 2, i))[:s]
            hull = convex_hull([pts[i] for i in cls])
            cost = sum(w for h, w in zip(test, weight) if crosses(h, hull))
            if best is None or cost < best[0]:
                best = (cost, cls, hull)
        _, cls, hull = best
        for j, h in enumerate(test):
            if crosses(h, hull):
                weight[j] *= 2
        taken = set(cls)
        rest = [i for i in rest if i not in taken]
        classes.append(cls)
    classes.append(rest)
    return classes


class PartitionTree:
    """A static partition tree on a multiset of points in the plane."""

    def __init__(self, points: Sequence[Point] = (), r: int = 8, leaf_size: int = 4,
                 seed: int = 0, tests: int = 64) -> None:
        if r < 2 or leaf_size < 1:
            raise ValueError("need r >= 2 and leaf_size >= 1")
        self.pts = [tuple(p) for p in points]
        self.n = len(self.pts)
        self.r = r
        self.leaf_size = leaf_size
        self.perm: List[int] = [0] * self.n  # subtree of v holds perm[lo[v]:hi[v]]
        self.cell: List[Tuple[List[Point], List[Point]]] = []  # (lower chain, upper chain)
        self.lo: List[int] = []
        self.hi: List[int] = []
        self.children: List[List[int]] = []
        if self.n == 0:
            return
        rng = random.Random(seed)
        root = self._new_node(0, self.n)
        stack = [(root, list(range(self.n)))]
        while stack:
            v, idx = stack.pop()
            self.cell[v] = hull_chains([self.pts[i] for i in idx])
            if len(idx) <= leaf_size:
                self.perm[self.lo[v]:self.hi[v]] = idx
                continue
            classes = simplicial_partition(idx, self.pts, r, rng, tests)
            start = self.lo[v]
            for cls in classes:
                w = self._new_node(start, start + len(cls))
                self.children[v].append(w)
                stack.append((w, cls))
                start += len(cls)

    def _new_node(self, lo: int, hi: int) -> int:
        self.cell.append(([], []))
        self.lo.append(lo)
        self.hi.append(hi)
        self.children.append([])
        return len(self.lo) - 1

    def __len__(self) -> int:
        return self.n

    def query(self, constraints: Sequence[Line], report: bool = True,
              stats: Optional[dict] = None):
        """Count (and list, if report) the points with a x + b y <= c for every (a, b, c)."""
        return partition_tree_query(self, constraints, report, stats)

    def count(self, constraints: Sequence[Line]) -> int:
        return self.query(constraints, report=False)

    def report(self, constraints: Sequence[Line]) -> List[Point]:
        return self.query(constraints)[1]

    def triangle(self, p: Point, q: Point, t: Point) -> List[Point]:
        """The points in the closed triangle p, q, t (which must not be degenerate)."""
        return self.report(triangle_constraints(p, q, t))

    def halfplane(self, a, b, c) -> List[Point]:
        """The points with a x + b y <= c."""
        return self.report([(a, b, c)])

    def crossing_numbers(self, h: Line) -> List[int]:
        """For each internal node, how many of its children's cells the line crosses."""
        return [sum(crosses(h, self.cell[w][0] + self.cell[w][1]) for w in ch)
                for ch in self.children if ch]

    def hull_vertices(self) -> int:
        return sum(len(lower) + len(upper) for lower, upper in self.cell)

    def check_invariant(self) -> None:
        if self.n == 0:
            assert not self.lo
            return
        assert sorted(self.perm) == list(range(self.n))
        assert (self.lo[0], self.hi[0]) == (0, self.n)
        for v in range(len(self.lo)):
            ch = self.children[v]
            members = [self.pts[i] for i in self.perm[self.lo[v]:self.hi[v]]]
            assert self.cell[v] == hull_chains(members)
            if not ch:
                assert 1 <= len(members) <= self.leaf_size
                continue
            assert 2 <= len(ch) <= max(self.r, 2)
            assert self.lo[ch[0]] == self.lo[v] and self.hi[ch[-1]] == self.hi[v]
            for a, b in zip(ch, ch[1:]):
                assert self.hi[a] == self.lo[b]
            sizes = [self.hi[w] - self.lo[w] for w in ch]
            assert all(z >= 1 for z in sizes) and max(sizes) < len(members)


def partition_tree_query(tree: PartitionTree, constraints: Sequence[Line], report: bool = True,
                         stats: Optional[dict] = None):
    """The points of the tree in the closed range given by the halfplanes a x + b y <= c.

    Returns (count, points) if report, else count. stats, if given, receives the number of
    visited nodes, of nodes found inside and outside, and of points scanned at leaves."""
    count = 0
    out: List[Point] = []
    stack = [0] if tree.n else []  # @line L1
    visits = inside = outside = scanned = 0
    while stack:  # @line L2
        v = stack.pop()
        visits += 1
        cell = tree.cell[v]
        bounds = [(-extreme(cell, -a, -b), extreme(cell, a, b), c)  # @line L3
                  for a, b, c in constraints]
        if any(lo > c for lo, _, c in bounds):  # @line L4
            outside += 1
            continue
        lo_v, hi_v = tree.lo[v], tree.hi[v]
        if all(hi <= c for _, hi, c in bounds):  # @line L5
            inside += 1
            count += hi_v - lo_v
            if report:
                out.extend(tree.pts[i] for i in tree.perm[lo_v:hi_v])
            continue
        if not tree.children[v]:  # @line L6
            scanned += hi_v - lo_v
            for i in tree.perm[lo_v:hi_v]:
                p = tree.pts[i]
                if all(value(h, p) <= 0 for h in constraints):
                    count += 1
                    if report:
                        out.append(p)
        else:
            stack.extend(reversed(tree.children[v]))  # @line L7
    if stats is not None:
        stats.update(visits=visits, inside=inside, outside=outside, scanned=scanned)
    return (count, out) if report else count  # @line L8
