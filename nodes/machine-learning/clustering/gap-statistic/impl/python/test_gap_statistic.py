# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gap-statistic/. The authors are listed in prov/BXW1TS.jsonl.

import random
from math import isclose

from gap_statistic import choose_k, gap_statistic, kmeans, pooled_dispersion, reference_sampler, sqdist


def three_clusters(seed):
    # Standard normal clusters of 25, 25 and 50 points centered at (0, 0), (0, 5) and (5, -3).
    r = random.Random(seed)
    pts = []
    for (cx, cy), m in [((0, 0), 25), ((0, 5), 25), ((5, -3), 50)]:
        pts += [[r.gauss(cx, 1), r.gauss(cy, 1)] for _ in range(m)]
    return pts


def uniform_square(seed, n=60):
    r = random.Random(seed)
    return [[r.random(), r.random()] for _ in range(n)]


def test_dispersion_is_within_sum_of_squares() -> None:
    rng = random.Random(1)
    pts = [[rng.uniform(0, 5), rng.uniform(0, 5)] for _ in range(30)]
    lab = [rng.randrange(3) for _ in range(30)]
    wcss = 0.0
    for c in set(lab):
        g = [x for x, l in zip(pts, lab) if l == c]
        m = [sum(col) / len(g) for col in zip(*g)]
        wcss += sum(sqdist(x, m) for x in g)
    assert isclose(pooled_dispersion(pts, lab), wcss, rel_tol=1e-12)


def test_rule_on_given_values() -> None:
    gap = [0.10, 0.50, 0.90, 0.85, 0.95]
    s = [0.05, 0.05, 0.05, 0.06, 0.20]
    # k = 3 is the first k with Gap(k) >= Gap(k + 1) - s_(k+1): 0.90 >= 0.85 - 0.06.
    assert choose_k(gap, s) == 3
    assert choose_k([0.2, 0.1, 0.3], [0.0, 0.0, 0.0]) == 1
    assert choose_k([0.1, 0.2, 0.3], [0.0, 0.0, 0.0]) == 3


def test_reference_sets_stay_in_their_box() -> None:
    rng = random.Random(2)
    pts = [[t, 2 * t + rng.uniform(-0.1, 0.1)] for t in [i / 10 for i in range(30)]]
    box = reference_sampler(pts, "box")(rng)
    assert all(0 <= x <= 2.9 + 1e-12 and min(p[1] for p in pts) <= y <= max(p[1] for p in pts) for x, y in box)
    # The principal component box of points near a line is thin: the reference stays near the line.
    pc = reference_sampler(pts, "pc")(rng)
    assert all(abs(y - 2 * x) < 0.5 for x, y in pc)


def test_kmeans_finds_separated_groups() -> None:
    pts = [[0, 0], [0, 1], [1, 0], [10, 10], [10, 11], [11, 10]]
    lab = kmeans(pts, 2, random.Random(0))
    assert lab[0] == lab[1] == lab[2] != lab[3] == lab[4] == lab[5]


def test_three_clusters_give_three() -> None:
    for seed in range(3):
        gap, s, k = gap_statistic(three_clusters(seed), 5, 10, random.Random(100 + seed))
        assert k == 3
        assert all(x >= 0 for x in s)
        assert gap[2] > gap[1] > gap[0]


def test_uniform_data_gives_one() -> None:
    picks = [gap_statistic(uniform_square(seed), 4, 10, random.Random(100 + seed))[2] for seed in range(10)]
    assert picks.count(1) >= 9
