# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/efficient-ransac-shape-detection/. The authors are listed in prov/NAW12G.jsonl.
"""Efficient RANSAC for shape detection in a point cloud with normals, after
Schnabel, Wahl and Klein (2007), for planes, spheres and cylinders.

The three ideas of the method are here:

1. Localized sampling. The first point of a minimal set is drawn uniformly;
   the other two are drawn from the octree cell of the first point at a
   random level, so they are likely to lie on the same shape.
2. Lazy scoring. The points are split once into random subsets. A candidate
   is scored on the first subset, its score is extrapolated to an interval,
   and it is scored on more subsets only while its interval overlaps the
   interval of the best candidate.
3. Probabilistic extraction. The best candidate is extracted when the
   probability that a shape of its size was missed by every draw so far is
   below 1 - p_t. The extracted shape keeps only the largest connected set of
   its compatible points, and those points are removed.

A point is compatible with a shape when it is within eps of the shape and
its normal is within alpha of the shape normal there, up to sign.

Simplifications, compared with the paper: the octree level is drawn
uniformly, the subsets have equal sizes, the interval uses a normal
approximation, the candidates are cleared after each extraction, the
connectivity uses a 3D distance beta in place of a bitmap in the parameter
domain of the shape, and the shape is not refitted to its points. Cones and
tori are left out. The draw probability uses the bound for uniform
sampling, (n / |R|)^3.
"""

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Sequence, Set, Tuple

Vec = Tuple[float, float, float]
Shape = Tuple[str, tuple]


def _sub(a, b) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _add(a, b) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _mul(s: float, a) -> Vec:
    return (s * a[0], s * a[1], s * a[2])


def _dot(a, b) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _norm(a) -> float:
    return math.sqrt(_dot(a, a))


def _unit(a) -> Optional[Vec]:
    length = _norm(a)
    if length < 1e-12:
        return None
    return _mul(1.0 / length, a)


def shape_distance_and_normal(shape: Shape, p) -> Tuple[float, Optional[Vec]]:
    """Distance from p to the shape, and the unit shape normal at the
    closest point (None where it is not defined)."""
    kind, par = shape
    if kind == "plane":
        n, d = par
        return abs(_dot(n, p) - d), n
    if kind == "sphere":
        c, r = par
        v = _sub(p, c)
        return abs(_norm(v) - r), _unit(v)
    c, a, r = par  # cylinder: a point c on the axis, the unit direction a
    v = _sub(p, c)
    radial = _sub(v, _mul(_dot(v, a), a))
    return abs(_norm(radial) - r), _unit(radial)


def compatible(shape: Shape, p, n, eps: float, cos_alpha: float) -> bool:
    dist, sn = shape_distance_and_normal(shape, p)
    return dist <= eps and sn is not None and abs(_dot(sn, n)) >= cos_alpha


def _closest_points_of_lines(p1, d1, p2, d2) -> Optional[Tuple[Vec, Vec]]:
    """Closest points of the lines p1 + t d1 and p2 + u d2, unit d1 and d2."""
    b = _dot(d1, d2)
    denom = 1.0 - b * b
    if denom < 1e-6:
        return None
    w = _sub(p1, p2)
    d, e = _dot(d1, w), _dot(d2, w)
    t = (b * e - d) / denom
    u = (e - b * d) / denom
    return _add(p1, _mul(t, d1)), _add(p2, _mul(u, d2))


def fit_plane(ps, ns, eps: float, cos_alpha: float) -> Optional[Shape]:
    n = _unit(_cross(_sub(ps[1], ps[0]), _sub(ps[2], ps[0])))
    if n is None:
        return None
    shape = ("plane", (n, _dot(n, ps[0])))
    return shape if all(compatible(shape, p, m, eps, cos_alpha) for p, m in zip(ps, ns)) else None


def fit_sphere(ps, ns, eps: float, cos_alpha: float, max_radius: float) -> Optional[Shape]:
    """The center is the midpoint of the closest points of the two normal
    lines; the third point only verifies."""
    cp = _closest_points_of_lines(ps[0], ns[0], ps[1], ns[1])
    if cp is None:
        return None
    c = _mul(0.5, _add(cp[0], cp[1]))
    r = 0.5 * (_norm(_sub(ps[0], c)) + _norm(_sub(ps[1], c)))
    if r > max_radius:
        return None
    shape = ("sphere", (c, r))
    return shape if all(compatible(shape, p, m, eps, cos_alpha) for p, m in zip(ps, ns)) else None


