# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-hashing-max-load-bound/. The authors are listed in prov/E7P3Z6.jsonl.

import math
import random
from fractions import Fraction

from consistent_hashing_max_load_bound import (expected_max_gap_exact, gamma_tail_bound, harmonic, key_loads,
                                               lower_failure_bound, lower_threshold, max_gap,
                                               prob_max_gap_exceeds, prob_min_gap_exceeds, ring_points,
                                               ring_shares, share_failure_bound, share_window,
                                               shares_from_points, upper_failure_bound, upper_threshold,
                                               vnodes_needed)


def brute_shares(pts, n):
    """Share of each server: for each point, the clockwise distance from the nearest point before it."""
    shares = [0.0] * n
    for p, s in pts:
        gaps = [(p - q) % 1.0 for q, _ in pts if q != p]
        shares[s] += min(gaps) if gaps else 1.0
    return shares


def brute_owner(pts, x):
    """Server of the point with the least clockwise distance from x."""
    return min(pts, key=lambda ps: (ps[0] - x) % 1.0)[1]


def test_shares_partition_the_circle() -> None:
    rng = random.Random(1)
    for n, v in ((1, 1), (2, 1), (7, 3), (12, 5)):
        pts = ring_points(n, v, rng)
        sh = shares_from_points(pts, n)
        assert len(sh) == n and min(sh) >= 0
        assert math.isclose(sum(sh), 1.0)
        for a, b in zip(sh, brute_shares(pts, n)):
            assert math.isclose(a, b, abs_tol=1e-12)


def test_key_loads_match_a_linear_scan() -> None:
    rng = random.Random(2)
    n = 5
    pts = ring_points(n, 4, rng)
    keys = [rng.random() for _ in range(2000)]
    loads = key_loads(pts, n, keys)
    ref = [0] * n
    for x in keys:
        ref[brute_owner(pts, x)] += 1
    assert loads == ref and sum(loads) == len(keys)


def test_exact_law_of_the_largest_arc() -> None:
    for n in range(1, 31):
        assert expected_max_gap_exact(n) == harmonic(n) / n
    assert expected_max_gap_exact(2) == Fraction(3, 4)
    assert expected_max_gap_exact(3) == Fraction(11, 18)
    assert prob_max_gap_exceeds(3, Fraction(1, 2)) == Fraction(3, 4)
    assert prob_max_gap_exceeds(3, Fraction(2, 5)) == Fraction(24, 25)
    # n = 2: the largest of two arcs exceeds x in [1/2, 1) with probability 2 (1 - x)
    for x in (Fraction(1, 2), Fraction(3, 5), Fraction(9, 10)):
        assert prob_max_gap_exceeds(2, x) == 2 * (1 - x)
    # a tail: 1 at 0, 0 at 1, nonincreasing between
    n = 6
    grid = [Fraction(j, 60) for j in range(61)]
    tail = [prob_max_gap_exceeds(n, x) for x in grid]
    assert tail[0] == 1 and tail[-1] == 0
    assert all(a >= b for a, b in zip(tail, tail[1:]))
    # every arc is at least 1/n of the circle on average, so the largest is at least 1/n
    assert prob_max_gap_exceeds(n, Fraction(1, n)) == 1


def test_exact_law_against_simulation() -> None:
    rng = random.Random(3)
    n, runs = 5, 4000
    largest, smallest = [], []
    for _ in range(runs):
        sh = ring_shares(n, 1, rng)
        largest.append(max(sh))
        smallest.append(min(sh))
    assert abs(sum(largest) / runs - float(harmonic(n) / n)) < 0.01
    assert abs(sum(smallest) / runs - 1 / n ** 2) < 0.005
    for x in (0.3, 0.4, 0.5, 0.6):
        observed = sum(g > x for g in largest) / runs
        assert abs(observed - prob_max_gap_exceeds(n, x)) < 0.03
    for x in (0.02, 0.05, 0.1):
        observed = sum(g > x for g in smallest) / runs
        assert abs(observed - prob_min_gap_exceeds(n, x)) < 0.03


def test_bounds_hold_against_the_exact_law() -> None:
    n = 40
    for j in range(1, 40):
        x = Fraction(j, 4 * n)
        tail = prob_max_gap_exceeds(n, x)
        assert tail <= upper_failure_bound(n, float(x)) + 1e-12
        assert 1 - tail <= lower_failure_bound(n, float(x)) + 1e-12


def test_largest_arc_over_seeds_is_within_the_bound() -> None:
    n = 1000
    hi, lo = upper_threshold(n, 1), lower_threshold(n, 0.5)
    assert upper_failure_bound(n, hi) <= 1 / n
    assert lower_failure_bound(n, lo) <= math.e / math.sqrt(n)
    ratios = []
    for seed in range(60):
        g = max_gap(n, random.Random(seed))
        assert lo < g <= hi
        ratios.append(n * g)
    # the mean of n times the largest arc is H_n = 7.485 for n = 1000
    assert abs(sum(ratios) / len(ratios) - float(harmonic(n))) < 0.6


def test_virtual_nodes_keep_every_share_in_the_window() -> None:
    for n, delta, seeds in ((100, 0.5, 5), (50, 0.25, 3)):
        v = vnodes_needed(n, delta, 1)
        assert share_failure_bound(n, v, delta) <= 1 / n
        lo, hi = share_window(n, delta)
        for seed in range(seeds):
            sh = ring_shares(n, v, random.Random(100 + seed))
            assert lo <= min(sh) and max(sh) <= hi
    assert vnodes_needed(100, 0.5, 1) == 159 and vnodes_needed(1000, 0.5, 1) == 233


def test_chernoff_bounds_for_the_gamma_sums() -> None:
    for v in (1, 4, 16, 64, 256, 1024):
        for delta in (0.05, 0.1, 0.25, 0.5, 0.75, 0.99):
            assert gamma_tail_bound(v, delta) <= 2 * math.exp(-v * delta * delta / 4) + 1e-15
    for n in (10, 100, 10 ** 4):
        for delta in (0.1, 0.5):
            for c in (0.5, 1.0, 2.0):
                v = vnodes_needed(n, delta, c)
                assert share_failure_bound(n, v, delta) <= n ** -c * (1 + 1e-9)
                assert 2 * n * math.exp(-(v - 1) * delta * delta / 4) > n ** -c


def test_key_loads_follow_the_shares() -> None:
    rng = random.Random(7)
    n, m = 20, 20000
    v = vnodes_needed(n, 0.5, 1)
    pts = ring_points(n, v, rng)
    sh = shares_from_points(pts, n)
    loads = key_loads(pts, n, [rng.random() for _ in range(m)])
    assert sum(loads) == m
    lo, hi = share_window(n, 0.5)
    assert max(loads) <= 1.5 * hi * m  # the theorem with eps = 1/2
    assert max(loads) <= 1.2 * max(sh) * m  # Chernoff given the actual shares
