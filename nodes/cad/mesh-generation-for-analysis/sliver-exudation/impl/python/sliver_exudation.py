# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliver-exudation/. The authors are listed in prov/4WRSY6.jsonl.

"""Sliver exudation (Cheng, Dey, Edelsbrunner, Facello and Teng, 2000).

Each vertex u in turn is "pumped": its weight (the square U^2 of the radius of
a sphere centered at u) is chosen among the weights for which the weighted
Delaunay (regular) triangulation is free of the worst tetrahedra around u.
The weight is kept at most (OMEGA * d_u)^2, where d_u is the distance from u to
its nearest neighbor and OMEGA < 1/2, so the spheres stay disjoint and every
point stays a vertex. As in Edelsbrunner and Guoy's implementation, the weight
chosen is the one that maximizes the smallest dihedral angle of the star of u.

The paper treats periodic point sets, which have no boundary. Here the points
lie in an axis-aligned box whose 8 corners are part of the input; the corners
keep weight 0, and only the points strictly inside are pumped.

Coordinates and weights are integers, so every power (weighted insphere) test
is exact integer arithmetic. A chosen weight is an integer strictly between two
consecutive critical weights, so no degenerate configuration is ever chosen.
"""

import math
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Set, Tuple

from mg2geom import det4, dihedral_angles_deg, dist2, orient3d, sub

Tet = Tuple[int, int, int, int]
Face = Tuple[int, int, int]

OMEGA = Fraction(9, 20)  # Edelsbrunner and Guoy use 0.45; any constant in (0, 1/2) is allowed


def power_test(a, b, c, d, e, wa=0, wb=0, wc=0, wd=0, we=0):
    """Positive if the weighted point (e, we) conflicts with the orthosphere of abcd.

    The value is -det of the rows (p - e, |p - e|^2 - w_p + w_e) for p = a, b, c,
    d, times the sign of orient3d(a, b, c, d). It equals -pi * |orient3d|, where
    pi = |e - z|^2 - Z^2 - w_e is the power distance from (e, we) to the
    orthosphere (z, Z^2) of the four weighted points. So it is positive exactly
    when pi < 0, and with all weights 0 it is the ordinary insphere test.
    """
    rows = []
    for p, w in ((a, wa), (b, wb), (c, wc), (d, wd)):
        v = sub(p, e)
        rows.append([v[0], v[1], v[2], v[0] * v[0] + v[1] * v[1] + v[2] * v[2] - w + we])
    o = orient3d(a, b, c, d)
    if o == 0:
        raise ValueError("flat tetrahedron")
    val = -det4(rows)
    return val if o > 0 else -val  # @line L11


def critical_weight(a, b, c, d, u, wa=0, wb=0, wc=0, wd=0) -> Fraction:
    """The power pi_t(u) = |u - z|^2 - Z^2 of the point u to the orthosphere of abcd.

    The weighted point (u, w) conflicts with the tetrahedron exactly when w > pi_t(u).
    """
    rows = []
    for p, w in ((a, wa), (b, wb), (c, wc), (d, wd)):
        v = sub(p, u)
        rows.append([v[0], v[1], v[2], v[0] * v[0] + v[1] * v[1] + v[2] * v[2] - w])
    return Fraction(det4(rows), orient3d(a, b, c, d))


def faces_of(t: Tet) -> List[Face]:
    return [tuple(sorted(t[:i] + t[i + 1 :])) for i in range(4)]


def min_dihedral(pts, tets) -> float:
    return min(min(dihedral_angles_deg(*[pts[v] for v in t])) for t in tets)


