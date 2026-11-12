# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram/. The authors are listed in prov/R1T161.jsonl.

import random
from collections import Counter
from fractions import Fraction
from itertools import combinations

from histogram import EndBiased, Histogram, exact_range, v_optimal_partition


def brute_v_optimal(f, B):
    """Try every choice of at most B - 1 cut points."""
    n, best = len(f), None
    for k in range(0, min(B, n)):
        for cuts in combinations(range(1, n), k):
            bounds = (0,) + cuts + (n,)
            err = Fraction(0)
            for i, j in zip(bounds, bounds[1:]):
                part = f[i:j]
                m = Fraction(sum(part), len(part))
                err += sum((x - m) ** 2 for x in part)
            if best is None or err < best:
                best = err
    return best


def group_error(f, groups):
    err = Fraction(0)
    for i, j in groups:
        m = Fraction(sum(f[i:j]), j - i)
        err += sum((x - m) ** 2 for x in f[i:j])
    return err


def test_worked_example():
    f = [5, 6, 4, 20, 3, 4, 5, 6]  # frequencies of the values 1..8
    err, groups = v_optimal_partition(f, 3)
    assert groups == [(0, 3), (3, 4), (4, 8)] and err == 7
    assert group_error(f, [(0, 3), (3, 6), (6, 8)]) == Fraction(369, 2)  # equal widths
    vals = [i + 1 for i, c in enumerate(f) for _ in range(c)]
    ew, ed, vo = Histogram.equi_width(vals, 3), Histogram.equi_depth(vals, 3), Histogram.v_optimal(vals, 3)
    assert ew.buckets == [(1, 3, 15, 3), (4, 6, 27, 3), (7, 8, 11, 2)]
    assert ed.buckets == [(1, 4, 18, 4), (4, 5, 18, 2), (5, 8, 17, 4)]
    assert vo.buckets == [(1, 3, 15, 3), (4, 4, 20, 1), (5, 8, 18, 4)]
    assert (ew.estimate_eq(4), ed.estimate_eq(4), vo.estimate_eq(4)) == (9, Fraction(27, 2), 20)
    assert exact_range(vals, 4, 5) == 23
    assert (ew.estimate_range(4, 5), ed.estimate_range(4, 5), vo.estimate_range(4, 5)) == (18, Fraction(107, 4), Fraction(49, 2))


def test_v_optimal_against_brute_force():
    rng = random.Random(2024)
    for _ in range(700):
        n = rng.randrange(1, 9)
        f = [rng.randrange(1, 12) for _ in range(n)]
        B = rng.randrange(1, 5)
        err, groups = v_optimal_partition(f, B)
        assert err == brute_v_optimal(f, B)
        assert group_error(f, groups) == err
        assert len(groups) == min(B, n) and groups[0][0] == 0 and groups[-1][1] == n
        assert all(i < j for i, j in groups)


def test_v_optimal_beats_equi_width_and_equi_depth():
    rng = random.Random(8)
    for _ in range(300):
        vals = [rng.randrange(12) for _ in range(rng.randrange(1, 40))]
        B = rng.randrange(1, 5)
        freq = [c for _, c in sorted(Counter(vals).items())]
        err, _ = v_optimal_partition(freq, B)
        h = Histogram.v_optimal(vals, B)
        h.check_invariant(vals)
        # any split of the same distinct values into <= B groups has error >= err
        dvals = sorted(set(vals))
        for other in (Histogram.equi_width(vals, B), Histogram.equi_depth(vals, B)):
            groups, k = [], 0
            for lo, hi, _, _ in other.buckets:
                idx = [i for i, v in enumerate(dvals) if lo <= v <= hi and i >= k]
                if idx:
                    groups.append((idx[0], idx[-1] + 1))
                    k = idx[-1] + 1
            if len(groups) <= B and sum(j - i for i, j in groups) == len(dvals):
                assert group_error(freq, groups) >= err


def test_equi_depth_range_error_bound():
    rng = random.Random(77)
    for _ in range(600):
        N = rng.randrange(1, 60)
        skew = rng.random() < 0.5
        vals = [min(rng.randrange(30), rng.randrange(30)) if skew else rng.randrange(30) for _ in range(N)]
        B = rng.randrange(1, 8)
        h = Histogram.equi_depth(vals, B)
        h.check_invariant(vals)
        d = -(-N // B)
        assert all(c <= d for _, _, c, _ in h.buckets)
        for _ in range(10):
            a = rng.randrange(-2, 32)
            b = rng.randrange(a, 33)
            assert abs(h.estimate_range(a, b) - exact_range(vals, a, b)) <= 2 * d
        assert h.estimate_range(-10, 100) == N


def test_equi_width_exact_on_uniform_data():
    vals = [v for v in range(20) for _ in range(3)]
    h = Histogram.equi_width(vals, 4)
    h.check_invariant(vals)
    assert [b[:3] for b in h.buckets] == [(0, 4, 15), (5, 9, 15), (10, 14, 15), (15, 19, 15)]
    for a in range(20):
        for b in range(a, 20):
            assert h.estimate_range(a, b) == exact_range(vals, a, b)
    assert h.estimate_eq(7) == 3


def test_end_biased():
    vals = [1] * 50 + [2] * 3 + [3] * 2 + [4] * 3 + [5] * 2 + [6] * 40
    eb = EndBiased(vals, 3)
    assert eb.estimate_eq(1) == 50 and eb.estimate_eq(6) == 40
    assert eb.estimate_eq(2) == Fraction(10, 4) and eb.estimate_eq(9) == 0
    rng = random.Random(4)
    for _ in range(200):
        vals = [rng.randrange(8) for _ in range(rng.randrange(1, 40))]
        eb = EndBiased(vals, rng.randrange(1, 5))
        cnt = Counter(vals)
        assert sum(eb.estimate_eq(v) for v in cnt) == len(vals)


def test_edges():
    assert Histogram.equi_depth([], 3).buckets == []
    assert Histogram.v_optimal([], 3).buckets == []
    h = Histogram.v_optimal([5, 5, 5], 4)
    assert h.buckets == [(5, 5, 3, 1)]
    assert h.estimate_eq(5) == 3 and h.estimate_eq(4) == 0
    assert v_optimal_partition([7], 3) == (0, [(0, 1)])
