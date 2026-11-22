# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/side-channel-key-rank-estimation/. The authors are listed in prov/BD5WM2.jsonl.

import math
import random
from fractions import Fraction

from side_channel_key_rank_estimation import (
    brute_force_rank,
    convolve,
    key_rank_bounds,
    synthetic_scores,
)

A = [0, 3, 5, 9]
B = [0, 2, 7, 8]


def test_worked_example() -> None:
    assert brute_force_rank([A, B], [1, 2]) == 7
    assert key_rank_bounds([A, B], [1, 2], 4) == (4, 16)
    assert key_rank_bounds([A, B], [1, 2], 2) == (4, 11)
    assert key_rank_bounds([A, B], [1, 2], 1) == (5, 8)
    assert key_rank_bounds([A, B], [1, 2], Fraction(1, 2)) == (7, 7)


def test_convolve_counts_sums() -> None:
    rng = random.Random(11)
    for _ in range(200):
        a = [rng.randrange(4) for _ in range(rng.randrange(1, 7))]
        b = [rng.randrange(4) for _ in range(rng.randrange(1, 7))]
        want = [0] * (len(a) + len(b) - 1)
        for i in range(len(a)):
            for j in range(len(b)):
                want[i + j] += a[i] * b[j]
        assert convolve(a, b) == want


def test_bounds_against_enumeration_exact() -> None:
    # Exact rational scores and widths, so no score is rounded across a bin edge.
    rng = random.Random(20240505)
    for _ in range(500):
        d = rng.randrange(1, 4)
        k = rng.randrange(1, 17)
        scores = [[Fraction(rng.randrange(-40, 41), rng.randrange(1, 5)) for _ in range(k)] for _ in range(d)]
        key = [rng.randrange(k) for _ in range(d)]
        width = Fraction(rng.randrange(1, 40), rng.randrange(1, 8))
        rank = brute_force_rank(scores, key)
        lo, up = key_rank_bounds(scores, key, width)
        assert 1 <= lo <= rank <= up <= k ** d


def test_bounds_against_enumeration_synthetic() -> None:
    # Three 4-bit parts, 4096 keys, scores from the Gaussian leakage model.
    rng = random.Random(3)
    for _ in range(12):
        key = [rng.randrange(16) for _ in range(3)]
        scores = synthetic_scores(rng, key, rng.randrange(1, 4), 1.0)
        rank = brute_force_rank(scores, key)
        for bins in (5, 50, 500):
            width = max(max(p) - min(p) for p in scores) / bins
            lo, up = key_rank_bounds(scores, key, width)
            assert lo <= rank <= up


def test_fine_bins_give_the_exact_rank() -> None:
    # If 2 d w is below the smallest gap between distinct totals, lower = upper = rank.
    rng = random.Random(5)
    for _ in range(100):
        d = rng.randrange(1, 4)
        scores = [[Fraction(rng.randrange(1000)) for _ in range(6)] for _ in range(d)]
        key = [rng.randrange(6) for _ in range(d)]
        totals = sorted({sum(c) for c in _products(scores)})
        if len(totals) != 6 ** d:
            continue
        gap = min(y - x for x, y in zip(totals, totals[1:])) if len(totals) > 1 else Fraction(1)
        width = gap / (2 * d + 1)
        rank = brute_force_rank(scores, key)
        assert key_rank_bounds(scores, key, width) == (rank, rank)


def _products(scores):
    out = [[]]
    for part in scores:
        out = [c + [s] for c in out for s in part]
    return out


def test_one_bin_of_slack_is_not_a_bound() -> None:
    # The naive count 1 + #{bin sum > bin of the key} overshoots the true rank here.
    hists, star = [], 0
    for part, k in zip([A, B], [1, 2]):
        idx = [s // 4 for s in part]
        h = [0] * (max(idx) + 1)
        for b in idx:
            h[b] += 1
        hists.append(h)
        star += idx[k]
    total = convolve(hists[0], hists[1])
    assert 1 + sum(total[star + 1:]) == 9 > brute_force_rank([A, B], [1, 2])


def test_64_bit_key_measurement() -> None:
    rng = random.Random(7)
    key = [rng.randrange(16) for _ in range(16)]
    for m in (2, 3):
        synthetic_scores(rng, key, m, 1.0)
    scores = synthetic_scores(rng, key, 4, 1.0)
    span = max(max(p) - min(p) for p in scores)
    got = []
    for bins in (10, 100, 1000):
        lo, up = key_rank_bounds(scores, key, span / bins)
        assert lo <= up <= 16 ** 16
        got.append((round(math.log2(lo), 2), round(math.log2(up), 2)))
    assert got == [(0.0, 58.11), (23.98, 36.21), (29.8, 31.02)]


def test_one_part() -> None:
    scores = [[0.5, 2.5, 1.5, 4.0]]
    assert brute_force_rank(scores, [2]) == 3
    assert key_rank_bounds(scores, [2], 0.25) == (3, 3)
    assert key_rank_bounds(scores, [3], 1.0) == (1, 1)
