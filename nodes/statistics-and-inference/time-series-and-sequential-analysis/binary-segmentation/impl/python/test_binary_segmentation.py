# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-segmentation/. The authors are listed in prov/PQ8R7K.jsonl.
import math
import random
from fractions import Fraction

from binary_segmentation import (
    best_split,
    binary_segmentation,
    contrast,
    contrast_squared,
    default_threshold,
    prefix_sums,
    random_intervals,
    wild_binary_segmentation,
)

EXAMPLE = [0.1, -0.3, 0.2, 0.0, 2.1, 1.8, 2.2, 1.9, 2.0, -0.1, 0.2, 0.1]


def rss(xs):
    if not xs:
        return 0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs)


def naive_contrast(xs, s, b, e):
    left = xs[s:b]
    right = xs[b:e]
    d = sum(left) / len(left) - sum(right) / len(right)
    return math.sqrt(len(left) * len(right) / (e - s)) * abs(d)


def naive_binseg(xs, zeta, s=0, e=None):
    """Plain recursion with O(L) contrasts: the reference for the stack version."""
    if e is None:
        e = len(xs)
    if e - s < 2:
        return []
    vals = [(naive_contrast(xs, s, b, e), -b) for b in range(s + 1, e)]
    c, nb = max(vals)
    if c <= zeta:
        return []
    b = -nb
    return sorted(naive_binseg(xs, zeta, s, b) + [b] + naive_binseg(xs, zeta, b, e))


def test_worked_example():
    p = prefix_sums(EXAMPLE)
    b, c = best_split(p, 0, 12)
    assert b == 4 and abs(c - 2.082) < 1e-3
    b, c = best_split(p, 4, 12)
    assert b == 9 and abs(c - 2.647) < 1e-3
    assert binary_segmentation(EXAMPLE, 1.5) == [4, 9]


def test_edge_cases():
    assert binary_segmentation([], 1.0) == []
    assert binary_segmentation([5.0], 1.0) == []
    assert binary_segmentation([0.0, 10.0], 1.0) == [1]
    assert binary_segmentation([1.0] * 20, 0.0) == []


def test_contrast_squared_is_rss_drop_exact():
    rng = random.Random(1974)
    for _ in range(500):
        n = rng.randint(2, 15)
        xs = [Fraction(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(n)]
        p = prefix_sums(xs)
        s = rng.randint(0, n - 2)
        e = rng.randint(s + 2, n)
        b = rng.randint(s + 1, e - 1)
        assert contrast_squared(p, s, b, e) == rss(xs[s:e]) - rss(xs[s:b]) - rss(xs[b:e])


def test_matches_naive_recursion():
    rng = random.Random(1981)
    for _ in range(500):
        n = rng.randint(0, 25)
        mu = 0.0
        xs = []
        for _ in range(n):
            if rng.random() < 0.15:
                mu = rng.choice([-3.0, 0.0, 3.0])
            xs.append(mu + rng.gauss(0.0, 0.5))
        zeta = rng.uniform(0.5, 3.0)
        assert binary_segmentation(xs, zeta) == naive_binseg(xs, zeta)


def test_argmax_against_brute_force():
    rng = random.Random(6)
    for _ in range(500):
        n = rng.randint(2, 20)
        xs = [rng.gauss(0.0, 1.0) for _ in range(n)]
        p = prefix_sums(xs)
        b, c = best_split(p, 0, n)
        vals = [naive_contrast(xs, 0, k, n) for k in range(1, n)]
        assert abs(c - max(vals)) < 1e-9
        assert abs(contrast(p, 0, b, n) - max(vals)) < 1e-9


def test_misses_a_short_burst_that_wbs_finds():
    xs = [0.0] * 50 + [3.0] * 4 + [0.0] * 50
    zeta = default_threshold(len(xs))
    assert abs(zeta - 3.962) < 1e-3
    assert abs(best_split(prefix_sums(xs), 0, len(xs))[1] - 1.1323) < 1e-4
    assert binary_segmentation(xs, zeta) == []
    intervals = random_intervals(len(xs), 100, random.Random(1))
    assert wild_binary_segmentation(xs, zeta, intervals) == [50, 54]


def test_noisy_burst():
    rng = random.Random(2014)
    xs = [rng.gauss(0, 1) for _ in range(150)] + [rng.gauss(4, 1) for _ in range(6)] + [rng.gauss(0, 1) for _ in range(150)]
    zeta = default_threshold(len(xs))
    assert binary_segmentation(xs, zeta) == []
    found = wild_binary_segmentation(xs, zeta, random_intervals(len(xs), 300, random.Random(2)))
    assert any(abs(c - 150) <= 2 for c in found) and any(abs(c - 156) <= 2 for c in found)


def test_wbs_with_no_intervals_is_binary_segmentation():
    rng = random.Random(8)
    for _ in range(100):
        xs = [rng.choice([0.0, 2.0]) + rng.gauss(0, 0.3) for _ in range(rng.randint(0, 30))]
        assert wild_binary_segmentation(xs, 1.2, []) == binary_segmentation(xs, 1.2)