def fit_cylinder(ps, ns, eps: float, cos_alpha: float, max_radius: float) -> Optional[Shape]:
    """The axis direction is n1 x n2; the axis passes through the meeting
    point of the two normal lines projected along it."""
    a = _unit(_cross(ns[0], ns[1]))
    if a is None:
        return None
    q1 = _sub(ps[0], _mul(_dot(ps[0], a), a))
    q2 = _sub(ps[1], _mul(_dot(ps[1], a), a))
    m1 = _unit(_sub(ns[0], _mul(_dot(ns[0], a), a)))
    m2 = _unit(_sub(ns[1], _mul(_dot(ns[1], a), a)))
    if m1 is None or m2 is None:
        return None
    cp = _closest_points_of_lines(q1, m1, q2, m2)
    if cp is None:
        return None
    c = _mul(0.5, _add(cp[0], cp[1]))

    def axis_distance(p) -> float:
        v = _sub(p, c)
        return _norm(_sub(v, _mul(_dot(v, a), a)))

    r = 0.5 * (axis_distance(ps[0]) + axis_distance(ps[1]))
    if r > max_radius:
        return None
    shape = ("cylinder", (c, a, r))
    return shape if all(compatible(shape, p, m, eps, cos_alpha) for p, m in zip(ps, ns)) else None


class Octree:
    """An implicit octree: the cell of a point at level l is its integer
    key in a grid of 2^l cells per side over the bounding cube."""

    def __init__(self, points: Sequence[Sequence[float]], depth: int) -> None:
        self.depth = depth
        self.origin = tuple(min(p[i] for p in points) for i in range(3))
        self.size = max(max(p[i] for p in points) - self.origin[i] for i in range(3)) or 1.0
        self.cells: List[Dict[tuple, List[int]]] = []
        for level in range(depth + 1):
            table: Dict[tuple, List[int]] = {}
            for i, p in enumerate(points):
                table.setdefault(self.key(p, level), []).append(i)
            self.cells.append(table)

    def key(self, p, level: int) -> tuple:
        side = 1 << level
        return tuple(min(side - 1, int((p[i] - self.origin[i]) / self.size * side)) for i in range(3))

    def cell(self, p, level: int) -> List[int]:
        return self.cells[level][self.key(p, level)]


class Candidate:
    """A shape with a lazily computed score over the random subsets."""

    def __init__(self, shape: Shape, ident: int) -> None:
        self.shape, self.ident = shape, ident
        self.j = 0  # the number of subsets scored
        self.hits = 0  # compatible points among the tested points
        self.tested = 0  # remaining points of the scored subsets
        self.est = self.lo = self.hi = 0.0

    def refine(self, subsets, remaining: Set[int], points, normals, eps, cos_alpha) -> None:
        for i in subsets[self.j]:
            if i in remaining:
                self.tested += 1
                if compatible(self.shape, points[i], normals[i], eps, cos_alpha):
                    self.hits += 1
        self.j += 1
        size = len(remaining)
        if self.j == len(subsets):
            self.est = self.lo = self.hi = float(self.hits)
        elif self.tested == 0:
            self.est, self.lo, self.hi = 0.0, 0.0, float(size)
        else:
            f = self.hits / self.tested
            self.est = f * size
            half = 2.0 * size * math.sqrt(f * (1.0 - f) / self.tested) + size / self.tested
            self.lo, self.hi = max(0.0, self.est - half), min(float(size), self.est + half)


def _separate(cands: List[Candidate], subsets, remaining, points, normals, eps, cos_alpha) -> Candidate:
    """Refine until the best candidate's interval overlaps no other one."""
    while True:
        best = max(cands, key=lambda c: (c.est, -c.ident))
        rivals = [c for c in cands if c is not best and c.hi >= best.lo]
        todo = [c for c in rivals + [best] if c.j < len(subsets)]
        if not rivals or not todo:
            return best
        for c in todo:
            c.refine(subsets, remaining, points, normals, eps, cos_alpha)


