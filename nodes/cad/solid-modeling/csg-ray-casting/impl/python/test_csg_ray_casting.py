# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/csg-ray-casting/. The authors are listed in prov/K0WQSY.jsonl.

import random
import unittest
from fractions import Fraction

from csg_ray_casting import box, cast, first_hit, merge

F = Fraction


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def is_node(t):
    return isinstance(t, tuple) and len(t) == 3 and isinstance(t[0], str)


def leaves(tree):
    return leaves(tree[1]) + leaves(tree[2]) if is_node(tree) else [tree]


def member(x, tree):
    """Point membership of the plain formula, with closed primitives."""
    if not is_node(tree):
        return all(dot(a, x) <= b for a, b in tree)
    op, l, r = tree
    p, q = member(x, l), member(x, r)
    return {"union": p or q, "intersection": p and q, "difference": p and not q}[op]


def brute_intervals(o, d, tree):
    """Classify the midpoints between all plane crossings by 3D point membership."""
    ts = set()
    for prim in leaves(tree):
        for a, b in prim:
            s = dot(a, d)
            if s != 0:
                ts.add(F(b - dot(a, o)) / s)
    ts = sorted(ts)
    out = []
    for t0, t1 in zip(ts, ts[1:]):
        m = (t0 + t1) / 2
        x = tuple(o[i] + m * d[i] for i in range(3))
        if member(x, tree):
            if out and out[-1][1] == t0:
                out[-1] = (out[-1][0], t1)
            else:
                out.append((t0, t1))
    return out


def in_a_face_plane(o, d, tree):
    return any(dot(a, d) == 0 and dot(a, o) == b for prim in leaves(tree) for a, b in prim)


def random_primitive(rng):
    lo = [rng.randint(0, 3) for _ in range(3)]
    hi = [x + rng.randint(1, 3) for x in lo]
    prim = box(lo[0], lo[1], lo[2], hi[0], hi[1], hi[2])
    center = [F(lo[i] + hi[i], 2) for i in range(3)]
    for _ in range(rng.randint(0, 2)):
        a = tuple(rng.randint(-2, 2) for _ in range(3))
        if a != (0, 0, 0):
            prim.append((a, dot(a, center) + rng.randint(0, 2)))  # a cut that keeps the center
    return prim


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        return random_primitive(rng)
    op = rng.choice(["union", "union", "intersection", "difference"])
    return (op, random_tree(rng, depth - 1), random_tree(rng, depth - 1))


A = box(0, 0, 0, 1, 1, 1)
B = box(1, 0, 0, 2, 1, 1)
C = box(F(3, 2), F(1, 4), F(1, 4), F(5, 2), F(3, 4), F(3, 4))
O, D = (-1, F(1, 2), F(1, 2)), (1, 0, 0)


class TestCsgRayCasting(unittest.TestCase):
    def test_worked_example(self):
        self.assertEqual(cast(O, D, A), [(1, 2)])
        self.assertEqual(cast(O, D, B), [(2, 3)])
        self.assertEqual(cast(O, D, ("union", A, B)), [(1, 3)])
        self.assertEqual(cast(O, D, C), [(F(5, 2), F(7, 2))])
        tree = ("difference", ("union", A, B), C)
        self.assertEqual(cast(O, D, tree), [(1, F(5, 2))])
        self.assertEqual(first_hit(O, D, tree), 1)

    def test_touching_and_grazing(self):
        self.assertEqual(cast(O, D, ("intersection", A, B)), [])
        self.assertEqual(cast((1, -1, F(1, 2)), (-1, 1, 0), A), [])  # touches only the edge x = y = 0
        self.assertEqual(merge([(0, 1)], [(1, 2)], "union"), [(0, 2)])
        self.assertEqual(merge([(0, 3)], [(1, 2)], "difference"), [(0, 1), (2, 3)])
        self.assertEqual(merge([(0, 2)], [(0, 2)], "difference"), [])

    def test_first_hit_inside_and_miss(self):
        self.assertEqual(first_hit((F(1, 2), F(1, 2), F(1, 2)), (1, 0, 0), A), 0)
        self.assertIsNone(first_hit((-1, 5, 5), (1, 0, 0), A))
        self.assertIsNone(first_hit((3, F(1, 2), F(1, 2)), (1, 0, 0), A))

    def test_random_against_point_membership(self):
        rng = random.Random(1982)
        done = hits = 0
        while done < 600 or hits < 300:
            tree = random_tree(rng, 3)
            o = tuple(F(rng.randint(-8, 16), 2) for _ in range(3))
            aim = tuple(F(rng.randint(1, 11), 2) for _ in range(3))  # aim into the scene
            d = tuple(int(2 * (aim[i] - o[i])) for i in range(3))
            if d == (0, 0, 0) or in_a_face_plane(o, d, tree):
                continue
            expect = brute_intervals(o, d, tree)
            self.assertEqual(cast(o, d, tree), expect)
            hit = next((max(t0, F(0)) for t0, t1 in expect if t1 >= 0), None)
            self.assertEqual(first_hit(o, d, tree), hit)
            done += 1
            hits += bool(expect)


if __name__ == "__main__":
    unittest.main()
