# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marching-cubes/. The authors are listed in prov/N004FS.jsonl.

"""Marching cubes: a triangle mesh of the level set f = c of a 3D sample grid.

The field is field[z][y][x]. A sample is inside when it is less than c and
outside when it is at least c. Each cell (a cube of 8 samples) gets an 8-bit
case number, and a 256-entry table gives its triangles as triples of cube
edges. The table is built once, at import, from a rule on the six faces of the
cube: on a face whose two inside corners are diagonal (an ambiguous face),
the two inside corners are kept apart. The rule reads only the four signs of
the face, so two cells that share a face cut it the same way, and the mesh has
no holes. The original table of Lorensen and Cline does not have this property.
"""

from fractions import Fraction
from typing import Union

Number = Union[int, float, Fraction]
Vec = tuple[Number, Number, Number]

# Corner k of a cell is at offset (k & 1, (k >> 1) & 1, (k >> 2) & 1).
CORNERS = [(k & 1, (k >> 1) & 1, (k >> 2) & 1) for k in range(8)]
# The 12 edges: pairs of corners that differ in one coordinate.
EDGES = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count("1") == 1]
EDGE_ID = {e: i for i, e in enumerate(EDGES)}
# Axis of each edge: 0 for x, 1 for y, 2 for z.
EDGE_AXIS = [(a ^ b).bit_length() - 1 for a, b in EDGES]


def _faces() -> list[list[int]]:
    """The 6 faces, each as 4 corners in counterclockwise order seen from outside the cube."""
    out = []
    for d in range(3):
        d1, d2 = (d + 1) % 3, (d + 2) % 3
        for s in (0, 1):
            ring = []
            for u, v in ((0, 0), (1, 0), (1, 1), (0, 1)):
                bits = [0, 0, 0]
                bits[d], bits[d1], bits[d2] = s, u, v
                ring.append(bits[0] | bits[1] << 1 | bits[2] << 2)
            out.append(ring if s == 1 else ring[::-1])
    return out


FACES = _faces()

# Square table on one face, as in marching squares: face edge e joins ring
# corners e and e + 1. Segments are oriented with the inside on the left, seen
# from outside. The ambiguous cases 5 and 10 keep the inside corners apart.
_SQUARE = {
    0: (), 1: ((0, 3),), 2: ((1, 0),), 3: ((1, 3),), 4: ((2, 1),),
    5: ((0, 3), (2, 1)), 6: ((2, 0),), 7: ((2, 3),), 8: ((3, 2),),
    9: ((0, 2),), 10: ((1, 0), (3, 2)), 11: ((1, 2),), 12: ((3, 1),),
    13: ((0, 1),), 14: ((3, 0),), 15: (),
}


def face_segments(case: int, ring: list[int]) -> list[tuple[int, int]]:
    """Directed segments (cube edge, cube edge) that cut one face for a cell case."""
    sq = sum(1 << k for k in range(4) if case >> ring[k] & 1)
    out = []
    for ea, eb in _SQUARE[sq]:
        a = EDGE_ID[tuple(sorted((ring[ea], ring[(ea + 1) % 4])))]
        b = EDGE_ID[tuple(sorted((ring[eb], ring[(eb + 1) % 4])))]
        out.append((a, b))
    return out


def _same_face(e1: int, e2: int) -> bool:
    """Do two cube edges lie on one face? Then a chord between them lies on that face."""
    pts = EDGES[e1] + EDGES[e2]
    return any(len({p >> d & 1 for p in pts}) == 1 for d in range(3))


