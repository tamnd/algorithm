# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radial-edge-data-structure/. The authors are listed in prov/X79HMJ.jsonl.

import random
import unittest
from fractions import Fraction

from radial_edge_data_structure import RadialEdge, RadialEdgeError

CUBE_FACES = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]


def box_points(x0, y0, z0, s=1):
    return [(x0, y0, z0), (x0 + s, y0, z0), (x0 + s, y0 + s, z0), (x0, y0 + s, z0),
            (x0, y0, z0 + s), (x0 + s, y0, z0 + s), (x0 + s, y0 + s, z0 + s), (x0, y0 + s, z0 + s)]


def two_boxes(second, merge):
    """Two unit cubes; vertices of the second cube that equal a vertex of the first are merged."""
    pts = box_points(0, 0, 0)
    ids = []
    for p in box_points(*second):
        if merge and p in pts:
            ids.append(pts.index(p))
        else:
            ids.append(len(pts))
            pts.append(p)
    faces = [list(f) for f in CUBE_FACES] + [[ids[v] for v in f] for f in CUBE_FACES]
    return pts, faces


# ----- the brute force: face lists, scans and a sort by an exact pseudo-angle -----

def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def area_normal(points, verts):
    n = (0, 0, 0)
    for i in range(len(verts)):
        a, b, c = points[verts[0]], points[verts[i - 1]], points[verts[i]]
        t = cross(sub(b, a), sub(c, a))
        n = tuple(x + y for x, y in zip(n, t))
    return n


def pseudo_angle(x, y):
    """A strictly increasing function of the angle of (x, y) in [0, 4), exact."""
    if y >= 0:
        return Fraction(y, x + y) if x >= 0 else 1 + Fraction(-x, -x + y)
    return 2 + Fraction(-y, -x - y) if x < 0 else 3 + Fraction(x, x - y)


def scan_radial(points, faces, u, v):
    """The faces that have the side {u, v}, sorted counterclockwise about v - u."""
    d = sub(points[v], points[u])
    axis = next(a for a in ((1, 0, 0), (0, 1, 0), (0, 0, 1)) if cross(d, a) != (0, 0, 0))
    b1 = cross(d, axis)
    b2 = cross(d, b1)
    out = []
    for f, c in enumerate(faces):
        k = len(c)
        for i in range(k):
            p, q = c[i], c[(i + 1) % k]
            if {p, q} == {u, v}:
                w = cross(area_normal(points, c), sub(points[q], points[p]))
                out.append((pseudo_angle(dot(w, b1), dot(w, b2)), f))
    return [f for _, f in sorted(out)]


def rotation(cyc, start):
    i = cyc.index(start)
    return cyc[i:] + cyc[:i]


def compare(test, rs, points, faces, wires):
    rs.check()
    pairs = {frozenset((c[i], c[(i + 1) % len(c)])) for c in faces for i in range(len(c))}
    pairs |= {frozenset(w) for w in wires}
    test.assertEqual(len(rs.edges), len(pairs))
    for pair in pairs:
        u, v = sorted(pair)
        e = rs.edge(u, v)
        a, b = rs.edge_vertices(e)
        want = scan_radial(points, faces, a, b)
        got = rs.radial_faces(e)
        test.assertEqual(sorted(got), sorted(want))
        if want:
            test.assertEqual(rotation(got, want[0]), want)
        test.assertEqual(rs.is_wire(e), frozenset((u, v)) in {frozenset(w) for w in wires})
    for f, c in enumerate(faces):
        test.assertEqual(rotation(rs.face_vertices(f), c[0]), c)
        test.assertEqual(sorted(rs.face_edges(f)), sorted(rs.edge(c[i], c[(i + 1) % len(c)]) for i in range(len(c))))
    for v in range(len(points)):
        test.assertEqual(rs.vertex_faces(v), [f for f, c in enumerate(faces) if v in c])
        test.assertEqual(rs.vertex_edges(v), sorted(rs.edge(*sorted(p)) for p in pairs if v in p))


