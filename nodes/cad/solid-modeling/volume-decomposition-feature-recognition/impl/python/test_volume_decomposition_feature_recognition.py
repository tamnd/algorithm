# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volume-decomposition-feature-recognition/. The authors are listed in prov/Y3M61K.jsonl.

import random
import unittest
from bisect import bisect_left
from fractions import Fraction
from itertools import combinations

from volume_decomposition_feature_recognition import Decomposition, in_expression, minimum_cover, recognize


def random_part(rng, size=7, ncells=None):
    """A random simple rectilinear polygon: a polyomino with no holes and no
    pinch vertices, on random integer coordinates. Returns the vertex list
    and an independent membership oracle built from the cells."""
    while True:
        target = ncells or rng.randint(4, 22)
        cells = {(rng.randrange(size), rng.randrange(size))}
        while len(cells) < target:
            i, j = rng.choice(sorted(cells))
            di, dj = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            if 0 <= i + di < size and 0 <= j + dj < size:
                cells.add((i + di, j + dj))
        if ok_polyomino(cells, size):
            break
    mi, mj = min(i for i, _ in cells), min(j for _, j in cells)
    cells = {(i - mi, j - mj) for i, j in cells}
    W, H = max(i for i, _ in cells) + 1, max(j for _, j in cells) + 1
    X = sorted(rng.sample(range(-20, 60), W + 1))
    Y = sorted(rng.sample(range(-20, 60), H + 1))
    poly = [(X[i], Y[j]) for i, j in trace(cells)]

    def oracle(x, y):
        i, j = bisect_left(X, x) - 1, bisect_left(Y, y) - 1
        return (i, j) in cells
    return poly, oracle, cells, X, Y


def ok_polyomino(cells, size):
    # no holes: every empty cell of the padded grid reaches the outside
    empty = {(i, j) for i in range(-1, size + 1) for j in range(-1, size + 1)} - cells
    seen, stack = {(-1, -1)}, [(-1, -1)]
    while stack:
        i, j = stack.pop()
        for c in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if c in empty and c not in seen:
                seen.add(c)
                stack.append(c)
    if seen != empty:
        return False
    # no pinch: no 2 by 2 block with a checkerboard pattern
    for i in range(-1, size):
        for j in range(-1, size):
            a, b = (i, j) in cells, (i + 1, j + 1) in cells
            c, d = (i + 1, j) in cells, (i, j + 1) in cells
            if a == b and c == d and a != c:
                return False
    return True


def trace(cells):
    """The boundary of the cells as one counterclockwise cycle of corners,
    with collinear corners removed."""
    nxt = {}
    for i, j in cells:
        if (i, j - 1) not in cells: nxt[(i, j)] = (i + 1, j)
        if (i + 1, j) not in cells: nxt[(i + 1, j)] = (i + 1, j + 1)
        if (i, j + 1) not in cells: nxt[(i + 1, j + 1)] = (i, j + 1)
        if (i - 1, j) not in cells: nxt[(i, j + 1)] = (i, j)
    start = min(nxt)
    cyc, p = [start], nxt[start]
    while p != start:
        cyc.append(p)
        p = nxt[p]
    out = []
    for k in range(len(cyc)):
        a, b, c = cyc[k - 1], cyc[k], cyc[(k + 1) % len(cyc)]
        if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) != 0:
            out.append(b)
    return out


def generic_points(rng, poly, count):
    """Random rational points with denominator 97, never on a grid line."""
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    pts = []
    while len(pts) < count:
        a = rng.randint(97 * (min(xs) - 2), 97 * (max(xs) + 2))
        b = rng.randint(97 * (min(ys) - 2), 97 * (max(ys) + 2))
        if a % 97 and b % 97:
            pts.append((Fraction(a, 97), Fraction(b, 97)))
    # and points close to every vertex, in all four quadrants
    for x, y in poly:
        for sx in (-1, 1):
            for sy in (-1, 1):
                pts.append((x + Fraction(sx, 97), y + Fraction(sy, 89)))
    return pts


class TestHandCases(unittest.TestCase):
    def test_slot(self):
        poly = [(0, 0), (6, 0), (6, 4), (4, 4), (4, 2), (2, 2), (2, 4), (0, 4)]
        stock, feats = recognize(poly)
        self.assertEqual(stock, (0, 0, 6, 4))
        self.assertEqual(feats, [((2, 2, 4, 4), ("top",))])

    def test_stepped_slot(self):
        poly = [(0, 0), (8, 0), (8, 6), (6, 6), (6, 4), (5, 4), (5, 2), (3, 2),
                (3, 4), (2, 4), (2, 6), (0, 6)]
        dec = Decomposition(poly)
        self.assertEqual(len(dec.delta), 4)          # three cells in the upper band, one below
        self.assertEqual(sorted(dec.maximal_blocks()), [(1, 2, 4, 3), (2, 1, 3, 3)])
        stock, feats = recognize(poly)
        self.assertEqual([r for r, _ in feats], [(2, 4, 6, 6), (3, 2, 5, 6)])

    def test_t_slot_head_has_no_open_side(self):
        poly = [(0, 0), (8, 0), (8, 6), (5, 6), (5, 4), (7, 4), (7, 2), (1, 2),
                (1, 4), (3, 4), (3, 6), (0, 6)]
        stock, feats = recognize(poly)
        self.assertEqual(feats, [((1, 2, 7, 4), ()), ((3, 2, 5, 6), ("top",))])

    def test_two_interacting_steps(self):
        poly = [(0, 0), (6, 0), (6, 1), (5, 1), (5, 3), (3, 3), (3, 4), (0, 4)]
        stock, feats = recognize(poly)
        self.assertEqual(feats, [((3, 3, 6, 4), ("right", "top")), ((5, 1, 6, 4), ("right", "top"))])