class Exuder:
    def __init__(self, side: int, inner: Sequence[Sequence[int]], omega: Fraction = OMEGA):
        if side <= 0:
            raise ValueError("side must be positive")
        self.omega = Fraction(omega)
        if not 0 < self.omega < Fraction(1, 2):
            raise ValueError("omega must lie in (0, 1/2)")
        corners = [(x, y, z) for x in (0, side) for y in (0, side) for z in (0, side)]
        self.pts: List[tuple] = corners + [tuple(int(c) for c in p) for p in inner]
        if len(set(self.pts)) != len(self.pts):
            raise ValueError("repeated point")
        for p in self.pts[8:]:
            if not all(0 < c < side for c in p):
                raise ValueError("inner points must lie strictly inside the box")
        self.side = side
        self.w: List[int] = [0] * len(self.pts)
        self.tets: Set[Tet] = self.triangulate(range(len(self.pts)))  # @line L1
        self.log: List[tuple] = []

    # weighted Delaunay triangulation by Bowyer-Watson insertion with the power test
    def conflicts(self, t: Tet, v: int) -> bool:
        P, W = self.pts, self.w
        return power_test(*[P[x] for x in t], P[v], *[W[x] for x in t], W[v]) > 0

    def triangulate(self, verts) -> Set[Tet]:
        """The regular triangulation of the given vertices with the current weights.

        The 8 corners are always included and start as 6 tetrahedra around the
        diagonal; they are cospherical with equal weights, so this is regular.
        """
        P = self.pts
        tets: Set[Tet] = set()
        face_tets: Dict[Face, Set[Tet]] = {}

        def add(t):
            if orient3d(*[P[x] for x in t]) < 0:
                t = (t[1], t[0], t[2], t[3])
            if orient3d(*[P[x] for x in t]) == 0:
                raise AssertionError("flat tetrahedron: the cavity is not star-shaped")
            tets.add(t)
            for f in faces_of(t):
                face_tets.setdefault(f, set()).add(t)

        def remove(t):
            tets.discard(t)
            for f in faces_of(t):
                face_tets[f].discard(t)
                if not face_tets[f]:
                    del face_tets[f]

        for path in ((1, 3), (1, 5), (2, 3), (2, 6), (4, 5), (4, 6)):
            add((0, path[0], path[1], 7))
        for v in verts:
            if v < 8:
                continue
            start = next(t for t in tets if self.conflicts(t, v))
            cavity, stack = {start}, [start]
            while stack:
                t = stack.pop()
                for f in faces_of(t):
                    for s in face_tets[f]:
                        if s not in cavity and self.conflicts(s, v):
                            cavity.add(s)
                            stack.append(s)
            boundary = [f for t in cavity for f in faces_of(t) if not any(s in cavity for s in face_tets[f] if s != t)]
            for t in cavity:
                remove(t)
            for f in boundary:
                add(f + (v,))
        return tets

    def nearest2(self, u: int) -> int:
        return min(dist2(self.pts[u], q) for i, q in enumerate(self.pts) if i != u)

    def star(self, rest: Set[Tet], crit: Dict[Tet, Fraction], u: int, w) -> Tuple[Set[Tet], List[Tet]]:
        """The cavity {t in rest : crit[t] < w} and the cone from u over its boundary."""
        cavity = {t for t in rest if crit[t] < w}
        count: Dict[Face, int] = {}
        for t in cavity:
            for f in faces_of(t):
                count[f] = count.get(f, 0) + 1
        cone = []
        for f, m in count.items():
            if m == 1:
                t = f + (u,)
                o = orient3d(*[self.pts[x] for x in t])
                if o == 0:
                    raise AssertionError("flat tetrahedron in the star")
                cone.append(t if o > 0 else (t[1], t[0], t[2], t[3]))
        return cavity, cone

    def pump(self, u: int) -> int:
        P = self.pts
        rest = self.triangulate([v for v in range(len(P)) if v != u])  # @line L3
        crit = {t: critical_weight(*[P[x] for x in t], P[u], *[self.w[x] for x in t]) for t in rest}  # @line L4
        wmax = math.floor(self.omega**2 * self.nearest2(u))  # @line L5
        cuts = sorted({c for c in crit.values() if 0 < c < wmax})
        # the current weight 0, and one integer strictly inside each interval
        cands = [0]  # @line L6
        for lo, hi in zip([Fraction(0)] + cuts, cuts + [Fraction(wmax + 1)]):
            m = math.floor((lo + hi) / 2)
            for x in (m, m + 1, math.floor(lo) + 1):
                if lo < x < hi and x <= wmax:
                    cands.append(x)
                    break
        best = None
        for w in cands:
            if w != 0 and w in crit.values():
                continue
            cavity, cone = self.star(rest, crit, u, w)  # @line L7
            zeta = min_dihedral(P, cone)
            if best is None or zeta > best[0]:  # @line L8
                best = (zeta, w, cavity, cone)
        zeta0 = min_dihedral(P, self.star(rest, crit, u, 0)[1])
        _, w, cavity, cone = best
        self.w[u] = w  # @line L9
        self.tets = (rest - cavity) | set(cone)
        self.log.append((u, w, wmax, len(cands), zeta0, best[0]))
        return w

    def run(self) -> None:
        for u in range(8, len(self.pts)):  # @line L2
            self.pump(u)


def sliver_exudation(side: int, inner: Sequence[Sequence[int]], omega: Fraction = OMEGA) -> Exuder:
    """Pump every inner point once; return the Exuder with fields pts, w (weights) and tets."""
    e = Exuder(side, inner, omega)
    e.run()
    return e  # @line L10