def build(points, faces, wires=(), order=None):
    rs = RadialEdge(points)
    for w in wires:
        rs.add_wire(*w)
    ids = {}
    for f in order if order is not None else range(len(faces)):
        ids[f] = rs.add_face(faces[f])
    return rs, ids


# ----- voxel complexes and a grid walk for the shells -----

AXES = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]  # (a, b, c) with e_b x e_c = e_a


def voxel_faces(filled, n):
    """The boundary squares of a set of unit cells in an n by n by n grid, each
    counterclockwise seen from the empty side. Returns (points, faces, sides),
    where sides[f] = (filled cell, empty cell)."""
    vid = {}
    points = []

    def pt(p):
        if p not in vid:
            vid[p] = len(points)
            points.append(p)
        return vid[p]

    faces, sides = [], []
    for cell in sorted(filled):
        for a, b, c in AXES:
            for s in (1, -1):
                nb = list(cell)
                nb[a] += s
                nb = tuple(nb)
                if nb in filled:
                    continue
                corners = []
                for db, dc in ((0, 0), (1, 0), (1, 1), (0, 1)):
                    p = [0, 0, 0]
                    p[a] = cell[a] + (1 if s > 0 else 0)
                    p[b], p[c] = cell[b] + db, cell[c] + dc
                    corners.append(pt(tuple(p)))
                if s < 0:
                    corners.reverse()
                faces.append(corners)
                sides.append((cell, nb))
    return points, faces, sides


def grid_shells(points, faces, sides, filled):
    """The faceuses joined across edges, found by walking the cells around each edge."""
    face_of = {}
    for f, (inn, out) in enumerate(sides):
        face_of[(inn, out)] = f
        face_of[(out, inn)] = f
    parent = {(f, s): (f, s) for f in range(len(faces)) for s in (1, -1)}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for f, c in enumerate(faces):
        inn, out = sides[f]
        for i in range(4):
            p, q = points[c[i]], points[c[(i + 1) % 4]]
            a = next(j for j in range(3) if p[j] != q[j])
            b, cc = [j for j in range(3) if j != a]
            lo = min(p[a], q[a])
            ring = []
            for db, dc in ((-1, -1), (0, -1), (0, 0), (-1, 0)):
                cell = [0, 0, 0]
                cell[a], cell[b], cell[cc] = lo, p[b] + db, p[cc] + dc
                ring.append(tuple(cell))
            for side, start, other in ((1, out, inn), (-1, inn, out)):
                k = ring.index(start)
                step = 1 if ring[(k - 1) % 4] == other else -1
                cur = start
                while True:
                    nxt = ring[(ring.index(cur) + step) % 4]
                    if (nxt in filled) != (cur in filled):
                        break
                    cur = nxt
                g = face_of[(cur, nxt)]
                gside = -1 if cur in filled else 1
                parent[find((f, side))] = find((g, gside))
    groups = {}
    for x in parent:
        groups.setdefault(find(x), set()).add(x)
    return sorted(sorted(s) for s in groups.values())


def normalize(shells, ids=None):
    back = {v: k for k, v in ids.items()} if ids else None
    out = []
    for s in shells:
        out.append(sorted((back[f] if back else f, side) for f, side in s))
    return sorted(out)


