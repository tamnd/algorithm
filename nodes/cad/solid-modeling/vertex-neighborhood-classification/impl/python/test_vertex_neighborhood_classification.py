# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-neighborhood-classification/. The authors are listed in prov/QA5D08.jsonl.

import random
import unittest
from fractions import Fraction

from vertex_neighborhood_classification import area, boolean, classify, generate, winding_number

F = Fraction
OPS = {
    "union": lambda a, b: a or b,
    "intersection": lambda a, b: a and b,
    "difference": lambda a, b: a and not b,
}


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def inside(x, P):
    """Even-odd test for a point off the boundary, written apart from the module under test."""
    c = 0
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        if (a[0] > x[0]) != (b[0] > x[0]):
            y = a[1] + F(x[0] - a[0]) * (b[1] - a[1]) / (b[0] - a[0])
            c += y > x[1]
    return c % 2 == 1


def on_boundary(x, P):
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        if cross(a, b, x) == 0 and min(a[0], b[0]) <= x[0] <= max(a[0], b[0]) \
                and min(a[1], b[1]) <= x[1] <= max(a[1], b[1]):
            return True
    return False


def slice_length(x, A, B, op):
    """Length of the vertical line at x inside A op B, by the plain formula at midpoints."""
    ys = set()
    for P in (A, B):
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            if a[0] != b[0] and min(a[0], b[0]) <= x <= max(a[0], b[0]):
                ys.add(a[1] + F(x - a[0]) * (b[1] - a[1]) / (b[0] - a[0]))
    ys = sorted(ys)
    total = F(0)
    for y0, y1 in zip(ys, ys[1:]):
        m = (x, (y0 + y1) / 2)
        if OPS[op](inside(m, A), inside(m, B)):
            total += y1 - y0
    return total


def brute_area(A, B, op):
    """Area of A op B: the slice length is linear between event abscissas, so midpoints are exact."""
    xs = {p[0] for p in A + B}
    for i in range(len(A)):
        p, q = A[i], A[(i + 1) % len(A)]
        for j in range(len(B)):
            r, s = B[j], B[(j + 1) % len(B)]
            d = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
            if d != 0:
                t = F((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / d
                u = F((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / d
                if 0 <= t <= 1 and 0 <= u <= 1:
                    xs.add(p[0] + t * (q[0] - p[0]))
    xs = sorted(xs)
    return sum((x1 - x0) * slice_length((x0 + x1) / 2, A, B, op) for x0, x1 in zip(xs, xs[1:]))


DIRS = [(1, 0), (2, 1), (1, 1), (1, 2), (0, 1), (-1, 2), (-1, 1), (-2, 1),
        (-1, 0), (-2, -1), (-1, -1), (-1, -2), (0, -1), (1, -2), (1, -1), (2, -1)]  # by angle


def random_polygon(rng):
    """A star-shaped simple polygon around an integer center, counterclockwise."""
    while True:
        idx = sorted(rng.sample(range(16), rng.randint(3, 7)))
        dirs = [DIRS[i] for i in idx]
        if all(cross((0, 0), dirs[k], dirs[(k + 1) % len(dirs)]) > 0 for k in range(len(dirs))):
            break
    c = (rng.randint(2, 4), rng.randint(2, 4))
    pts = []
    for d in dirs:
        r = rng.choice([1, 1, 2]) if max(abs(d[0]), abs(d[1])) == 1 else 1
        pts.append((c[0] + r * d[0], c[1] + r * d[1]))
    return pts


SQ1 = [(0, 0), (2, 0), (2, 2), (0, 2)]
SQ2 = [(1, 1), (3, 1), (3, 3), (1, 3)]


class TestVertexNeighborhoodClassification(unittest.TestCase):
    def test_worked_example(self):
        SA, SB = generate(SQ1, SQ2), generate(SQ2, SQ1)
        self.assertEqual(SA, [(0, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2)])
        self.assertEqual(SB, [(1, 1), (2, 1), (3, 1), (3, 3), (1, 3), (1, 2)])
        self.assertEqual(classify(SA, SB), ["out", "out", "in", "in", "out", "out"])
        self.assertEqual(classify(SB, SA), ["in", "out", "out", "out", "out", "in"])
        self.assertEqual(area(boolean(SQ1, SQ2, "union")), 7)
        self.assertEqual(area(boolean(SQ1, SQ2, "intersection")), 1)
        self.assertEqual(area(boolean(SQ1, SQ2, "difference")), 3)
        self.assertEqual(len(boolean(SQ1, SQ2, "difference")[0]), 6)

    def test_touching_squares(self):
        R = [(2, 0), (4, 0), (4, 2), (2, 2)]  # shares the edge x = 2 with SQ1
        self.assertEqual(classify(generate(SQ1, R), generate(R, SQ1))[1], "on-opposite")
        self.assertEqual(boolean(SQ1, R, "intersection"), [])
        self.assertEqual(area(boolean(SQ1, R, "union")), 8)
        self.assertEqual(sorted(boolean(SQ1, R, "difference")[0]), sorted(SQ1))
        C = [(2, 2), (4, 2), (4, 4), (2, 4)]  # touches SQ1 at one corner
        loops = boolean(SQ1, C, "union")
        self.assertEqual(len(loops), 2)
        self.assertEqual(area(loops), 8)
        self.assertEqual(boolean(SQ1, C, "intersection"), [])

    def test_same_and_nested(self):
        self.assertEqual(area(boolean(SQ1, SQ1, "union")), 4)
        self.assertEqual(boolean(SQ1, SQ1, "difference"), [])
        inner = [(F(1, 2), F(1, 2)), (F(3, 2), F(1, 2)), (F(3, 2), F(3, 2)), (F(1, 2), F(3, 2))]
        loops = boolean(SQ1, inner, "difference")
        self.assertEqual(len(loops), 2)  # an outer loop and a clockwise hole
        self.assertEqual(sorted(area([lp]) for lp in loops), [-1, 4])

    def test_random_against_point_membership_and_area(self):
        rng = random.Random(1986)
        grid = [(F(i, 4), F(j, 4)) for i in range(-1, 30, 3) for j in range(-1, 30, 3)]
        degenerate = 0
        for _ in range(150):
            A, B = random_polygon(rng), random_polygon(rng)
            degenerate += any(on_boundary(p, B) for p in A)
            for op in OPS:
                loops = boolean(A, B, op)
                self.assertEqual(area(loops), brute_area(A, B, op))
                for x in grid:
                    if on_boundary(x, A) or on_boundary(x, B):
                        continue
                    w = winding_number(x, loops)
                    self.assertEqual(w, int(OPS[op](inside(x, A), inside(x, B))))
        self.assertGreater(degenerate, 20)


if __name__ == "__main__":
    unittest.main()
