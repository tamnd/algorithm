# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-binary-segmentation/. The authors are listed in prov/6NYYG1.jsonl.

import itertools
import math
import random

from circular_binary_segmentation import cbs, max_arc, permutation_p_value, segment_means

EXAMPLE = [0.1, -0.2, 0.0, 0.2, -0.1, 1.1, 0.9, 1.0, 1.2, 0.0, -0.1, 0.1]


def direct_max_arc(y):
    """The arc statistic from the definition, with means computed from scratch."""
    n = len(y)
    mu = sum(y) / n
    s = math.sqrt(sum((v - mu) ** 2 for v in y) / (n - 1))
    best = (-1.0, 0, n)
    for i in range(n):
        for j in range(i + 1, n + 1):
            if j - i == n:
                continue
            ins = y[i:j]
            out = y[:i] + y[j:]
            z = abs(sum(ins) / len(ins) - sum(out) / len(out)) / (s * math.sqrt(1 / len(ins) + 1 / len(out)))
            if z > best[0] + 1e-12:
                best = (z, i, j)
    return best


def rss(x, cuts):
    return sum(sum((v - m) ** 2 for v in x[a:b]) for a, b, m in segment_means(x, cuts))


def best_segmentation(x, k):
    """Least squares segmentation into k segments, by brute force over all cut sets."""
    n = len(x)
    return min(itertools.combinations(range(1, n), k - 1), key=lambda c: rss(x, list(c)))


def test_max_arc_against_definition():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(2, 12)
        y = [rng.gauss(0, 1) for _ in range(n)]
        t, i, j = max_arc(y)
        t2, i2, j2 = direct_max_arc(y)
        assert abs(t - t2) < 1e-9
        assert (i, j) == (i2, j2)


def test_example_statistic():
    t, i, j = max_arc(EXAMPLE)
    assert (i, j) == (5, 9)
    assert abs(t - 3.224704) < 1e-6


def test_example_p_value_near_exact():
    # The four high values form one arc in 12 of the C(12, 4) = 495 placements on the circle,
    # and only those placements reach the observed statistic, so the exact p-value is 12 / 495.
    t, _, _ = max_arc(EXAMPLE)
    n_perm = 1999
    p = permutation_p_value(EXAMPLE, t, random.Random(8), n_perm)
    exact = 12 / 495
    assert abs(p - exact) <= 4 * math.sqrt(exact * (1 - exact) / n_perm) + 1 / n_perm


def test_example_segmentation_matches_brute_force():
    cuts = cbs(EXAMPLE, random.Random(5), alpha=0.05, n_perm=999)
    assert cuts == [5, 9]
    assert tuple(cuts) == best_segmentation(EXAMPLE, 3)
    # At the level 0.01 the 12 points cannot show the change: the exact p-value is 0.0242.
    assert cbs(EXAMPLE, random.Random(5), alpha=0.01, n_perm=999) == []


def test_single_change_point():
    x = [0.0, 0.1, -0.1, 0.05, 2.0, 2.1, 1.9, 2.05, 1.95, 2.0]
    cuts = cbs(x, random.Random(2), alpha=0.1, n_perm=999)
    assert cuts == [4]
    assert tuple(cuts) == best_segmentation(x, 2)


def test_constant_and_short():
    assert cbs([1.0] * 8, random.Random(0)) == []
    assert cbs([3.0], random.Random(0)) == []
    assert cbs([], random.Random(0)) == []
    assert max_arc([2.0, 2.0, 2.0]) == (0.0, 0, 3)


def test_p_value_bounds():
    rng = random.Random(9)
    y = [rng.gauss(0, 1) for _ in range(10)]
    t, _, _ = max_arc(y)
    p = permutation_p_value(y, t, rng, 99)
    assert 1 / 100 <= p <= 1
    # The observed order is one of the permutations, so a huge statistic still gives p = 1 / (P + 1).
    assert permutation_p_value(y, 1e9, rng, 99) == 1 / 100


def test_pure_noise_has_few_false_splits():
    rng = random.Random(31)
    false_splits = 0
    for _ in range(10):
        y = [rng.gauss(0, 1) for _ in range(20)]
        false_splits += len(cbs(y, rng, alpha=0.01, n_perm=99)) > 0
    assert false_splits <= 2


def test_simulated_segments_recovered():
    rng = random.Random(2004)
    truth = [15, 21, 40]
    levels = [0.0, 1.0, 0.0, -1.0]
    bounds = [0] + truth + [50]
    x = []
    for (a, b), mu in zip(zip(bounds, bounds[1:]), levels):
        x.extend(mu + rng.gauss(0, 0.25) for _ in range(b - a))
    cuts = cbs(x, rng, alpha=0.01, n_perm=199)
    assert cuts == truth
