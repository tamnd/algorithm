# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-means-plus-plus/. The authors are listed in prov/V3K4X6.jsonl.

import itertools
import random
from fractions import Fraction as F

from k_means_plus_plus import cost, k_means_plus_plus, seed, seeding_distribution, sq_dist


def pts(*xs):
    return [tuple(F(v) for v in (x if isinstance(x, tuple) else (x,))) for x in xs]


def exact_seed_law(points, k):
    """The exact probability of each ordered sequence of k chosen indices."""
    law = {(): F(1)}
    for _ in range(k):
        nxt = {}
        for seq, p in law.items():
            for i, q in enumerate(seeding_distribution(points, list(seq))):
                if q:
                    nxt[seq + (i,)] = nxt.get(seq + (i,), 0) + p * q
        law = nxt
    return law


def test_distribution_example() -> None:
    x = pts(0, 1, 6, 7)
    assert seeding_distribution(x, []) == [F(1, 4)] * 4
    assert seeding_distribution(x, [0]) == [0, F(1, 86), F(36, 86), F(49, 86)]
    assert seeding_distribution(x, [0, 3]) == [0, F(1, 2), F(1, 2), 0]
    law = exact_seed_law(x, 2)
    assert sum(law.values()) == 1
    assert law[(0, 3)] == F(1, 4) * F(49, 86)


def test_exact_split_probability() -> None:
    x = pts(0, 1, 6, 7)
    law = exact_seed_law(x, 2)
    split = sum(p for s, p in law.items() if (s[0] < 2) != (s[1] < 2))
    # first 0: 85/86; first 1: 61/62 (25 + 36 over 62); first 6: 61/62; first 7: 85/86
    assert split == F(1, 2) * (F(85, 86) + F(61, 62))


def test_sampler_matches_law() -> None:
    x = pts((0, 0), (1, 0), (0, 1), (5, 5), (6, 5), (9, 0))
    k = 3
    law = exact_seed_law(x, k)
    rng = random.Random(2024)
    trials = 8000
    counts = {}
    for _ in range(trials):
        s = tuple(seed(x, k, rng))
        counts[s] = counts.get(s, 0) + 1
    for s, c in counts.items():
        assert s in law  # the sampler never picks a sequence of probability 0
    for s, p in law.items():
        if p > F(1, 50):
            freq = counts.get(s, 0) / trials
            sd = (float(p) * (1 - float(p)) / trials) ** 0.5
            assert abs(freq - float(p)) < 5 * sd


def test_never_repeats_and_zero_weight() -> None:
    rng = random.Random(9)
    x = pts(3, 3, 3, 8)
    for _ in range(200):
        s = seed(x, 3, rng)
        assert len(set(s)) == 3
        assert 3 in s  # the only point at positive distance must be chosen by step 2
    assert seeding_distribution(x, [0, 3]) == [0, F(1, 2), F(1, 2), 0]


def test_expected_seeding_cost_below_bound() -> None:
    import math
    rng = random.Random(5)
    for _ in range(25):
        n = rng.randrange(3, 7)
        x = [(F(rng.randrange(0, 12)), F(rng.randrange(0, 12))) for _ in range(n)]
        k = rng.randrange(1, min(n, 3) + 1)
        law = exact_seed_law(x, k)
        expected = sum(p * cost(x, [x[i] for i in s]) for s, p in law.items())
        # optimum over all choices of labels: brute force by centroids of label maps
        best = None
        for lab in itertools.product(range(k), repeat=n):
            groups = [[p for p, a in zip(x, lab) if a == j] for j in range(k)]
            if any(not g for g in groups):
                continue
            c = sum(sum(sq_dist(p, tuple(sum(q[t] for q in g) / len(g) for t in range(2))) for p in g) for g in groups)
            best = c if best is None or c < best else best
        assert float(expected) <= 8 * (math.log(k) + 2) * float(best) + 1e-9


def test_full_run_is_fixed_point() -> None:
    rng = random.Random(1)
    x = [(F(rng.randrange(-20, 21)), F(rng.randrange(-20, 21))) for _ in range(40)]
    centers, labels = k_means_plus_plus(x, 4, rng)
    for p, a in zip(x, labels):
        assert sq_dist(p, centers[a]) == min(sq_dist(p, c) for c in centers)
