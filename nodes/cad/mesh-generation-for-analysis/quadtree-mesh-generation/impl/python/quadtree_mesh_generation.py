# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadtree-mesh-generation/. The authors are listed in prov/C1TYAG.jsonl.

"""Quadtree triangulation of a planar point set after Bern, Eppstein and Gilbert.

The input is a list of at least two distinct points with int or Fraction
coordinates. All arithmetic is exact. A box is a triple (k, i, j): level k,
column i and row j, so its side is S / 2^k and its lower left corner is
origin + (i, j) S / 2^k. The parameter reach is the half width of the block
of boxes that condition C3 looks at: reach=1 is the 3 by 3 block of the
paper, reach=2 (the default) is the 5 by 5 block that this page uses so that
no warped box has a split side.
"""

import math
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from mg2geom import dist2, orient2d

Box = Tuple[int, int, int]
SIDES = ((0, -1), (1, 0), (0, 1), (-1, 0))  # bottom, right, top, left


class Quadtree:
    def __init__(self, points: Sequence, reach: int = 2):
        pts = [tuple(Fraction(c) for c in p) for p in points]
        if len(set(pts)) != len(pts) or len(pts) < 2:
            raise ValueError("need at least two distinct points")
        self.points = pts
        self.reach = reach
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        ext = max(max(xs) - min(xs), max(ys) - min(ys))
        cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        self.side = 4 * ext  # root side 4L: points stay in the middle quarter
        self.origin = (cx - 2 * ext, cy - 2 * ext)  # @line L1
        self.leaves = {(0, 0, 0)}  # @line L2
        self.internal = set()
        self._at_level: Dict[int, Dict[Box, list]] = {}
        self.nn2 = {p: min(dist2(p, q) for q in pts if q != p) for p in pts}

    # geometry of boxes
    def width(self, k: int) -> Fraction:
        return self.side / (1 << k)

    def corner(self, k: int, i: int, j: int) -> tuple:
        w = self.width(k)
        return (self.origin[0] + i * w, self.origin[1] + j * w)

    def inside_root(self, k: int, i: int, j: int) -> bool:
        return 0 <= i < (1 << k) and 0 <= j < (1 << k)

    def index_of(self, p, k: int) -> tuple:
        w = self.width(k)
        return (math.floor((p[0] - self.origin[0]) / w), math.floor((p[1] - self.origin[1]) / w))

    def points_in(self, b: Box) -> list:
        k = b[0]
        if k not in self._at_level:  # map box -> points, one map per level
            m: Dict[Box, list] = {}
            for p in self.points:
                m.setdefault((k,) + self.index_of(p, k), []).append(p)
            self._at_level[k] = m
        return self._at_level[k].get(b, [])

    # tree edits
    def exists(self, b: Box) -> bool:
        return b in self.leaves or b in self.internal

    def split(self, b: Box) -> None:
        k, i, j = b
        self.leaves.remove(b)
        self.internal.add(b)
        for a in (0, 1):
            for c in (0, 1):
                self.leaves.add((k + 1, 2 * i + a, 2 * j + c))

    def make_exist(self, b: Box) -> None:
        """Split the leaf that covers box b until b is a node of the tree."""
        k, i, j = b
        while not self.exists(b):
            for up in range(1, k + 1):
                anc = (k - up, i >> up, j >> up)
                if anc in self.leaves:
                    self.split(anc)
                    break

    def block(self, b: Box, reach: int):
        k, i, j = b
        for di in range(-reach, reach + 1):
            for dj in range(-reach, reach + 1):
                nb = (k, i + di, j + dj)
                if (di or dj) and self.inside_root(*nb):
                    yield nb

    # conditions
    def crowded(self, b: Box) -> bool:
        pts = self.points_in(b)
        if not pts:
            return False
        if len(pts) >= 2:  # C1
            return True
        w = self.width(b[0])
        if self.nn2[pts[0]] < 8 * w * w:  # C2: nearest neighbor closer than 2 sqrt(2) w
            return True
        return any(nb in self.internal for nb in self.block(b, self.reach))  # C3

    def missing_neighbor(self, b: Box):
        if not self.points_in(b):
            return None
        for nb in self.block(b, 1):
            if not self.exists(nb):
                return nb
        return None

    def unbalanced(self, b: Box) -> bool:
        """True if a side of leaf b has two or more quadtree corners inside it."""
        k, i, j = b
        for di, dj in SIDES:
            nb = (k, i + di, j + dj)
            if nb not in self.internal:
                continue
            for a in (0, 1):
                ci = 2 * nb[1] + (a if di == 0 else (0 if di == 1 else 1))
                cj = 2 * nb[2] + (a if dj == 0 else (0 if dj == 1 else 1))
                if (k + 1, ci, cj) in self.internal:
                    return True
        return False

    def build(self, trace=None) -> None:
        """Split until no leaf is crowded, every leaf with a point has its 8 neighbors, and the tree is balanced.

        If trace is a list, each round appends (rule, list of boxes).
        """
        while True:  # @line L3
            todo = [b for b in sorted(self.leaves) if self.crowded(b)]  # @line L4
            if todo:
                done = []
                for b in todo:
                    if b in self.leaves and self.crowded(b):
                        self.split(b)  # @line L5
                        done.append(b)
                        for nb in self.block(b, 1):
                            self.make_exist(nb)
                            if nb in self.leaves:
                                self.split(nb)
                if trace is not None:
                    trace.append(("crowded", done))
                continue
            gaps = [nb for b in sorted(self.leaves) for nb in [self.missing_neighbor(b)] if nb]  # @line L6
            if gaps:
                for nb in gaps:
                    self.make_exist(nb)  # @line L7
                if trace is not None:
                    trace.append(("neighbor", gaps))
                continue
            bad = [b for b in sorted(self.leaves) if self.unbalanced(b)]  # @line L8
            if bad:
                for b in bad:
                    if b in self.leaves:
                        self.split(b)  # @line L9
                if trace is not None:
                    trace.append(("balance", bad))
                continue
            return  # @line L10

    # boundary vertices of a leaf, counterclockwise from the lower left corner
    def boundary(self, b: Box) -> list:
        k, i, j = b
        w = self.width(k)
        x0, y0 = self.corner(k, i, j)
        corners = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + w), (x0, y0 + w)]
        out = []
        for s, (di, dj) in enumerate(SIDES):
            out.append(("corner", corners[s]))
            if (k, i + di, j + dj) in self.internal:
                p, q = corners[s], corners[(s + 1) % 4]
                out.append(("mid", ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)))
        return out


