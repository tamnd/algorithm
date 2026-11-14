# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/topological-tetrahedral-mesh-improvement/. The authors are listed in prov/JMSVP1.jsonl.

"""2-3 and 3-2 flips of a tetrahedral mesh, and hill climbing with them.

A mesh is a list of points (tuples of Fraction) and a list of tetrahedra, each a
tuple of four vertex indices with orient3d > 0. A 2-3 flip replaces the two
tetrahedra abcd and abce on the face abc by abde, bcde and cade; a 3-2 flip is
the inverse. Every validity decision is an exact orient3d sign. The quality of
a tetrahedron (the mean ratio) is measured in floats and used only to decide
whether a valid flip is an improvement.
"""

import math
from itertools import combinations
from typing import Dict, FrozenSet, List, Optional, Sequence, Tuple

from mg3geom import orient3d

Tet = Tuple[int, int, int, int]


def positive(points, t: Sequence[int]) -> Tet:
    """The tetrahedron t with its vertices ordered so that orient3d > 0.
    Raises ValueError if it is flat."""
    a, b, c, d = t
    s = orient3d(points[a], points[b], points[c], points[d])
    if s == 0:
        raise ValueError("flat tetrahedron")
    return (a, b, c, d) if s > 0 else (b, a, c, d)


def mean_ratio(points, t: Sequence[int]) -> float:
    """12 (3V)^(2/3) / (sum of the six squared edge lengths): 1 for the regular
    tetrahedron, 0 for a flat one, negative if inverted."""
    p = [points[i] for i in t]
    v = float(orient3d(*p)) / 6.0
    s = sum(float(sum((x - y) ** 2 for x, y in zip(p[i], p[j]))) for i, j in combinations(range(4), 2))
    return math.copysign(12.0 * (3.0 * abs(v)) ** (2.0 / 3.0) / s, v)


def faces(tets: Sequence[Tet]) -> Dict[FrozenSet[int], List[int]]:
    """Map each face (a set of three vertices) to the indices of its tetrahedra."""
    out: Dict[FrozenSet[int], List[int]] = {}
    for k, t in enumerate(tets):
        for f in combinations(t, 3):
            out.setdefault(frozenset(f), []).append(k)
    return out


def flip23(points, tets: Sequence[Tet], face: FrozenSet[int]) -> Optional[List[Tet]]:
    """The three tetrahedra that replace the two on `face`, or None if the flip
    is invalid. Valid iff the segment between the two apexes crosses the
    interior of the face, that is, iff the three new tetrahedra have orient3d
    of one strict sign."""
    owners = [t for t in tets if face <= set(t)]
    if len(owners) != 2:
        return None
    a, b, c = sorted(face)
    d = [v for v in owners[0] if v not in face][0]
    e = [v for v in owners[1] if v not in face][0]
    P = points
    signs = [orient3d(P[x], P[y], P[d], P[e]) for x, y in ((a, b), (b, c), (c, a))]
    if not (all(s > 0 for s in signs) or all(s < 0 for s in signs)):  # @line L1
        return None
    return [positive(P, (x, y, d, e)) for x, y in ((a, b), (b, c), (c, a))]  # @line L2


def degree3_edges(tets: Sequence[Tet]):
    """Edges (d, e) in exactly three tetrahedra whose other vertices form a
    closed ring a, b, c; these are the interior edges of degree 3. Yields
    (edge, ring, indices of the three tetrahedra)."""
    around: Dict[Tuple[int, int], List[int]] = {}
    for k, t in enumerate(tets):
        for d, e in combinations(sorted(t), 2):
            around.setdefault((d, e), []).append(k)
    for (d, e), ks in around.items():
        if len(ks) != 3:
            continue
        links = [tuple(v for v in tets[k] if v not in (d, e)) for k in ks]
        verts = [v for l in links for v in l]
        ring = sorted(set(verts))
        if len(ring) == 3 and all(verts.count(v) == 2 for v in ring):
            yield (d, e), tuple(ring), ks


def flip32(points, edge: Tuple[int, int], ring: Tuple[int, int, int]) -> Optional[List[Tet]]:
    """The two tetrahedra abcd and abce that replace the three around the
    interior edge de of degree 3, or None if invalid. Valid iff d and e lie
    strictly on opposite sides of the plane abc."""
    d, e = edge
    a, b, c = ring
    P = points
    sd = orient3d(P[a], P[b], P[c], P[d])
    se = orient3d(P[a], P[b], P[c], P[e])
    if sd * se >= 0:  # @line L3
        return None
    return [positive(P, (a, b, c, d)), positive(P, (a, b, c, e))]  # @line L4


def improve(points, tets: Sequence[Tet], max_flips: int = 10000):
    """Hill climbing: apply a 2-3 or 3-2 flip whenever it is valid and raises
    the smallest quality of the tetrahedra it touches; stop when none does.
    Returns (tets, number of 2-3 flips, number of 3-2 flips)."""
    tets = list(tets)
    n23 = n32 = 0
    for _ in range(max_flips):  # @line L5
        done = False
        for face, ks in faces(tets).items():  # @line L6
            if len(ks) != 2:
                continue
            new = flip23(points, tets, face)  # @line L7
            if new is None:
                continue
            old_q = min(mean_ratio(points, tets[k]) for k in ks)
            if min(mean_ratio(points, t) for t in new) > old_q:  # @line L8
                tets = [t for k, t in enumerate(tets) if k not in ks] + new
                n23 += 1
                done = True
                break
        if not done:
            for edge, ring, ks in degree3_edges(tets):  # @line L9
                new = flip32(points, edge, ring)  # @line L10
                if new is None:
                    continue
                old_q = min(mean_ratio(points, tets[k]) for k in ks)
                if min(mean_ratio(points, t) for t in new) > old_q:  # @line L11
                    tets = [t for k, t in enumerate(tets) if k not in ks] + new
                    n32 += 1
                    done = True
                    break
        if not done:  # @line L12
            break
    return tets, n23, n32  # @line L13


def kuhn_cube_mesh(n: int) -> Tuple[List[Tuple[int, int, int]], List[Tet]]:
    """The n x n x n grid of unit cubes, each split into 6 tetrahedra along its
    main diagonal (the Kuhn or Freudenthal split, conforming across cubes)."""
    idx = lambda i, j, k: (k * (n + 1) + j) * (n + 1) + i
    pts = [(i, j, k) for k in range(n + 1) for j in range(n + 1) for i in range(n + 1)]
    tets = []
    for k in range(n):
        for j in range(n):
            for i in range(n):
                for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
                    cur = [i, j, k]
                    path = [idx(*cur)]
                    for axis in perm:
                        cur[axis] += 1
                        path.append(idx(*cur))
                    tets.append(positive(pts, path))
    return pts, tets
