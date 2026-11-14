# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hint-based-feature-recognition/. The authors are listed in prov/0YXFJ0.jsonl.

import random
import unittest
from bisect import bisect_left
from fractions import Fraction

from hint_based_feature_recognition import Grid, in_expression, recognize


def random_part(rng, size=7):
    """A hole-free polyomino with no pinch points, traced into a simple
    rectilinear polygon on random integer coordinates. Returns the polygon,
    the cells, and the coordinates of the cell grid."""
    while True:
        target = rng.randint(4, 24)
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
    return [(X[i], Y[j]) for i, j in trace(cells)], cells, X, Y


def random_carved(rng):
    """A block of cells with winding tunnels carved in from its boundary.
    Tunnels that turn under the material make undercuts, which random growth
    seldom does. Returns the same as random_part."""
    a, b = rng.randint(4, 8), rng.randint(4, 8)
    cells = {(i, j) for i in range(a) for j in range(b)}
    for _ in range(rng.randint(1, 3)):
        i, j = rng.choice([(rng.randrange(a), 0), (rng.randrange(a), b - 1), (0, rng.randrange(b)), (a - 1, rng.randrange(b))])
        di, dj = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        for _ in range(rng.randint(2, 10)):
            trial = cells - {(i, j)}
            if (i, j) in cells and len(trial) >= 3 and ok_polyomino(trial, max(a, b)) and connected(trial):
                cells = trial
            if rng.random() < 0.4:
                di, dj = rng.choice([(dj, di), (-dj, -di)])
            i, j = i + di, j + dj
            if not (0 <= i < a and 0 <= j < b):
                break
    mi, mj = min(i for i, _ in cells), min(j for _, j in cells)
    cells = {(i - mi, j - mj) for i, j in cells}
    W, H = max(i for i, _ in cells) + 1, max(j for _, j in cells) + 1
    X = sorted(rng.sample(range(-20, 60), W + 1))
    Y = sorted(rng.sample(range(-20, 60), H + 1))
    return [(X[i], Y[j]) for i, j in trace(cells)], cells, X, Y


def connected(cells):
    start = next(iter(cells))
    seen, stack = {start}, [start]
    while stack:
        i, j = stack.pop()
        for c in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if c in cells and c not in seen:
                seen.add(c)
                stack.append(c)
    return len(seen) == len(cells)


def ok_polyomino(cells, size):
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
    for i in range(-1, size):
        for j in range(-1, size):
            a, b = (i, j) in cells, (i + 1, j + 1) in cells
            c, d = (i + 1, j) in cells, (i, j + 1) in cells
            if a == b and c == d and a != c:
                return False
    return True


def trace(cells):
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


def accessible(cells, W, H, i, j):
    """Brute force: can a straight axis move from outside the stock reach
    the empty cell (i, j) without passing through the part?"""
    return (all((i, t) not in cells for t in range(j + 1, H))
            or all((i, t) not in cells for t in range(0, j))
            or all((t, j) not in cells for t in range(i + 1, W))
            or all((t, j) not in cells for t in range(0, i)))


def rect_of(feats, undercut):
    return [f["rect"] for f in feats if (f["kind"] == "undercut") == undercut]


