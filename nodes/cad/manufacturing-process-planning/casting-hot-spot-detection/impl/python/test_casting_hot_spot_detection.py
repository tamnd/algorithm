# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/casting-hot-spot-detection/. The authors are listed in prov/NAYQYF.jsonl.

import random
import unittest
from itertools import product

from casting_hot_spot_detection import from_rows, hot_spots, lower_envelope_1d, squared_edt

PAGE_ROWS = [
    ".............",
    ".#####.......",
    ".#####..###..",
    ".###########.",
    ".#####..###..",
    ".#####.......",
    ".............",
]


def cells_of(shape):
    return list(product(*[range(s) for s in shape]))


def brute_edt(mask, shape):
    cells = cells_of(shape)
    mold = [c for c, m in zip(cells, mask) if m == 0]
    out = []
    for c in cells:
        out.append(min(sum((a - b) ** 2 for a, b in zip(c, y)) for y in mold))
    return out


def brute_hot_cells(mask, shape, dist):
    """Cells in regional maxima, by a second definition.

    A metal cell x lies in a regional maximum if and only if the connected
    component of x in the upper set {y metal : D(y) >= D(x)} has no cell with
    D > D(x). The plateau of x is then that whole component.
    """
    cells = cells_of(shape)
    index = {c: i for i, c in enumerate(cells)}
    result = {}
    for c, m in zip(cells, mask):
        if m != 1:
            continue
        v = dist[index[c]]
        comp = {c}
        stack = [c]
        top = v
        while stack:
            x = stack.pop()
            for off in product((-1, 0, 1), repeat=len(shape)):
                y = tuple(a + o for a, o in zip(x, off))
                if y in index and y not in comp:
                    j = index[y]
                    if mask[j] == 1 and dist[j] >= v:
                        comp.add(y)
                        stack.append(y)
                        top = max(top, dist[j])
        if top == v:
            result[c] = (v, frozenset(comp))
    return result


def random_mask(rng, shape, p):
    mask = [1 if rng.random() < p else 0 for _ in range(len(cells_of(shape)))]
    if all(m == 1 for m in mask):
        mask[rng.randrange(len(mask))] = 0
    return mask


class LowerEnvelopeTest(unittest.TestCase):
    def test_random_lines_match_brute_force(self):
        rng = random.Random(7)
        for _ in range(400):
            n = rng.randint(1, 15)
            f = [None if rng.random() < 0.4 else rng.randint(0, 30) for _ in range(n)]
            got = lower_envelope_1d(f)
            for q in range(n):
                vals = [(q - p) ** 2 + f[p] for p in range(n) if f[p] is not None]
                self.assertEqual(got[q], min(vals) if vals else None)

    def test_ties_and_equal_values(self):
        self.assertEqual(lower_envelope_1d([0, None, None, None, 0]), [0, 1, 4, 1, 0])
        self.assertEqual(lower_envelope_1d([5, 5, 5]), [5, 5, 5])
        self.assertEqual(lower_envelope_1d([None, None]), [None, None])


class EDTTest(unittest.TestCase):
    def test_random_2d_matches_brute_force(self):
        rng = random.Random(11)
        for _ in range(80):
            shape = (rng.randint(1, 12), rng.randint(1, 12))
            mask = random_mask(rng, shape, rng.choice([0.5, 0.8, 0.95]))
            self.assertEqual(squared_edt(mask, shape), brute_edt(mask, shape))

    def test_random_3d_matches_brute_force(self):
        rng = random.Random(13)
        for _ in range(25):
            shape = (rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6))
            mask = random_mask(rng, shape, rng.choice([0.6, 0.9, 0.98]))
            self.assertEqual(squared_edt(mask, shape), brute_edt(mask, shape))

    def test_one_and_four_dimensions(self):
        rng = random.Random(17)
        for _ in range(30):
            shape = (rng.randint(1, 20),)
            mask = random_mask(rng, shape, 0.8)
            self.assertEqual(squared_edt(mask, shape), brute_edt(mask, shape))
        for _ in range(5):
            shape = (3, 4, 3, 4)
            mask = random_mask(rng, shape, 0.9)
            self.assertEqual(squared_edt(mask, shape), brute_edt(mask, shape))

    def test_page_example(self):
        mask, shape = from_rows(PAGE_ROWS)
        d = squared_edt(mask, shape)
        row3 = d[3 * 13:4 * 13]
        self.assertEqual(row3, [0, 1, 4, 9, 5, 2, 1, 1, 2, 4, 2, 1, 0])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            squared_edt([1, 1, 1, 1], (2, 2))
        with self.assertRaises(ValueError):
            squared_edt([1, 0, 1], (2, 2))
        with self.assertRaises(ValueError):
            squared_edt([1, 0, 2, 0], (2, 2))
        with self.assertRaises(ValueError):
            squared_edt([], ())
        with self.assertRaises(ValueError):
            from_rows(["#.", "#"])


class HotSpotTest(unittest.TestCase):
    def test_page_example(self):
        mask, shape = from_rows(PAGE_ROWS)
        self.assertEqual(hot_spots(mask, shape), [(9, [(3, 3)]), (4, [(3, 9)])])

    def test_cube_has_one_centre(self):
        n = 7
        shape = (n, n, n)
        mask = [1 if all(1 <= x <= n - 2 for x in c) else 0 for c in cells_of(shape)]
        self.assertEqual(hot_spots(mask, shape), [(9, [(3, 3, 3)])])

    def test_plate_is_one_plateau(self):
        shape = (4, 8, 8)
        mask = [1 if (1 <= c[0] <= 2 and 1 <= c[1] <= 6 and 1 <= c[2] <= 6) else 0 for c in cells_of(shape)]
        spots = hot_spots(mask, shape)
        # A plate two cells thick: every metal cell is next to the mold.
        self.assertEqual(len(spots), 1)
        self.assertEqual(spots[0][0], 1)
        self.assertEqual(len(spots[0][1]), 2 * 6 * 6)

    def test_random_grids_match_second_definition(self):
        rng = random.Random(23)
        trials = [(rng.randint(2, 11), rng.randint(2, 11)) for _ in range(60)]
        trials += [(rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 6)) for _ in range(20)]
        for shape in trials:
            mask = random_mask(rng, shape, rng.choice([0.6, 0.85, 0.97]))
            dist = squared_edt(mask, shape)
            spots = hot_spots(mask, shape)
            expect = brute_hot_cells(mask, shape, dist)
            got = {}
            for value, plateau in spots:
                comp = frozenset(plateau)
                for c in plateau:
                    self.assertNotIn(c, got)
                    got[c] = (value, comp)
            self.assertEqual(got, expect)
            values = [v for v, _ in spots]
            self.assertEqual(values, sorted(values, reverse=True))
            if any(mask):
                self.assertEqual(values[0], max(d for d, m in zip(dist, mask) if m == 1))


if __name__ == "__main__":
    unittest.main()
