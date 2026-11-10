# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/count-sketch/. The authors are listed in prov/2S6HW2.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction
from itertools import combinations, product

import pytest

from count_sketch import CountSketch, parity_sign


def zipf_counts(rng: random.Random, n: int, total: int) -> Counter:
    weights = [1 / (i + 1) for i in range(n)]
    return Counter(rng.choices(range(n), weights=weights, k=total))


def test_sizes_from_error() -> None:
    sk = CountSketch.from_error(0.1, 0.1, random.Random(0))
    assert (sk.w, sk.d) == (300, 42)
    sk = CountSketch.from_error(0.25, 0.2, random.Random(0))
    assert (sk.w, sk.d) == (48, 29)
    with pytest.raises(ValueError):
        CountSketch.from_error(0.1, 0, random.Random(0))


def test_sign_family_is_pairwise_independent_exactly() -> None:
    bits = 3
    fam = [(a, b) for a in range(1 << bits) for b in range(2)]
    for x, y in combinations(range(1 << bits), 2):
        joint = Counter((parity_sign(a, b, x), parity_sign(a, b, y)) for a, b in fam)
        assert joint == {(1, 1): 4, (1, -1): 4, (-1, 1): 4, (-1, -1): 4}


def test_row_estimate_unbiased_and_variance_bound_exactly() -> None:
    # Enumerate every bucket hash ((a x + b) mod 5) mod 2 and every sign over 3 bits.
    p, w = 5, 2
    buckets = [(a, b) for a in range(1, p) for b in range(p)]
    signs = [(a, b) for a in range(8) for b in range(2)]
    for x, y in combinations(range(p), 2):
        coll = sum(((a * x + b) % p) % w == ((a * y + b) % p) % w for a, b in buckets)
        assert Fraction(coll, len(buckets)) <= Fraction(1, w)
    rng = random.Random(3)
    for _ in range(5):
        f = [rng.randrange(-4, 7) for _ in range(p)]
        f2 = sum(v * v for v in f)
        for x in range(p):
            vals = []
            for (a, b), (sa, sb) in product(buckets, signs):
                hx = ((a * x + b) % p) % w
                cell = sum(parity_sign(sa, sb, y) * f[y] for y in range(p) if ((a * y + b) % p) % w == hx)
                vals.append(parity_sign(sa, sb, x) * cell)
            n = len(vals)
            mean = Fraction(sum(vals), n)
            var = Fraction(sum(v * v for v in vals), n) - mean * mean
            assert mean == f[x]
            assert var <= Fraction(f2 - f[x] ** 2, w)


def make_example() -> CountSketch:
    sk = CountSketch(3, 3, random.Random(0), prime=31)
    sk.buckets = [(1, 0), (2, 0), (13, 0)]
    sk.signs = [(1, 0), (2, 0), (1, 1)]
    for x, c in [(1, 5), (2, 3), (3, 1), (4, 1)]:
        sk.update(x, c)
    return sk


def test_example() -> None:
    sk = make_example()
    assert sk.table == [[-1, -4, 3], [-1, -3, 6], [-1, 5, -2]]
    assert sk.row_estimates(1) == [4, 6, 5]
    assert sk.row_estimates(7) == [4, -6, -2]
    assert [sk.estimate(x) for x in (1, 2, 3, 4, 7)] == [5, 3, 1, 1, -2]


def test_linear_merge_subtract_and_turnstile() -> None:
    rng = random.Random(2)
    base = CountSketch(16, 5, rng)
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
    z = base.empty_like()
    for x, c in s1:
        z.update(x, c)
    for x, c in s1:
        z.update(x, -c)
    assert all(v == 0 for row in z.table for v in row)
    with pytest.raises(ValueError):
        a.merge(CountSketch(16, 5, random.Random(99)))


def test_row_failure_at_most_one_third() -> None:
    # One row with w = ceil(3/eps^2): Pr[|error| > eps ||f||_2] <= 1/3 by Chebyshev.
    eps = 0.3
    w = math.ceil(3 / eps**2)
    trials, n = 300, 150
    rate_sum = 0.0
    for seed in range(trials):
        rng = random.Random(seed)
        f = zipf_counts(rng, n, 1500)
        for x in range(0, n, 7):
            f[x] -= 3  # some negative counts: the general turnstile model
        sk = CountSketch(w, 1, rng)
        for x, c in f.items():
            sk.update(x, c)
        l2 = math.sqrt(sum(v * v for v in f.values()))
        rate_sum += sum(abs(sk.estimate(x) - f[x]) > eps * l2 for x in range(n)) / n
    rate = rate_sum / trials
    assert rate <= 1 / 3 + 3 * math.sqrt((1 / 3) * (2 / 3) / trials)


def test_median_failure_at_most_delta() -> None:
    eps, delta = 0.25, 0.2
    trials, n = 40, 80
    rate_sum = 0.0
    for seed in range(trials):
        rng = random.Random(1000 + seed)
        f = zipf_counts(rng, n, 1000)
        sk = CountSketch.from_error(eps, delta, rng)
        for x, c in f.items():
            sk.update(x, c)
        l2 = math.sqrt(sum(v * v for v in f.values()))
        rate_sum += sum(abs(sk.estimate(x) - f[x]) > eps * l2 for x in range(n)) / n
    rate = rate_sum / trials
    assert rate <= delta + 3 * math.sqrt(delta * (1 - delta) / trials)


def test_tail_bound_for_one_row() -> None:
    # For k <= w/6: Pr[|error| > sqrt(6/w) * ||f_res(k)||_2] <= 1/3.
    w = 60
    k = w // 6
    trials, n = 200, 200
    rate_sum = 0.0
    for seed in range(trials):
        rng = random.Random(5000 + seed)
        f = zipf_counts(rng, n, 4000)
        sk = CountSketch(w, 1, rng)
        for x, c in f.items():
            sk.update(x, c)
        tail = sorted((v * v for v in f.values()), reverse=True)[k:]
        t = math.sqrt(6 / w) * math.sqrt(sum(tail))
        rate_sum += sum(abs(sk.estimate(x) - f[x]) > t for x in range(n)) / n
    rate = rate_sum / trials
    assert rate <= 1 / 3 + 3 * math.sqrt((1 / 3) * (2 / 3) / trials)
