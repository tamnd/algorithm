# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-confidence-interval/. The authors are listed in prov/W2JAG5.jsonl.

import math
import random

import pytest

from stdist import t_sf
from t_confidence_interval import t_interval

SLEEP_DIFFERENCES = [1.2, 2.4, 1.3, 1.3, 0.0, 1.0, 1.8, 0.8, 4.6, 1.4]
R = 4000
SE4 = 4.0 * math.sqrt(0.05 * 0.95 / R)  # four standard errors of a coverage near 0.95


def test_sleep_data() -> None:
    lo, hi = t_interval(SLEEP_DIFFERENCES)
    # 1.58 -+ t_(9, 0.975) * 0.388959..., with t_(9, 0.975) = 2.262157...
    assert abs(lo - 0.7001) < 1e-4 and abs(hi - 2.4599) < 1e-4
    assert abs((lo + hi) / 2 - 1.58) < 1e-12


def test_closed_form_quantiles() -> None:
    # nu = 1 is the Cauchy law: t_(1, p) = tan(pi (p - 1/2)). With n = 2, S = |x1 - x2| / sqrt(2),
    # so the 95% interval is the mean -+ tan(0.475 pi) |x1 - x2| / 2.
    lo, hi = t_interval([3.0, 7.0])
    q1 = math.tan(0.475 * math.pi)
    assert abs(q1 - 12.706204736174698) < 1e-9
    assert abs(lo - (5.0 - 2.0 * q1)) < 1e-9 and abs(hi - (5.0 + 2.0 * q1)) < 1e-9
    # nu = 2: t_(2, p) = (2p - 1) / sqrt(2 p (1 - p)).
    lo, hi = t_interval([1.0, 2.0, 6.0], confidence=0.9)
    q2 = 0.9 / math.sqrt(2 * 0.95 * 0.05)
    se = math.sqrt(7.0 / 3.0)  # S^2 = 7 with divisor n - 1 = 2
    assert abs(hi - lo - 2.0 * q2 * se) < 1e-9


def test_duality_with_the_t_test() -> None:
    rng = random.Random(21)
    for _ in range(30):
        n = rng.randint(2, 15)
        x = [rng.gauss(10.0, 3.0) for _ in range(n)]
        lo, hi = t_interval(x, 0.95)
        mean = sum(x) / n
        se = math.sqrt(sum((v - mean) ** 2 for v in x) / (n - 1) / n)
        p = lambda mu0: 2.0 * t_sf(abs(mean - mu0) / se, n - 1)
        # At the end points the two-sided p-value is alpha; inside it is larger, outside smaller.
        assert abs(p(lo) - 0.05) < 1e-9 and abs(p(hi) - 0.05) < 1e-9
        assert p((lo + hi) / 2) > 0.05
        assert p(hi + 0.01 * (hi - lo)) < 0.05


def test_one_sided_bounds() -> None:
    rng = random.Random(22)
    x = [rng.gauss(0.0, 1.0) for _ in range(12)]
    lo90, hi90 = t_interval(x, 0.90)
    lower, inf = t_interval(x, 0.95, "lower")
    minf, upper = t_interval(x, 0.95, "upper")
    assert inf == math.inf and minf == -math.inf
    # A 95% one-sided bound is an end point of the 90% two-sided interval.
    assert abs(lower - lo90) < 1e-12 and abs(upper - hi90) < 1e-12


def test_equivariance() -> None:
    rng = random.Random(23)
    x = [rng.gauss(0.0, 1.0) for _ in range(9)]
    lo, hi = t_interval(x)
    lo2, hi2 = t_interval([3.0 - 2.5 * v for v in x])
    assert abs(lo2 - (3.0 - 2.5 * hi)) < 1e-12 and abs(hi2 - (3.0 - 2.5 * lo)) < 1e-12


def coverage(draw, mu: float, n: int, side: str, seed: int) -> float:
    rng = random.Random(seed)
    hits = 0
    for _ in range(R):
        lo, hi = t_interval([draw(rng) for _ in range(n)], 0.95, side)
        hits += lo <= mu <= hi
    return hits / R


def test_exact_coverage_for_normal_data() -> None:
    for n, seed in ((2, 1), (5, 2), (20, 3)):
        assert abs(coverage(lambda g: g.gauss(4.0, 2.0), 4.0, n, "two-sided", seed) - 0.95) < SE4
    assert abs(coverage(lambda g: g.gauss(4.0, 2.0), 4.0, 5, "upper", 4) - 0.95) < SE4


def test_under_coverage_for_skewed_data() -> None:
    # Exponential data with mean 1, n = 5: only asymptotic. The two-sided coverage is about 0.88,
    # the upper bound covers about 0.85 and the lower bound about 0.99.
    expo = lambda g: g.expovariate(1.0)
    assert coverage(expo, 1.0, 5, "two-sided", 5) < 0.95 - SE4
    assert coverage(expo, 1.0, 5, "upper", 6) < 0.95 - SE4
    assert coverage(expo, 1.0, 5, "lower", 7) > 0.95 + SE4


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        t_interval([1.0])
    with pytest.raises(ValueError):
        t_interval([1.0, 2.0], confidence=1.0)
    with pytest.raises(ValueError):
        t_interval([1.0, 2.0], side="both")