class TestAgainstOracle(unittest.TestCase):
    def test_expression_equals_part(self):
        rng = random.Random(11)
        checked = 0
        for _ in range(300):
            poly, oracle, *_ = random_part(rng)
            stock, feats = recognize(poly)
            rects = [r for r, _ in feats]
            for x, y in generic_points(rng, poly, 60):
                self.assertEqual(in_expression(stock, rects, x, y), oracle(x, y))
                checked += 1
            # every feature lies in the delta volume
            for a, b, c, d in rects:
                for _ in range(10):
                    x = Fraction(rng.randint(97 * a + 1, 97 * c - 1), 97)
                    y = Fraction(rng.randint(97 * b + 1, 97 * d - 1), 97)
                    if x.denominator > 1 and y.denominator > 1:
                        self.assertFalse(oracle(x, y))
        self.assertGreater(checked, 500)

    def test_blocks_are_maximal(self):
        rng = random.Random(12)
        for _ in range(200):
            poly, oracle, *_ = random_part(rng)
            dec = Decomposition(poly)
            xs, ys = dec.xs, dec.ys

            def centre(i, j):
                return Fraction(xs[i] + xs[i + 1], 2), Fraction(ys[j] + ys[j + 1], 2)

            for i0, j0, i1, j1 in dec.maximal_blocks():
                for i in range(i0, i1):
                    for j in range(j0, j1):
                        self.assertFalse(oracle(*centre(i, j)))
                # each side is blocked by the part or by the stock
                for strip in ([(i0 - 1, j) for j in range(j0, j1)], [(i1, j) for j in range(j0, j1)],
                              [(i, j0 - 1) for i in range(i0, i1)], [(i, j1) for i in range(i0, i1)]):
                    outside = any(not (0 <= i < dec.nx and 0 <= j < dec.ny) for i, j in strip)
                    self.assertTrue(outside or any(oracle(*centre(i, j)) for i, j in strip))

    def test_cover_is_minimum(self):
        rng = random.Random(13)
        compared = 0
        for _ in range(250):
            poly, oracle, *_ = random_part(rng)
            dec = Decomposition(poly)
            blocks = dec.maximal_blocks()
            if len(blocks) > 12:
                continue
            cover = minimum_cover(dec.delta, blocks)
            cells = lambda b: {(i, j) for i in range(b[0], b[2]) for j in range(b[1], b[3])}
            best = next(k for k in range(len(blocks) + 1)
                        for sub in combinations(blocks, k)
                        if set().union(*[cells(b) for b in sub]) >= dec.delta)
            self.assertEqual(len(cover), best)
            compared += 1
        self.assertGreater(compared, 100)

    def test_cover_search_on_random_cell_sets(self):
        # Delta volumes of simple parts seldom have a redundant maximal block,
        # so the search is also checked on arbitrary sets of cells.
        rng = random.Random(14)
        compared = redundant = 0
        cells = lambda b: {(i, j) for i in range(b[0], b[2]) for j in range(b[1], b[3])}
        for _ in range(400):
            n = rng.randint(3, 5)
            D = {(i, j) for i in range(n) for j in range(n) if rng.random() < 0.65}
            if not D:
                continue
            inside = lambda b: 0 <= b[0] and 0 <= b[1] and b[2] <= n and b[3] <= n and cells(b) <= D
            blocks = [b for b in ((i0, j0, i1, j1) for i0 in range(n) for i1 in range(i0 + 1, n + 1)
                                  for j0 in range(n) for j1 in range(j0 + 1, n + 1))
                      if inside(b) and not any(inside(g) for g in ((b[0] - 1, b[1], b[2], b[3]),
                                                                   (b[0], b[1] - 1, b[2], b[3]),
                                                                   (b[0], b[1], b[2] + 1, b[3]),
                                                                   (b[0], b[1], b[2], b[3] + 1)))]
            if len(blocks) > 12:
                continue
            cover = minimum_cover(D, blocks)
            self.assertEqual(set().union(*[cells(b) for b in cover]), D)
            best = next(k for k in range(len(blocks) + 1)
                        for sub in combinations(blocks, k)
                        if set().union(*[cells(b) for b in sub]) >= D)
            self.assertEqual(len(cover), best)
            compared += 1
            redundant += best < len(blocks)
        self.assertGreater(compared, 200)
        self.assertGreater(redundant, 50)


if __name__ == "__main__":
    unittest.main()