def aspect(a, b, c) -> Fraction:
    """Exact aspect ratio of Bern, Eppstein and Gilbert: longest side over the altitude to it.

    It equals longest^2 / (2 area) = longest^2 / |orient2d|.
    """
    t = orient2d(a, b, c)
    if t == 0:
        raise ValueError("flat triangle")
    longest2 = max(dist2(a, b), dist2(b, c), dist2(c, a))
    return Fraction(longest2) / abs(t)


def quadtree_mesh(points: Sequence, reach: int = 2):
    """Return (tree, vertices, triangles). Triangles are counterclockwise triples of vertex indices."""
    t = Quadtree(points, reach)
    t.build()
    warp: Dict[tuple, tuple] = {}
    for p in t.points:  # @line L11
        k = max(b[0] for b in t.leaves)
        while True:  # find the leaf that holds p
            i, j = t.index_of(p, k)
            if (k, i, j) in t.leaves:
                break
            k -= 1
        x0, y0 = t.corner(k, i, j)
        w = t.width(k)
        cs = [(x0, y0), (x0, y0 + w), (x0 + w, y0), (x0 + w, y0 + w)]
        y = min(cs, key=lambda c: (dist2(c, p), c))  # nearest corner, ties to the smallest
        if y in warp:
            raise AssertionError("two points warp one corner")
        warp[y] = p
    index: Dict[tuple, int] = {}
    verts: List[tuple] = []

    def vid(p) -> int:
        if p not in index:
            index[p] = len(verts)
            verts.append(p)
        return index[p]

    tris: List[tuple] = []
    for b in sorted(t.leaves):  # @line L12
        bd = t.boundary(b)
        warped = [p for kind, p in bd if kind == "corner" and p in warp]
        if not warped:  # @line L13
            k, i, j = b
            w = t.width(k)
            x0, y0 = t.corner(k, i, j)
            c = (x0 + w / 2, y0 + w / 2)
            ring = [p for _, p in bd]
            for s in range(len(ring)):
                tris.append((vid(c), vid(ring[s]), vid(ring[(s + 1) % len(ring)])))
            continue
        if len(warped) != 1 or len(bd) != 4:
            raise AssertionError("warped box with a split side or two warped corners")
        q = [warp.get(p, p) for _, p in bd]  # @line L14
        best = None
        for d in (0, 1):  # diagonal q[d] q[d + 2]
            pair = [(q[d], q[d + 1], q[(d + 2) % 4]), (q[d], q[(d + 2) % 4], q[(d + 3) % 4])]
            if any(orient2d(*tri) <= 0 for tri in pair):
                continue
            score = max(aspect(*tri) for tri in pair)
            if best is None or score < best[0]:
                best = (score, pair)
        for tri in best[1]:
            tris.append(tuple(vid(p) for p in tri))
    return t, verts, tris  # @line L15
