# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brep-reconstruction-from-scans/. The authors are listed in prov/RBGNXS.jsonl.

"""B-rep reconstruction of a polyhedral part from a segmented scan.

The input is a list of regions of 3D points, one region per face, as a
segmentation gives them. Each region is fitted by a plane; two faces are
adjacent when some of their points are close; adjacent faces meet in an edge
on the line where their planes meet; three faces that are pairwise adjacent
meet in a vertex where their planes meet, if the data come close to that
point. Edges are the segments between the vertices of their two faces, and
the edges of a face form its boundary loop. The result is checked with the
Euler formula V - E + F = 2 for a closed solid without holes.

Only planar faces with sharp edges are handled here: no curved faces, no
blends, and no faces with inner loops.
"""

from itertools import combinations
from math import sqrt
from typing import Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

from re1lin import cross, dot, jacobi_eigen, norm, solve, sub

Vec3 = Tuple[float, float, float]
Plane = Tuple[Vec3, float]          # unit normal n and offset c of the plane n . x = c


def fit_plane(points: Sequence[Vec3]) -> Plane:
    """Least-squares plane (orthogonal distance): the centroid and the eigenvector of the smallest eigenvalue."""
    if len(points) < 3:
        raise ValueError("a plane needs at least three points")
    m = len(points)
    c = tuple(sum(p[k] for p in points) / m for k in range(3))
    cov = [[sum((p[a] - c[a]) * (p[b] - c[b]) for p in points) for b in range(3)] for a in range(3)]
    values, vectors = jacobi_eigen(cov)
    n = tuple(vectors[0])
    s = norm(n)
    n = (n[0] / s, n[1] / s, n[2] / s)
    return n, dot(n, c)


def adjacent_pairs(regions: Sequence[Sequence[Vec3]], delta: float) -> Set[Tuple[int, int]]:
    """Pairs (j, k), j < k, with a point of region j within delta of a point of region k (grid hashing)."""
    grid: Dict[Tuple[int, int, int], List[Tuple[int, Vec3]]] = {}
    for j, reg in enumerate(regions):
        for p in reg:
            grid.setdefault(tuple(int(p[a] // delta) for a in range(3)), []).append((j, p))
    pairs = set()
    d2 = delta * delta
    for cell, items in grid.items():
        near = [it for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)
                for it in grid.get((cell[0] + dx, cell[1] + dy, cell[2] + dz), ())]
        for j, p in items:
            for k, q in near:
                if j < k and (j, k) not in pairs and dot(sub(p, q), sub(p, q)) <= d2:
                    pairs.add((j, k))
    return pairs


def plane_line(a: Plane, b: Plane, min_sin: float = 1e-3) -> Optional[Tuple[Vec3, Vec3]]:
    """The line where two planes meet, as (point, unit direction); None if they are nearly parallel."""
    (n1, c1), (n2, c2) = a, b
    d = cross(n1, n2)
    s = norm(d)
    if s < min_sin:
        return None
    u, v = cross(n2, d), cross(d, n1)
    x0 = tuple((c1 * u[k] + c2 * v[k]) / (s * s) for k in range(3))
    return x0, (d[0] / s, d[1] / s, d[2] / s)


def plane_vertex(a: Plane, b: Plane, c: Plane, min_det: float = 1e-6) -> Optional[Vec3]:
    """The point where three planes meet; None if their normals are nearly dependent."""
    if abs(dot(a[0], cross(b[0], c[0]))) < min_det:
        return None
    x = solve([list(a[0]), list(b[0]), list(c[0])], [a[1], b[1], c[1]])
    return tuple(x)


def _near(points: Sequence[Vec3], v: Vec3, eta: float) -> bool:
    e2 = eta * eta
    return any(dot(sub(p, v), sub(p, v)) <= e2 for p in points)


class BRep:
    """Faces (planes), vertices (points with their faces), edges (vertex pairs with their two faces) and loops."""

    def __init__(self):
        self.planes: List[Plane] = []
        self.adjacency: Set[Tuple[int, int]] = set()
        self.vertices: List[Vec3] = []
        self.vertex_faces: List[FrozenSet[int]] = []
        self.edges: List[Tuple[int, int, Tuple[int, int]]] = []     # (vertex a, vertex b, (face j, face k))
        self.loops: Dict[int, List[int]] = {}

    def euler(self) -> int:
        return len(self.vertices) - len(self.edges) + len(self.planes)


def reconstruct(regions: Sequence[Sequence[Vec3]], delta: float, eta: float) -> BRep:
    """Build a B-rep from segmented points, one region per planar face.

    delta: largest gap between points of two adjacent faces; eta: largest
    distance from a vertex to the points of its faces, and the merge distance
    of vertices. Precondition: every region has at least three points that do
    not lie on one line. Cost: Theta(m) expected for the adjacency on m points
    of bounded density, plus Theta(T m) for the T triangles of the adjacency
    graph, plus Theta(F^3) to list them.
    """
    B = BRep()
    B.planes = [fit_plane(reg) for reg in regions]                              # @line L1
    B.adjacency = adjacent_pairs(regions, delta)                                # @line L2
    lines = {pair: plane_line(B.planes[pair[0]], B.planes[pair[1]]) for pair in B.adjacency}  # @line L3
    found: List[Tuple[Vec3, Set[int]]] = []
    for j, k, l in combinations(range(len(regions)), 3):
        if (j, k) in B.adjacency and (j, l) in B.adjacency and (k, l) in B.adjacency:
            v = plane_vertex(B.planes[j], B.planes[k], B.planes[l])            # @line L4
            if v is None or not all(_near(regions[f], v, eta) for f in (j, k, l)):
                continue
            for w in found:                                                     # @line L5
                if norm(sub(w[0], v)) <= eta:
                    w[1].update((j, k, l))
                    break
            else:
                found.append((v, {j, k, l}))
    B.vertices = [v for v, _ in found]
    B.vertex_faces = [frozenset(fs) for _, fs in found]
    for (j, k) in sorted(B.adjacency):
        line = lines[(j, k)]
        on = [i for i, fs in enumerate(B.vertex_faces) if j in fs and k in fs]
        if line is None or len(on) < 2:
            continue
        on.sort(key=lambda i: dot(sub(B.vertices[i], line[0]), line[1]))
        for a in range(0, len(on) - 1, 2):                                      # @line L6
            B.edges.append((on[a], on[a + 1], (j, k)))
    for f in range(len(regions)):
        B.loops[f] = face_loop(B, f)                                            # @line L7
    return B                                                                    # @line L8


def face_loop(B: BRep, f: int) -> List[int]:
    """The vertices of face f in the order of its boundary cycle; [] if its edges do not form one cycle."""
    nbr: Dict[int, List[int]] = {}
    for a, b, (j, k) in B.edges:
        if f in (j, k):
            nbr.setdefault(a, []).append(b)
            nbr.setdefault(b, []).append(a)
    if not nbr or any(len(v) != 2 for v in nbr.values()):
        return []
    start = min(nbr)
    loop, prev, cur = [start], None, start
    while True:
        nxt = nbr[cur][0] if nbr[cur][0] != prev else nbr[cur][1]
        if nxt == start:
            break
        loop.append(nxt)
        prev, cur = cur, nxt
    return loop if len(loop) == len(nbr) else []
