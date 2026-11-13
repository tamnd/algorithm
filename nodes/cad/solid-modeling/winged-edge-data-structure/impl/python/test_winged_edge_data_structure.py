# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winged-edge-data-structure/. The authors are listed in prov/4Q9BTY.jsonl.

import random
import unittest

from winged_edge_data_structure import WingedEdge, WingedEdgeError

CUBE = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
# vertices 0..3 at z = 0: (0,0), (1,0), (1,1), (0,1); 4..7 above them at z = 1
OCTAHEDRON = [[0, 2, 4], [2, 1, 4], [1, 3, 4], [3, 0, 4], [2, 0, 5], [1, 2, 5], [3, 1, 5], [0, 3, 5]]
# 0 = +x, 1 = -x, 2 = +y, 3 = -y, 4 = +z, 5 = -z


def torus(p, q):
    """A p by q grid of quads on a torus, oriented one way."""
    vid = lambda i, j: (i % p) * q + (j % q)
    return p * q, [[vid(i, j), vid(i + 1, j), vid(i + 1, j + 1), vid(i, j + 1)] for i in range(p) for j in range(q)]


def rotation(cyc, start):
    i = cyc.index(start)
    return cyc[i:] + cyc[:i]


class FaceList:
    """The brute force: faces as lists of vertex ids, and every query a scan."""

    def __init__(self, n, faces):
        self.n = n
        self.faces = {f: list(c) for f, c in enumerate(faces)}

    def edge_faces(self, u, v):
        left = [f for f, c in self.faces.items() if any(c[i] == u and c[(i + 1) % len(c)] == v for i in range(len(c)))]
        right = [f for f, c in self.faces.items() if any(c[i] == v and c[(i + 1) % len(c)] == u for i in range(len(c)))]
        assert len(left) == 1 and len(right) == 1
        return left[0], right[0]

    def ring(self, v):
        """The neighbours of v in counterclockwise order: from the edge v -> n
        of a face (..., p, v, n, ...), the next edge counterclockwise is v -> p."""
        step = {}
        for c in self.faces.values():
            k = len(c)
            for i in range(k):
                if c[i] == v:
                    step[c[(i + 1) % k]] = c[i - 1]
        start = next(iter(step))
        out = [start]
        x = step[start]
        while x != start:
            out.append(x)
            x = step[x]
        assert len(out) == len(step)
        return out

    def split_edge(self, u, v, m):
        for f, c in self.faces.items():
            k = len(c)
            for i in range(k):
                if {c[i], c[(i + 1) % k]} == {u, v}:
                    c.insert(i + 1, m)
                    break
        self.n += 1

    def split_face(self, f, u, w, g):
        c = rotation(self.faces[f], u)
        j = c.index(w)
        self.faces[g] = c[: j + 1]
        self.faces[f] = [u] + c[j:]

    def join_faces(self, u, w):
        f, g = self.edge_faces(u, w)
        cf = rotation(self.faces[f], w)  # w, ..., u
        cg = rotation(self.faces[g], u)  # u, ..., w
        self.faces[f] = cf + cg[1:-1]
        del self.faces[g]
        return g


def compare(test, we, fl):
    we.check()
    test.assertEqual(sorted(we.faces()), sorted(fl.faces))
    for f, c in fl.faces.items():
        got = we.face_vertices(f)
        test.assertEqual(rotation(got, c[0]), c)
    for v in range(fl.n):
        want = fl.ring(v)
        got = we.neighbors(v)
        test.assertEqual(rotation(got, want[0]), want)
        faces = we.vertex_faces(v)
        test.assertEqual(len(faces), len(want))
        for x, f in zip(we.neighbors(v), faces):
            test.assertEqual(fl.edge_faces(v, x)[0], f)
    edges = we.edges()
    for e in edges:
        u, v = we.edge_vertices(e)
        test.assertEqual(we.edge_faces(e), fl.edge_faces(u, v))
    pairs = {frozenset((c[i], c[(i + 1) % len(c)])) for c in fl.faces.values() for i in range(len(c))}
    test.assertEqual(len(pairs), len(edges))
    return len(fl.n * [0]) - len(edges) + len(fl.faces)