class RadialEdgeTests(unittest.TestCase):
    def test_cube(self):
        pts = box_points(0, 0, 0)
        rs, _ = build(pts, CUBE_FACES)
        compare(self, rs, pts, CUBE_FACES, [])
        e = rs.edge(0, 3)
        self.assertEqual(rs.radial_faces(e), [0, 5])
        shells = normalize(rs.shells())
        self.assertEqual(shells, [[(f, -1) for f in range(6)], [(f, 1) for f in range(6)]])

    def test_two_cubes_on_an_edge(self):
        pts, faces = two_boxes((1, 1, 0), merge=True)  # they share the edge from (1,1,0) to (1,1,1)
        rs, _ = build(pts, faces)
        compare(self, rs, pts, faces, [])
        e = rs.edge(2, 6)
        self.assertEqual(len(rs.radial_faces(e)), 4)
        self.assertEqual(len(rs.shells()), 3)  # outside, and the inside of each cube

    def test_two_cubes_at_a_vertex(self):
        pts, faces = two_boxes((1, 1, 1), merge=True)  # they share the vertex (1,1,1)
        rs, _ = build(pts, faces)
        compare(self, rs, pts, faces, [])
        self.assertEqual(len(rs.vertex_faces(6)), 6)
        self.assertEqual(len(rs.shells()), 4)  # the outside is joined only through a vertex

    def test_sheets_book_and_wire(self):
        pts = [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 0, 1), (-1, 1, 0), (-1, 1, 1), (0, -1, 0), (0, -1, 1), (3, 3, 3)]
        book = [[0, 2, 3, 1], [1, 5, 4, 0], [0, 6, 7, 1]]  # three pages on the spine 0-1
        rs, _ = build(pts, book, wires=[(3, 8)])
        compare(self, rs, pts, book, [(3, 8)])
        spine = rs.edge(0, 1)
        # page 0 uses the spine from 1 to 0 first, so the edge runs down, along -z
        self.assertEqual(rs.edge_vertices(spine), (1, 0))
        # the pages are at 0, 135 and 270 degrees about +z, so at 0, 90 and 225 about -z
        self.assertEqual(rotation(rs.radial_faces(spine), 0), [0, 2, 1])
        self.assertEqual(len(rs.shells()), 1)  # free edges join the two sides of each page
        self.assertTrue(rs.is_wire(rs.edge(3, 8)))
        self.assertEqual(rs.vertex_faces(8), [])

    def test_bad_input(self):
        pts = box_points(0, 0, 0) + [(0, 5, 5)]
        rs = RadialEdge(pts)
        rs.add_face([0, 1, 2, 3])
        with self.assertRaises(RadialEdgeError):
            rs.add_face([0, 1, 2, 3])  # the same half-planes again
        with self.assertRaises(RadialEdgeError):
            rs.add_face([0, 1, 5, 8])  # not planar
        with self.assertRaises(RadialEdgeError):
            rs.add_face([0, 4, 0])
        rs.add_wire(4, 8)
        with self.assertRaises(RadialEdgeError):
            rs.add_face([4, 8, 7])  # a face on a wire edge
        with self.assertRaises(RadialEdgeError):
            rs.add_wire(0, 1)  # the edge has a face
        rs.check()
        self.assertEqual(len(rs.faces), 1)

    def test_voxel_complexes(self):
        rng = random.Random(1986)
        n = 3
        cells = [(i, j, k) for i in range(n) for j in range(n) for k in range(n)]
        seen_four = 0
        for trial in range(60):
            filled = {c for c in cells if rng.random() < 0.45}
            if not filled:
                continue
            points, faces, sides = voxel_faces(filled, n)
            order = list(range(len(faces)))
            rng.shuffle(order)
            rot = [rng.randrange(4) for _ in faces]
            faces = [c[r:] + c[:r] for c, r in zip(faces, rot)]
            rs, ids = build(points, faces, order=order)
            # the structure numbers faces in insertion order; renumber the brute force to match
            back = [None] * len(faces)
            for f, fid in ids.items():
                back[fid] = faces[f]
            compare(self, rs, points, back, [])
            self.assertEqual(normalize(rs.shells(), ids), grid_shells(points, faces, sides, filled))
            seen_four += sum(1 for e in range(len(rs.edges)) if len(rs.radial_faces(e)) == 4)
        self.assertGreater(seen_four, 20)


if __name__ == "__main__":
    unittest.main()
