# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isosurface-stuffing/. The authors are listed in prov/B7WM22.jsonl.

"""Isosurface stuffing of Labelle and Shewchuk (2007), uniform version, for a ball.

The background grid is the body-centred cubic (BCC) lattice of spacing h. A
lattice point is stored by its doubled coordinates (i, j, k): all even for the
cubic lattice Z^3 and all odd for the shifted lattice Z^3 + (1/2, 1/2, 1/2).
Its position is (h/2)(i, j, k). An edge is *black* (long, axis aligned, length
h) or *red* (short, length h sqrt(3)/2).

The domain is the ball f(x) = r2 - |x - center|^2 > 0. The four steps are those
of the paper: values at the lattice points, cut points on the edges with a sign
change, warping of violated lattice points onto the surface, and stencils.
Cut points are the exact zeros of f on the edge, rounded once to a float and
then kept as exact fractions. Every predicate on positions is exact.
"""

import math
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from mg2geom import orient3d

# The row "minimum dihedral angle, unsafe" of Table 1 of the paper.
ALPHA_LONG = Fraction("0.28511")
ALPHA_SHORT = Fraction("0.39882")
DIHEDRAL_MIN = 10.7843
DIHEDRAL_MAX = 164.7373

BLACK_STEPS = [tuple(2 * s if a == i else 0 for a in range(3)) for i in range(3) for s in (1, -1)]
RED_STEPS = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]

Key = Tuple[int, int, int]


def is_black(p: Key, q: Key) -> bool:
    return sum(1 for a, b in zip(p, q) if a != b) == 1


def bcc_tetrahedra(points: set):
    """All BCC grid tetrahedra with the four vertices in points.

    Each one has exactly one black edge of the cubic lattice, so it is listed
    once: for the black edge p, p + 2e_i, the four centers around the edge give
    four tetrahedra.
    """
    out = []
    for p in sorted(points):
        if p[0] % 2:
            continue
        for i in range(3):
            q = tuple(p[a] + (2 if a == i else 0) for a in range(3))
            if q not in points:
                continue
            j, k = [a for a in range(3) if a != i]
            ring = []
            for sj, sk in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
                c = [0, 0, 0]
                c[i], c[j], c[k] = p[i] + 1, p[j] + sj, p[k] + sk
                ring.append(tuple(c))
            for s in range(4):
                c1, c2 = ring[s], ring[(s + 1) % 4]
                if c1 in points and c2 in points:
                    out.append((p, q, c1, c2))
    return out