class WingedEdgeTests(unittest.TestCase):
    def test_cube(self):
        we = WingedEdge(8, CUBE)
        chi = compare(self, we, FaceList(8, CUBE))
        self.assertEqual(chi, 2)
        e = next(e for e in we.edges() if we.edge_vertices(e) == (0, 3))
        self.assertEqual(we.edge_faces(e), (0, 5))
        # seen from outside, at the corner (0, 0, 0): +y, then +x, then +z, counterclockwise
        self.assertEqual(rotation(we.neighbors(0), 3), [3, 1, 4])
        self.assertEqual(rotation(we.face_vertices(0), 0), [0, 3, 2, 1])

    def test_octahedron_and_torus(self):
        compare(self, WingedEdge(6, OCTAHEDRON), FaceList(6, OCTAHEDRON))
        n, faces = torus(4, 5)
        chi = compare(self, WingedEdge(n, faces), FaceList(n, faces))
        self.assertEqual(chi, 0)

    def test_bad_input(self):
        with self.assertRaises(WingedEdgeError):
            WingedEdge(8, CUBE[:-1])  # open surface
        with self.assertRaises(WingedEdgeError):
            WingedEdge(8, [CUBE[0][::-1]] + CUBE[1:])  # one face reversed
        with self.assertRaises(WingedEdgeError):
            WingedEdge(8, CUBE + [[0, 1, 2]])  # an edge on three faces
        two_tetrahedra = [[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3], [0, 5, 4], [0, 4, 6], [0, 6, 5], [4, 5, 6]]
        WingedEdge(4, two_tetrahedra[:4]).check()
        with self.assertRaises(WingedEdgeError):
            WingedEdge(7, two_tetrahedra)  # vertex 0 has two fans

    def test_random_updates(self):
        rng = random.Random(4171975)
        ops = {"split_edge": 0, "split_face": 0, "join_faces": 0}
        for start in range(6):
            if start % 3 == 0:
                n, faces = 8, CUBE
            elif start % 3 == 1:
                n, faces = 6, OCTAHEDRON
            else:
                n, faces = torus(3, 4)
            we, fl = WingedEdge(n, faces), FaceList(n, faces)
            chi0 = compare(self, we, fl)
            for step in range(60):
                r = rng.random()
                if r < 0.35:
                    e = rng.choice(we.edges())
                    u, v = we.edge_vertices(e)
                    m = we.split_edge(e)
                    fl.split_edge(u, v, m)
                    ops["split_edge"] += 1
                elif r < 0.7:
                    f = rng.choice(we.faces())
                    c = fl.faces[f]
                    if len(c) < 4:
                        continue
                    i = rng.randrange(len(c))
                    j = (i + rng.randrange(2, len(c) - 1)) % len(c)
                    try:
                        n_edge, g = we.split_face(f, c[i], c[j])
                    except WingedEdgeError:
                        continue  # the two vertices already have an edge
                    fl.split_face(f, c[i], c[j], g)
                    ops["split_face"] += 1
                else:
                    e = rng.choice(we.edges())
                    u, w = we.edge_vertices(e)
                    try:
                        g = we.join_faces(e)
                    except WingedEdgeError:
                        continue
                    self.assertEqual(fl.join_faces(u, w), g)
                    ops["join_faces"] += 1
                self.assertEqual(compare(self, we, fl), chi0)
        self.assertTrue(all(c > 40 for c in ops.values()), ops)

    def test_split_face_errors(self):
        we = WingedEdge(8, CUBE)
        with self.assertRaises(WingedEdgeError):
            we.split_face(0, 0, 3)  # next to each other
        with self.assertRaises(WingedEdgeError):
            we.split_face(0, 0, 5)  # 5 is not on face 0


if __name__ == "__main__":
    unittest.main()