def largest_component(points, idxs: Sequence[int], beta: float) -> List[int]:
    """The largest set of the given points connected by steps of length at
    most beta. Ties go to the set with the smallest index."""
    grid: Dict[tuple, List[int]] = {}
    for i in idxs:
        grid.setdefault(tuple(math.floor(x / beta) for x in points[i]), []).append(i)
    seen: Set[int] = set()
    best: List[int] = []
    for start in sorted(idxs):
        if start in seen:
            continue
        seen.add(start)
        comp, stack = [start], [start]
        while stack:
            i = stack.pop()
            kx, ky, kz = (math.floor(x / beta) for x in points[i])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        for j in grid.get((kx + dx, ky + dy, kz + dz), ()):
                            if j not in seen and math.dist(points[i], points[j]) <= beta:
                                seen.add(j)
                                comp.append(j)
                                stack.append(j)
        if len(comp) > len(best):
            best = comp
    return sorted(best)


def hit_probability(n: float, remaining: int, draws: int) -> float:
    """The probability that at least one of the draws hits a shape of n
    points, for uniform draws of three points: 1 - (1 - (n/|R|)^3)^draws."""
    if remaining == 0 or n <= 0:
        return 0.0
    p = min(1.0, n / remaining) ** 3
    return 1.0 - (1.0 - p) ** draws


def detect_shapes(points: Sequence[Sequence[float]], normals: Sequence[Sequence[float]],
                  eps: float, alpha_degrees: float, beta: float, min_support: int,
                  p_t: float = 0.99, depth: int = 4, num_subsets: int = 8,
                  seed: int = 0) -> List[Tuple[Shape, List[int]]]:
    """Return the detected shapes in the order of extraction, each with the
    sorted indices of its points."""
    if min_support < 3:
        raise ValueError("min_support must be at least 3")
    if len(points) != len(normals):
        raise ValueError("one normal per point")
    n = len(points)
    if n < min_support:
        return []
    rng = random.Random(seed)
    cos_alpha = math.cos(math.radians(alpha_degrees))
    tree = Octree(points, depth)  # @line L1
    order = list(range(n))
    rng.shuffle(order)
    subsets = [order[i::num_subsets] for i in range(num_subsets)]
    max_radius = tree.size
    remaining: Set[int] = set(range(n))  # @line L2
    cands: List[Candidate] = []
    draws, made = 0, 0
    shapes: List[Tuple[Shape, List[int]]] = []
    pool = sorted(remaining)  # R as a list, rebuilt after each extraction
    while len(remaining) >= min_support:  # @line L3
        first = rng.choice(pool)  # @line L4
        level = rng.randint(0, depth)
        while True:
            others = [i for i in tree.cell(points[first], level) if i in remaining and i != first]
            if len(others) >= 2 or level == 0:
                break
            level -= 1
        sample = [first] + rng.sample(others, 2)
        draws += 1
        ps = [points[i] for i in sample]
        ns = [normals[i] for i in sample]
        fits = (fit_plane(ps, ns, eps, cos_alpha),  # @line L5
                fit_sphere(ps, ns, eps, cos_alpha, max_radius),
                fit_cylinder(ps, ns, eps, cos_alpha, max_radius))
        for shape in fits:
            if shape is not None:
                made += 1
                cand = Candidate(shape, made)
                cand.refine(subsets, remaining, points, normals, eps, cos_alpha)  # @line L6
                cands.append(cand)
        extracted = False
        if cands:
            best = _separate(cands, subsets, remaining, points, normals, eps, cos_alpha)  # @line L7
            if hit_probability(best.est, len(remaining), draws) >= p_t:  # @line L8
                inliers = [i for i in remaining
                           if compatible(best.shape, points[i], normals[i], eps, cos_alpha)]
                comp = largest_component(points, inliers, beta)  # @line L9
                if len(comp) >= min_support:  # @line L10
                    shapes.append((best.shape, comp))
                    remaining.difference_update(comp)
                    pool = sorted(remaining)
                    cands, draws, extracted = [], 0, True
                else:
                    cands.remove(best)  # @line L11
        if not extracted and hit_probability(min_support, len(remaining), draws) >= p_t:  # @line L12
            break
    return shapes  # @line L13
