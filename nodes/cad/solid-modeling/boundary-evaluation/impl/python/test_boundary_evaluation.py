# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-evaluation/. The authors are listed in prov/G7ANN6.jsonl.

import random
import unittest
from collections import Counter
from fractions import Fraction

from boundary_evaluation import box, boundary_evaluation, volume

F = Fraction


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def is_node(t):
    return isinstance(t, tuple) and len(t) == 3 and isinstance(t[0], str)


# ---- brute force: inclusion and exclusion over convex intersections ----

def clip(poly, a, b):
    """Keep the part of a convex polygon with a . x <= b (Sutherland and Hodgman)."""
    out = []
    for k in range(len(poly)):
        p, q = poly[k], poly[(k + 1) % len(poly)]
        vp, vq = dot(a, p) - b, dot(a, q) - b
        if vp <= 0:
            out.append(p)
        if (vp < 0 < vq) or (vq < 0 < vp):
            t = F(vp) / (vp - vq)
            out.append(tuple(p[i] + t * (q[i] - p[i]) for i in range(3)))
    return out


def convex_volume(halfspaces, R=1000):
    """Volume of {x : a . x <= b for all (a, b)}: clip a large square in each plane, then sum tetrahedra."""
    six_v = F(0)
    for i, (a, b) in enumerate(halfspaces):
        e = (1, 0, 0) if a[1] != 0 or a[2] != 0 else (0, 1, 0)
        u = cross(a, e)
        v = cross(a, u)
        p0 = tuple(F(b * a[k], dot(a, a)) for k in range(3))
        poly = [tuple(p0[k] + sx * R * u[k] + sy * R * v[k] for k in range(3))
                for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
        if dot(cross(u, v), a) < 0:
            poly.reverse()
        for j, (c, d) in enumerate(halfspaces):
            if j != i and poly:
                # a plane met twice is kept once: drop the copy with the larger index
                if cross(a, c) == (0, 0, 0) and dot(a, c) > 0 and b * dot(c, c) == d * dot(a, c):
                    if j < i:
                        poly = []
                    continue
                poly = clip(poly, c, d)
        for k in range(1, len(poly) - 1):
            six_v += dot(poly[0], cross(poly[k], poly[k + 1]))
    return six_v / 6


def indicator(tree, counter):
    """The indicator of the plain formula as a polynomial: {frozenset of leaves: coefficient}."""
    if not is_node(tree):
        counter[0] += 1
        return {frozenset([counter[0] - 1]): 1}
    op, l, r = tree
    p, q = indicator(l, counter), indicator(r, counter)
    pq = Counter()
    for s, x in p.items():
        for t, y in q.items():
            pq[s | t] += x * y
    res = Counter()
    if op == "union":
        res.update(p), res.update(q), res.subtract(pq)
    elif op == "intersection":
        res.update(pq)
    else:
        res.update(p), res.subtract(pq)
    return {s: x for s, x in res.items() if x}


def leaves(tree):
    return leaves(tree[1]) + leaves(tree[2]) if is_node(tree) else [tree]


def brute_volume(tree):
    prims = leaves(tree)
    poly = indicator(tree, [0])
    return sum(x * convex_volume([h for k in s for h in prims[k]]) for s, x in poly.items())


# ---- checks on the output surface ----

def area_vector_sum(faces):
    s = [0, 0, 0]
    for poly in faces:
        for k in range(len(poly)):
            c = cross(poly[k], poly[(k + 1) % len(poly)])
            for t in range(3):
                s[t] += c[t]
    return tuple(s)


def edges_cancel(faces):
    """Every directed edge, cut at the output vertices on it, has an opposite copy."""
    verts = {p for poly in faces for p in poly}
    count = Counter()
    for poly in faces:
        for k in range(len(poly)):
            p, q = poly[k], poly[(k + 1) % len(poly)]
            d = tuple(q[i] - p[i] for i in range(3))
            dd = dot(d, d)
            inner = []
            for w in verts:
                e = tuple(w[i] - p[i] for i in range(3))
                if cross(d, e) == (0, 0, 0):
                    t = F(dot(d, e)) / dd
                    if 0 < t < 1:
                        inner.append((t, w))
            chain = [p] + [w for _, w in sorted(inner)] + [q]
            for x, y in zip(chain, chain[1:]):
                count[(x, y)] += 1
    return all(count[(x, y)] == count[(y, x)] for (x, y) in count)


def random_primitive(rng):
    lo = [rng.randint(0, 2) for _ in range(3)]
    hi = [x + rng.randint(1, 3) for x in lo]
    prim = box(*lo, *hi)
    center = [F(lo[i] + hi[i], 2) for i in range(3)]
    if rng.random() < 0.5:
        a = tuple(rng.choice([-1, 1]) * rng.randint(0, 1) for _ in range(2)) + (rng.choice([-1, 1]),)
        prim.append((a, dot(a, center) + rng.randint(0, 1)))  # a cut that keeps the center
    return prim


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return random_primitive(rng)
    op = rng.choice(["union", "intersection", "difference"])
    return (op, random_tree(rng, depth - 1), random_tree(rng, depth - 1))


A = box(0, 0, 0, 2, 2, 2)
B = box(1, 1, 1, 3, 3, 3)


class TestBoundaryEvaluation(unittest.TestCase):
    def test_worked_example(self):
        for op, vol, nfaces in (("union", 15, 42), ("intersection", 1, 6), ("difference", 7, 24)):
            faces = boundary_evaluation((op, A, B))
            self.assertEqual(volume(faces), vol)
            self.assertEqual(len(faces), nfaces)
            self.assertEqual(area_vector_sum(faces), (0, 0, 0))
            self.assertTrue(edges_cancel(faces))

    def test_touching_and_coplanar(self):
        C = box(1, 0, 0, 2, 1, 1)
        D = box(0, 0, 0, 1, 1, 1)
        self.assertEqual(boundary_evaluation(("intersection", D, C)), [])
        self.assertEqual(volume(boundary_evaluation(("union", D, C))), 2)
        self.assertEqual(len(boundary_evaluation(("union", D, C))), 10)
        E = box(1, 0, 0, 2, 2, 2)  # shares three faces with A, same orientation
        self.assertEqual(volume(boundary_evaluation(("difference", A, E))), 4)
        self.assertEqual(volume(boundary_evaluation(("union", A, E))), 8)
        self.assertEqual(boundary_evaluation(("difference", E, A)), [])

    def test_random_against_inclusion_exclusion(self):
        rng = random.Random(1985)
        nonempty = 0
        for _ in range(70):
            tree = random_tree(rng, 2)
            faces = boundary_evaluation(tree)
            self.assertEqual(volume(faces), brute_volume(tree))
            self.assertEqual(area_vector_sum(faces), (0, 0, 0))
            self.assertTrue(edges_cancel(faces))
            nonempty += bool(faces)
        self.assertGreater(nonempty, 35)


if __name__ == "__main__":
    unittest.main()