class TestHandCases(unittest.TestCase):
    def test_slot(self):
        poly = [(0, 0), (6, 0), (6, 4), (4, 4), (4, 2), (2, 2), (2, 4), (0, 4)]
        _, feats = recognize(poly)
        self.assertEqual(len(feats), 1)
        self.assertEqual((feats[0]["rect"], feats[0]["kind"], feats[0]["approach"]),
                         ((2, 2, 4, 4), "slot", ("top",)))

    def test_stepped_slot_split_floor_still_gives_the_upper_slot(self):
        poly = [(0, 0), (8, 0), (8, 6), (6, 6), (6, 4), (5, 4), (5, 2), (3, 2),
                (3, 4), (2, 4), (2, 6), (0, 6)]
        _, feats = recognize(poly)
        self.assertEqual([(f["rect"], f["kind"], f["approach"]) for f in feats],
                         [((2, 4, 6, 6), "slot", ("top",)), ((3, 2, 5, 6), "slot", ("top",))])

    def test_t_slot_head_is_an_undercut(self):
        poly = [(0, 0), (8, 0), (8, 6), (5, 6), (5, 4), (7, 4), (7, 2), (1, 2),
                (1, 4), (3, 4), (3, 6), (0, 6)]
        _, feats = recognize(poly)
        self.assertEqual([(f["rect"], f["kind"]) for f in feats],
                         [((3, 2, 5, 6), "slot"), ((1, 2, 7, 4), "undercut")])

    def test_corner_steps(self):
        poly = [(0, 0), (6, 0), (6, 1), (5, 1), (5, 3), (3, 3), (3, 4), (0, 4)]
        _, feats = recognize(poly)
        self.assertEqual([(f["rect"], f["kind"], f["approach"]) for f in feats],
                         [((3, 3, 6, 4), "step", ("right", "top")), ((5, 1, 6, 4), "step", ("right", "top"))])

    def test_plus_shape_has_four_steps(self):
        plus = [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (2, 2), (2, 3), (1, 3), (1, 2), (0, 2), (0, 1), (1, 1)]
        _, feats = recognize(plus)
        self.assertEqual([(f["rect"], f["kind"]) for f in feats],
                         [((0, 0, 1, 1), "step"), ((0, 2, 1, 3), "step"),
                          ((2, 0, 3, 1), "step"), ((2, 2, 3, 3), "step")])
        # each corner square is reached from two sides
        self.assertTrue(all(len(f["approach"]) == 2 for f in feats))


class TestAgainstOracle(unittest.TestCase):
    def test_expression_and_accessibility(self):
        rng = random.Random(31)
        points = with_undercut = 0
        for t in range(600):
            poly, cells, X, Y = random_part(rng) if t % 2 else random_carved(rng)
            W, H = len(X) - 1, len(Y) - 1
            stock, feats = recognize(poly)
            self.assertEqual(stock, (X[0], Y[0], X[-1], Y[-1]))
            acc, und = rect_of(feats, False), rect_of(feats, True)
            with_undercut += bool(und)
            for f in feats:
                if f["kind"] == "undercut":
                    # no tool reaches an undercut, so it touches no side of the stock
                    self.assertEqual(f["open"], ())
                else:
                    # a tool can come in: the approach side is open
                    for side in f["approach"]:
                        self.assertIn(side, f["open"])
            for _ in range(40):
                x = Fraction(rng.randint(97 * X[0] - 30, 97 * X[-1] + 30), 97)
                y = Fraction(rng.randint(97 * Y[0] - 30, 97 * Y[-1] + 30), 97)
                if x.denominator == 1 or y.denominator == 1:
                    continue
                i, j = bisect_left(X, x) - 1, bisect_left(Y, y) - 1
                inside_w = 0 <= i < W and 0 <= j < H
                in_p = (i, j) in cells
                self.assertEqual(in_expression(stock, acc + und, x, y), in_p)
                if inside_w and not in_p:
                    in_acc = any(a < x < c and b < y < d for a, b, c, d in acc)
                    self.assertEqual(in_acc, accessible(cells, W, H, i, j))
                if in_p or not inside_w:
                    # no feature reaches into the part or outside the stock
                    self.assertFalse(any(a < x < c and b < y < d for a, b, c, d in acc + und))
                points += 1
        self.assertGreater(points, 500)
        self.assertGreater(with_undercut, 30)

    def test_every_hint_cell_is_on_the_boundary(self):
        from hint_based_feature_recognition import hints
        rng = random.Random(32)
        for _ in range(100):
            poly, cells, X, Y = random_part(rng)
            g = Grid(poly)
            for (i, j), side in hints(g):
                self.assertIn((i, j), g.D)
                di, dj = {"right": (1, 0), "left": (-1, 0), "top": (0, 1), "bottom": (0, -1)}[side]
                self.assertNotIn((i - di, j - dj), g.D)


if __name__ == "__main__":
    unittest.main()