class Stuffing:
    def __init__(self, center: Sequence, r2, h, alpha_long=ALPHA_LONG, alpha_short=ALPHA_SHORT):
        self.center = tuple(Fraction(c) for c in center)
        self.r2 = Fraction(r2)
        self.h = Fraction(h)
        if self.r2 <= 0 or self.h <= 0:
            raise ValueError("need r2 > 0 and h > 0")
        self.alpha = {True: Fraction(alpha_long), False: Fraction(alpha_short)}
        half = self.h / 2
        r = math.sqrt(self.r2)
        lo = [math.floor((float(c) - r) / float(half)) - 3 for c in self.center]
        hi = [math.ceil((float(c) + r) / float(half)) + 3 for c in self.center]
        self.points = {
            (i, j, k)
            for i in range(lo[0], hi[0] + 1)
            for j in range(lo[1], hi[1] + 1)
            for k in range(lo[2], hi[2] + 1)
            if i % 2 == j % 2 == k % 2
        }
        self.orig = {p: tuple(half * x for x in p) for p in self.points}
        self.pos = dict(self.orig)
        self.value = {p: self.f(self.orig[p]) for p in self.points}  # @line L1
        self.cut_t: Dict[tuple, Fraction] = {}
        self.warped: Dict[Key, Key] = {}

    def f(self, x) -> Fraction:
        return self.r2 - sum((a - c) ** 2 for a, c in zip(x, self.center))

    def neighbors(self, p: Key):
        for d in BLACK_STEPS + RED_STEPS:
            q = (p[0] + d[0], p[1] + d[1], p[2] + d[2])
            if q in self.points:
                yield q

    # cut points
    def has_cut(self, p: Key, q: Key) -> bool:
        return self.value[p] * self.value[q] < 0

    def cut_param(self, p: Key, q: Key) -> Fraction:
        """The position of the cut point on edge pq, as a fraction of the way from p to q."""
        e = (p, q) if p < q else (q, p)
        if e not in self.cut_t:
            a, b = self.orig[e[0]], self.orig[e[1]]
            d = [y - x for x, y in zip(a, b)]
            w = [x - c for x, c in zip(a, self.center)]
            # f(a + t d) = C0 - 2 t B - t^2 A with C0 = f(a), B = d . w, A = |d|^2.
            # If a is inside, the roots have opposite signs and we want the positive one.
            # If a is outside and b inside, we want the smaller root, where the edge enters.
            A = float(sum(x * x for x in d))
            B = float(sum(x * y for x, y in zip(d, w)))
            C0 = float(self.f(a))
            root = math.sqrt(max(0.0, B * B + A * C0))
            t = (-B + root) / A if C0 > 0 else (-B - root) / A
            self.cut_t[e] = min(max(Fraction(t), Fraction(0)), Fraction(1))  # @line L2
        t = self.cut_t[e]
        return t if e[0] == p else 1 - t

    def cut_point(self, p: Key, q: Key) -> tuple:
        s = self.cut_param(p, q)
        a, b = self.orig[p], self.orig[q]
        return tuple(x + s * (y - x) for x, y in zip(a, b))

    # step 3
    def warp(self) -> None:
        for q in sorted(self.points):  # @line L3
            if self.value[q] == 0:
                continue
            best = None
            for r in self.neighbors(q):
                if not self.has_cut(q, r):
                    continue
                s = self.cut_param(q, r)
                if s < self.alpha[is_black(q, r)]:  # @line L4
                    d2 = s * s * sum((x - y) ** 2 for x, y in zip(self.orig[q], self.orig[r]))
                    if best is None or (d2, r) < best[:2]:
                        best = (d2, r)
            if best is not None:
                r = best[1]
                self.pos[q] = self.cut_point(q, r)  # @line L5
                self.value[q] = Fraction(0)  # its cut points disappear with its sign
                self.warped[q] = r

    # step 4
    def quad_diagonal(self, a: Key, b: Key, x: Key) -> frozenset:
        """Diagonal of the quadrilateral that face abx leaves, with a, b positive and x negative.

        Its corners are a, b, cut(b, x), cut(a, x). A truncated black edge
        gives the diagonal at its cut point; a whole black edge ab uses the
        Parity Rule.
        """
        ca, cb = ("c",) + edge(a, x), ("c",) + edge(b, x)
        A, B = ("v", a), ("v", b)
        if is_black(a, x):
            return frozenset((B, ca))
        if is_black(b, x):
            return frozenset((A, cb))
        # Parity Rule: diagonals are a-c and b-d with c = cut(b, x), d = cut(a, x).
        # A coordinate of a is greater than that of c exactly when 2 a > b + x
        # coordinatewise, since c lies strictly inside the red edge bx.
        odd = sum(1 for i in range(3) if 2 * a[i] > b[i] + x[i]) % 2 == 1
        on_cubic = a[0] % 2 == 0
        return frozenset((A, cb)) if odd == on_cubic else frozenset((B, ca))

    def stencil(self, tet: Sequence[Key]) -> List[tuple]:
        pos = [v for v in tet if self.value[v] > 0]
        zero = [v for v in tet if self.value[v] == 0]
        neg = [v for v in tet if self.value[v] < 0]
        V = lambda v: ("v", v)  # noqa: E731
        C = lambda p, q: ("c",) + edge(p, q)  # noqa: E731
        if not pos:
            return []  # @line L7
        if not neg:
            return [tuple(V(v) for v in tet)]  # @line L8
        if len(pos) == 1:  # @line L9
            a = pos[0]
            return [(V(a),) + tuple(V(z) for z in zero) + tuple(C(a, x) for x in neg)]
        if len(pos) == 2 and len(zero) == 1:  # @line L10
            (a, b), z, d = pos, zero[0], neg[0]
            g = self.quad_diagonal(a, b, d)
            if g == frozenset((V(a), C(b, d))):
                return [(V(z), V(a), V(b), C(b, d)), (V(z), V(a), C(b, d), C(a, d))]
            return [(V(z), V(a), V(b), C(a, d)), (V(z), V(b), C(b, d), C(a, d))]
        if len(pos) == 2:  # @line L11
            (a, b), (c, d) = pos, neg
            bottom = (V(a), C(a, c), C(a, d))
            top = (V(b), C(b, c), C(b, d))
            q0 = self.quad_diagonal(a, b, c)
            q2 = self.quad_diagonal(a, b, d)
            for q1 in (frozenset((C(a, c), C(b, d))), frozenset((C(a, d), C(b, c)))):
                try:
                    return split_prism(bottom, top, [q0, q1, q2])
                except ValueError:
                    continue
            raise AssertionError("no prism split")
        a, b, c = pos  # @line L12
        d = neg[0]
        bottom = (V(a), V(b), V(c))
        top = (C(a, d), C(b, d), C(c, d))
        diags = [self.quad_diagonal(a, b, d), self.quad_diagonal(b, c, d), self.quad_diagonal(c, a, d)]
        return split_prism(bottom, top, diags)

    def position(self, key, warped=True) -> tuple:
        if key[0] == "v":
            return (self.pos if warped else self.orig)[key[1]]
        return self.cut_point(key[1], key[2])

    def mesh(self):
        """Run the four steps. Returns (vertices, tetrahedra) with positive orientation."""
        self.warp()
        index: Dict[tuple, int] = {}
        verts: List[tuple] = []
        tets: List[tuple] = []
        for tet in bcc_tetrahedra(self.points):  # @line L6
            for piece in self.stencil(tet):
                # orient by the unwarped positions, where the piece is a part of the BCC tetrahedron
                o = orient3d(*[self.position(k, warped=False) for k in piece])
                if o == 0:
                    raise AssertionError("flat stencil piece")
                if o < 0:
                    piece = (piece[1], piece[0]) + tuple(piece[2:])
                ids = []
                for k in piece:
                    p = self.position(k)
                    if p not in index:
                        index[p] = len(verts)
                        verts.append(p)
                    ids.append(index[p])
                tets.append(tuple(ids))  # @line L13
        return verts, tets


