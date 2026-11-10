# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/count-min-sketch/. The authors are listed in prov/4BWT77.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction
from itertools import combinations

import pytest

from count_min_sketch import CountMinSketch, DyadicCountMin


def zipf_counts(rng: random.Random, n: int, total: int) -> Counter:
    weights = [1 / (i + 1) for i in range(n)]
    return Counter(rng.choices(range(n), weights=weights, k=total))


def test_sizes_from_error() -> None:
    sk = CountMinSketch.from_error(0.1, 0.1, random.Random(0))
    assert (sk.w, sk.d) == (28, 3)
    sk = CountMinSketch.from_error(0.01, 0.01, random.Random(0))
    assert (sk.w, sk.d) == (272, 5)
    with pytest.raises(ValueError):
        CountMinSketch.from_error(0.1, 1, random.Random(0))


def test_hash_family_is_universal_exactly() -> None:
    # The family ((a x + b) mod p) mod w with a != 0, enumerated for p = 31, w = 5.
    p, w = 31, 5
    for x, y in combinations(range(p), 2):
        coll = sum(((a * x + b) % p) % w == ((a * y + b) % p) % w for a in range(1, p) for b in range(p))
        assert Fraction(coll, (p - 1) * p) <= Fraction(1, w)


def test_example() -> None:
    sk = CountMinSketch(4, 2, random.Random(0), prime=31)
    sk.hashes = [(1, 0), (7, 0)]  # h1(x) = x mod 4, h2(x) = (7x mod 31) mod 4
    for x, c in [(1, 3), (2, 2), (5, 1), (6, 4)]:
        sk.update(x, c)
    assert sk.table == [[0, 4, 6, 0], [1, 0, 2, 7]]
    assert [sk.estimate(x) for x in (1, 2, 5, 6, 9)] == [4, 2, 1, 6, 0]


def test_never_too_small_and_conservative_dominated() -> None:
    rng = random.Random(1)
    for trial in range(30):
        cm = CountMinSketch(rng.randrange(1, 12), rng.randrange(1, 5), rng)
        cu = cm.empty_like()
        freq = Counter()
        for _ in range(200):
            x, c = rng.randrange(40), rng.randrange(1, 4)
            cm.update(x, c)
            cu.update_conservative(x, c)
            freq[x] += c
            for j in range(cm.d):
                assert all(u <= v for u, v in zip(cu.table[j], cm.table[j]))
        for x in range(40):
            assert freq[x] <= cu.estimate(x) <= cm.estimate(x)
        # Each row of a plain sketch adds up to ||f||_1.
        assert all(sum(row) == sum(freq.values()) == cm.total for row in cm.table)


def test_linear_merge_subtract_and_turnstile() -> None:
    rng = random.Random(2)
    base = CountMinSketch(16, 4, rng)
    a, b, ab = base.empty_like(), base.empty_like(), base.empty_like()
    s1 = [(rng.randrange(100), rng.randrange(-3, 6)) for _ in range(300)]
    s2 = [(rng.randrange(100), rng.randrange(-3, 6)) for _ in range(300)]
    for x, c in s1:
        a.update(x, c)
        ab.update(x, c)
    for x, c in s2:
        b.update(x, c)
        ab.update(x, c)
    assert a.merge(b).table == ab.table
    assert ab.subtract(b).table == a.table
    # Insert, then delete all: the sketch is zero again.
    z = base.empty_like()
    for x, c in s1:
        z.update(x, c)
    for x, c in s1:
        z.update(x, -c)
    assert all(v == 0 for row in z.table for v in row)
    # Merging conservative sketches by addition keeps both bounds.
    cu1, cu2, cm12 = base.empty_like(), base.empty_like(), base.empty_like()
    f = Counter()
    for i in range(400):
        x = rng.randrange(60)
        (cu1 if i % 2 else cu2).update_conservative(x)
        cm12.update(x)
        f[x] += 1
    m = cu1.merge(cu2)
    for x in range(60):
        assert f[x] <= m.estimate(x) <= cm12.estimate(x)


def test_failure_rate_at_most_delta() -> None:
    eps, delta = 0.1, 0.1
    trials = 200
    n = 300
    rate_sum = 0.0
    for seed in range(trials):
        rng = random.Random(seed)
        freq = zipf_counts(rng, n, 3000)
        sk = CountMinSketch.from_error(eps, delta, rng)
        for x, c in freq.items():
            sk.update(x, c)
        l1 = sum(freq.values())
        fails = sum(sk.estimate(x) - freq[x] > eps * l1 for x in range(n))
        rate_sum += fails / n
    rate = rate_sum / trials
    # Each per-trial rate is in [0, 1] with mean <= e^-3 < delta.
    assert rate <= delta + 3 * math.sqrt(delta * (1 - delta) / trials)
    assert rate <= math.exp(-3) + 3 * math.sqrt(delta * (1 - delta) / trials)


def test_dyadic_cover_and_range_queries() -> None:
    levels = 6
    for lo in range(1 << levels):
        for hi in range(lo, 1 << levels, 5):
            cover = DyadicCountMin.dyadic_cover(lo, hi)
            assert len(cover) <= 2 * levels
            pts = [x for lev, i in cover for x in range(i << lev, (i + 1) << lev)]
            assert pts == list(range(lo, hi + 1))
    rng = random.Random(5)
    eps, delta = 0.05, 0.01
    w, d = math.ceil(math.e / eps), math.ceil(math.log(1 / delta))
    bad = 0
    queries = 0
    for _ in range(10):
        dy = DyadicCountMin(levels, w, d, rng)
        freq = Counter(rng.randrange(1 << levels) for _ in range(500))
        for x, c in freq.items():
            dy.update(x, c)
        l1 = sum(freq.values())
        for _ in range(50):
            lo = rng.randrange(1 << levels)
            hi = rng.randrange(lo, 1 << levels)
            true = sum(freq[x] for x in range(lo, hi + 1))
            est = dy.range_query(lo, hi)
            assert est >= true
            queries += 1
            bad += est - true > 2 * levels * eps * l1
    assert bad / queries <= 2 * levels * delta + 0.05