def _triangulate(cyc: list[int]) -> list[tuple[int, int, int]]:
    """Triangulate a cycle of cube edges with no chord on a cube face.

    A chord on a face would also be a chord of the neighbor cell, and the edge
    would then have four triangles. The search is over the ear at the first
    and last vertex, with an explicit stack; it fails only if no triangulation
    exists, which the table build checks.
    """
    n = len(cyc)

    def ok(i: int, j: int) -> bool:
        return (j - i) % n in (1, n - 1) or not _same_face(cyc[i], cyc[j])

    # solve(i, j): a list of triangles for the polygon cyc[i..j], or None
    memo: dict[tuple[int, int], list[tuple[int, int, int]] | None] = {}
    for i, j in [(i, i + d) for d in range(1, n) for i in range(n - d)]:
        if j - i < 2:
            memo[(i, j)] = []
            continue
        memo[(i, j)] = None
        if not ok(i, j):
            continue
        for k in range(i + 1, j):
            left, right = memo[(i, k)], memo[(k, j)]
            if left is not None and right is not None and ok(i, k) and ok(k, j):
                memo[(i, j)] = left + [(i, k, j)] + right
                break
    tris = memo[(0, n - 1)]
    if tris is None:
        raise ValueError("no triangulation without face chords")
    return [(cyc[a], cyc[b], cyc[c]) for a, b, c in tris]


def _build_table() -> list[list[tuple[int, int, int]]]:
    table = []
    for case in range(256):  # @line L1
        nxt: dict[int, int] = {}
        for ring in FACES:  # @line L2
            for a, b in face_segments(case, ring):
                nxt[a] = b
        tris = []
        seen: set[int] = set()
        for start in sorted(nxt):
            if start in seen:
                continue
            cyc = [start]
            seen.add(start)
            e = nxt[start]
            while e != start:  # @line L3
                cyc.append(e)
                seen.add(e)
                e = nxt[e]
            # The face segments run counterclockwise around the inside part of the
            # cube surface, so the reversed cycle has its normal pointing to the
            # outside (toward larger values).
            tris.extend(_triangulate(cyc[::-1]))  # @line L4
        table.append(tris)
    return table


TABLE = _build_table()


def _lerp(pa: Vec, pb: Vec, fa: Number, fb: Number, c: Number) -> Vec:
    if isinstance(fa, float) or isinstance(fb, float) or isinstance(c, float):
        t: Number = (c - fa) / (fb - fa)
    else:
        t = Fraction(c - fa) / (fb - fa)
    return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]), pa[2] + t * (pb[2] - pa[2]))


def marching_cubes(field: list[list[list[Number]]], c: Number) -> tuple[list[Vec], list[tuple[int, int, int]]]:
    """Return (vertices, triangles) of the level set field = c.

    Precondition: field[z][y][x] is a box of at least 2 by 2 by 2 numbers.
    Each mesh vertex lies on one grid edge whose two samples are on different sides
    of c, at the point of linear interpolation; neighboring cells share it. Triangles
    are oriented with the normal toward the outside (values at least c). When every
    sample on the border of the box is outside, the mesh is a closed, oriented
    2-manifold. Cost: O(X Y Z) time for an X by Y by Z grid.
    """
    nz, ny, nx = len(field), len(field[0]), len(field[0][0])
    verts: list[Vec] = []  # @line L5
    index: dict[tuple[int, int, int, int], int] = {}
    tris: list[tuple[int, int, int]] = []

    def vertex(x: int, y: int, z: int, e: int) -> int:
        a, b = EDGES[e]
        ax, ay, az = CORNERS[a]
        key = (x + ax, y + ay, z + az, EDGE_AXIS[e])  # @line L9
        k = index.get(key)
        if k is None:  # @line L10
            bx, by, bz = CORNERS[b]
            pa = (x + ax, y + ay, z + az)
            pb = (x + bx, y + by, z + bz)
            fa = field[pa[2]][pa[1]][pa[0]]
            fb = field[pb[2]][pb[1]][pb[0]]
            k = len(verts)
            verts.append(_lerp(pa, pb, fa, fb, c))  # @line L11
            index[key] = k
        return k

    for z in range(nz - 1):  # @line L6
        for y in range(ny - 1):
            for x in range(nx - 1):
                case = 0
                for k, (dx, dy, dz) in enumerate(CORNERS):
                    if field[z + dz][y + dy][x + dx] < c:
                        case |= 1 << k  # @line L7
                for t in TABLE[case]:  # @line L8
                    tris.append((vertex(x, y, z, t[0]), vertex(x, y, z, t[1]), vertex(x, y, z, t[2])))  # @line L12
    return verts, tris  # @line L13