def edge(p: Key, q: Key) -> tuple:
    return (p, q) if p < q else (q, p)


def split_prism(bottom: Sequence, top: Sequence, diags: Sequence[frozenset]) -> List[tuple]:
    """Cut a prism into three tetrahedra with the given diagonals of its quadrilaterals.

    bottom[i] and top[i] are joined by an edge, and diags[i] is the diagonal of
    the quadrilateral bottom[i], bottom[i+1], top[i+1], top[i]. A split exists
    if and only if some vertex is the end of two diagonals; otherwise
    ValueError is raised.
    """
    six = list(bottom) + list(top)
    deg = {v: sum(1 for g in diags if v in g) for v in six}
    twice = [v for v in six if deg[v] == 2]
    if not twice:
        raise ValueError("the three diagonals form a cycle")
    v = twice[0]
    quads = [(bottom[i], bottom[(i + 1) % 3], top[(i + 1) % 3], top[i]) for i in range(3)]
    if v in top:
        bottom, top = top, bottom
        quads = [(q[3], q[2], q[1], q[0]) for q in quads]
    i = list(bottom).index(v)
    far = (i + 1) % 3
    out = [(v, top[0], top[1], top[2])]
    a, b, c, d = quads[far]
    if diags[far] == frozenset((a, c)):
        out += [(v, a, b, c), (v, a, c, d)]
    else:
        out += [(v, a, b, d), (v, b, c, d)]
    return out


def isosurface_stuffing(center: Sequence, r2, h, **kw):
    """Mesh the ball |x - center|^2 < r2 with a BCC lattice of spacing h.

    Returns (stuffing state, vertices, tetrahedra).
    """
    s = Stuffing(center, r2, h, **kw)
    verts, tets = s.mesh()
    return s, verts, tets  # @line L14
