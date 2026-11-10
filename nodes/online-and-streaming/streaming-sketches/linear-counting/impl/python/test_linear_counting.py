# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-counting/. The authors are listed in prov/738TN4.jsonl.

import hashlib
import math
import random
from fractions import Fraction

from linear_counting import (
    LinearCounter,
    asymptotic_bias,
    asymptotic_standard_error,
    empty_moments,
    estimate_from_empty,
    linear_count,
)


def keyed_hash(seed: int, m: int):
    key = seed.to_bytes(8, "little")

    def h(x: object) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, key=key).digest()
        return int.from_bytes(d, "little") % m

    return h


def occupancy(m: int, n: int, one=1.0) -> list:
    """p[k] = P[exactly k positions are 1] after n distinct items, by dynamic programming."""
    p = [one * 0] * (m + 1)
    p[0] = one
    for _ in range(n):
        q = [one * 0] * (m + 1)
        for k, v in enumerate(p):
            if v:
                q[k] += v * k / m
                if k < m:
                    q[k + 1] += v * (m - k) / m
        p = q
    return p


def test_worked_example() -> None:
    table = {"a": 3, "b": 0, "c": 6, "d": 3, "e": 1, "f": 0}
    est = linear_count("abcadebf", 8, table.__getitem__)
    # Positions 0, 1, 3, 6 are set: U = 4 and the estimate is 8 ln 2.
    assert abs(est - 8 * math.log(2)) < 1e-12
    assert abs(8 * math.log(2) - 5.545) < 1e-3


def test_full_bitmap_gives_infinity() -> None:
    assert estimate_from_empty(4, 0) == math.inf
    assert linear_count(range(4), 4, lambda x: x) == math.inf


def test_exact_moments_of_empty_count() -> None:
    for m in range(1, 7):
        for n in range(0, 9):
            p = occupancy(m, n, Fraction(1))
            eu = sum(v * (m - k) for k, v in enumerate(p))
            vu = sum(v * (m - k) ** 2 for k, v in enumerate(p)) - eu * eu
            mean, var = empty_moments(m, n)
            assert abs(float(eu) - mean) < 1e-9
            assert abs(float(vu) - var) < 1e-9


def test_bias_and_standard_error_against_exact_distribution() -> None:
    # Exact moments of m ln(m / U) from the occupancy distribution (P[U = 0] is negligible here).
    for m, n in [(200, 100), (200, 200), (500, 1000)]:
        p = occupancy(m, n)
        assert p[m] < 1e-12
        vals = [(v, m * math.log(m / (m - k))) for k, v in enumerate(p) if k < m]
        e1 = sum(v * x for v, x in vals)
        e2 = sum(v * x * x for v, x in vals)
        t = n / m
        # The paper's bias (e^t - t - 1) / 2 uses E[U] = m e^(-t); with the exact
        # E[U] = m (1 - 1/m)^n a further t / 2 appears. Tolerance: 5 percent.
        assert abs((e1 - n) - (asymptotic_bias(m, n) + t / 2)) <= 0.05 * (asymptotic_bias(m, n) + t / 2)
        # Standard error of estimate / n: within 4 percent of the formula.
        sd = math.sqrt(e2 - e1 * e1) / n
        assert abs(sd / asymptotic_standard_error(m, n) - 1) < 0.04


def test_seeded_trials_match_standard_error() -> None:
    rng = random.Random(1)
    m, n, trials = 256, 512, 400
    errs = []
    for _ in range(trials):
        errs.append(linear_count(range(n), m, lambda x: rng.randrange(m)) / n - 1)
    se = asymptotic_standard_error(m, n)
    rms = math.sqrt(sum(e * e for e in errs) / trials)
    mean = sum(errs) / trials
    # Tolerance: RMS within 20 percent of the formula; mean within 4 standard errors.
    assert 0.8 * se <= rms <= 1.2 * se
    assert abs(mean) <= 4 * se / math.sqrt(trials) + 0.01


def test_duplicates_and_merge() -> None:
    m = 128
    h = keyed_hash(2, m)
    rng = random.Random(3)
    for _ in range(30):
        xs = [rng.randrange(2000) for _ in range(rng.randrange(150))]
        ys = [rng.randrange(2000) for _ in range(rng.randrange(150))]
        a, b, u = LinearCounter(m, h), LinearCounter(m, h), LinearCounter(m, h)
        a.add_all(xs)
        b.add_all(ys)
        u.add_all(xs + ys + xs)
        mg = a.merge(b)
        assert mg.bitmap == u.bitmap and mg.ones == u.ones
        assert mg.estimate() == u.estimate()
        assert abs(u.estimate() - linear_count(xs + ys, m, h)) < 1e-9 or u.empty() == 0
