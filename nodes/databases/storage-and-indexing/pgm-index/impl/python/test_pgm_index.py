# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pgm-index/. The authors are listed in prov/YYKWMY.jsonl.

import bisect
import random
import unittest
from fractions import Fraction
from itertools import combinations

from pgm_index import PGMIndex, build_pla


def feasible(xs, ys, eps):
    """Brute force: is there a line within eps of all points?

    By Helly's theorem in the (slope, intercept) plane, this holds if and only
    if it holds for every three points. For three points it holds if and only
    if the middle point is within 2 eps of the line through the outer two.
    """
    for a, b, c in combinations(range(len(xs)), 3):
        mid = Fraction(ys[a]) + Fraction(ys[c] - ys[a], xs[c] - xs[a]) * (xs[b] - xs[a])
        if abs(ys[b] - mid) > 2 * eps:
            return False
    return True


def optimal_count(xs, eps):
    """The fewest segments of any PLA with the error eps, by dynamic programming."""
    n = len(xs)
    best = [0] + [n + 1] * n
    for j in range(1, n + 1):
        for i in range(j):
            if best[i] + 1 < best[j] and feasible(xs[i:j], list(range(i, j)), eps):
                best[j] = best[i] + 1
    return best[n]


def random_keys(rng, n, kind):
    if kind == "uniform":
        return sorted(rng.sample(range(10 * n + 10), n))
    if kind == "clustered":
        out = set()
        while len(out) < n:
            centre = rng.randrange(10 ** 6)
            for _ in range(rng.randrange(1, 30)):
                out.add(centre + rng.randrange(200))
        return sorted(out)[:n]
    # gaps that grow fast, a hard case for a linear model
    out, x = [], 0
    for i in range(n):
        x += 1 + rng.randrange(1 + i * i // 50)
        out.append(x)
    return out


class TestPLA(unittest.TestCase):
    def test_error_bound_and_coverage(self):
        rng = random.Random(1)
        for kind in ("uniform", "clustered", "growing"):
            for eps in (1, 2, 4, 16):
                xs = random_keys(rng, 250, kind)
                segs = build_pla(xs, eps)
                self.assertEqual(segs[0].start, 0)
                self.assertEqual(segs[-1].end, len(xs) - 1)
                for a, b in zip(segs, segs[1:]):
                    self.assertEqual(a.end + 1, b.start)
                for s in segs:
                    for i in range(s.start, s.end + 1):
                        self.assertLessEqual(abs(s.predict(xs[i]) - i), eps)
                # every segment but the last covers at least 2 eps + 1 keys
                for s in segs[:-1]:
                    self.assertGreaterEqual(s.end - s.start + 1, 2 * eps + 1)
                self.assertLessEqual(len(segs), -(-len(xs) // (2 * eps)))

    def test_greedy_is_optimal(self):
        rng = random.Random(2)
        for trial in range(30):
            n = rng.randrange(3, 22)
            xs = random_keys(rng, n, rng.choice(["uniform", "growing", "clustered"]))
            eps = rng.choice([1, 1, 2])
            self.assertEqual(len(build_pla(xs, eps)), optimal_count(xs, eps), (xs, eps))

    def test_feasible_matches_greedy_on_one_segment(self):
        rng = random.Random(3)
        for _ in range(60):
            n = rng.randrange(2, 12)
            xs = random_keys(rng, n, "growing")
            one = len(build_pla(xs, 1)) == 1
            self.assertEqual(one, feasible(xs, list(range(n)), 1))


class TestPGMIndex(unittest.TestCase):
    def test_against_bisect(self):
        rng = random.Random(4)
        for kind in ("uniform", "clustered", "growing"):
            for eps, eps_rec in ((1, 1), (4, 2), (16, 4), (64, 4)):
                keys = random_keys(rng, 500, kind)
                keyset = set(keys)
                t = PGMIndex(keys, eps, eps_rec)
                self.assertEqual(t.segment_counts()[-1], 1)
                self.assertLessEqual(t.max_error(), max(eps, eps_rec))
                lo, hi = keys[0] - 5, keys[-1] + 5
                probes = list(keys[::9]) + [rng.randrange(lo, hi) for _ in range(80)] + [lo, hi]
                for x in probes:
                    self.assertEqual(t.rank(x), bisect.bisect_right(keys, x))
                    self.assertLessEqual(t.probes, 2 * max(eps, eps_rec) + 2)
                    self.assertEqual(t.lower_bound(x), bisect.bisect_left(keys, x))
                    self.assertEqual(t.contains(x), x in keyset)
                a = rng.randrange(lo, hi)
                b = a + rng.randrange(1000)
                self.assertEqual(t.range(a, b), [k for k in keys if a <= k <= b])

    def test_levels_shrink(self):
        keys = random_keys(random.Random(5), 1200, "growing")
        t = PGMIndex(keys, 2, 1)
        counts = t.segment_counts()
        self.assertGreaterEqual(len(counts), 3)
        self.assertLessEqual(counts[0], -(-len(keys) // 5))       # at least 2 eps + 1 = 5 keys per segment
        for below, above in zip(counts, counts[1:]):
            self.assertLessEqual(above, -(-below // 3))         # at least 2 eps_rec + 1 = 3 keys per segment

    def test_example_of_the_page(self):
        keys = [2, 3, 5, 8, 12, 13, 14, 20, 30, 31, 40, 41]
        t = PGMIndex(keys, 1, 1)
        segs = t.levels[-1]
        self.assertEqual([(s.start, s.end) for s in segs], [(0, 7), (8, 11)])
        self.assertEqual((segs[0].slope, segs[0].intercept), (Fraction(49, 120), Fraction(19, 60)))
        self.assertEqual(t.segment_counts(), [2, 1])
        self.assertEqual(t.rank(13), 6)
        self.assertEqual(t.lower_bound(25), 8)
        self.assertFalse(t.contains(25))

    def test_small_and_bad_inputs(self):
        t = PGMIndex([], 4)
        self.assertEqual(t.rank(10), 0)
        self.assertFalse(t.contains(10))
        t = PGMIndex([7], 4)
        self.assertEqual((t.rank(6), t.rank(7), t.rank(8)), (0, 1, 1))
        self.assertTrue(t.contains(7))
        with self.assertRaises(ValueError):
            PGMIndex([1, 1, 2])
        with self.assertRaises(ValueError):
            PGMIndex([1, 2], eps=0)


if __name__ == "__main__":
    unittest.main()
