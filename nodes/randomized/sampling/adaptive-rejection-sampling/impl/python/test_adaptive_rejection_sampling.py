# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-rejection-sampling/. The authors are listed in prov/7A5KY6.jsonl.

import math
import random

import pytest

from adaptive_rejection_sampling import ARS


def h_norm(x):
    return -0.5 * x * x


def dh_norm(x):
    return -x


def phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def ks_statistic(xs, cdf) -> float:
    xs = sorted(xs)
    m = len(xs)
    d = 0.0
    for i, x in enumerate(xs):
        c = cdf(x)
        d = max(d, (i + 1) / m - c, c - i / m)
    return d


def ks_threshold(m: int, alpha: float = 1e-9) -> float:
    # Dvoretzky-Kiefer-Wolfowitz with Massart's constant: Pr[D > t] <= 2 exp(-2 m t^2).
    return math.sqrt(math.log(2.0 / alpha) / (2.0 * m))


def test_example_hulls() -> None:
    # For h(x) = -x^2 / 2 the tangents at a and b meet at (a + b) / 2.
    s = ARS(h_norm, dh_norm, [-1.0, 0.5, 2.0])
    assert s.z[0] == -math.inf and s.z[-1] == math.inf
    assert abs(s.z[1] + 0.25) < 1e-12 and abs(s.z[2] - 1.25) < 1e-12
    for i in range(-60, 61):
        t = i / 10
        assert s.lower(t) <= h_norm(t) + 1e-12
        assert h_norm(t) <= s.upper(t) + 1e-12
    # The tangent at -1 is 1/2 + x; the chord from (-1, -1/2) to (1/2, -1/8) is -1/4 at 0.
    assert abs(s.upper(-0.5) - 0.0) < 1e-12
    assert abs(s.lower(0.0) + 0.25) < 1e-12
    assert s.lower(-1.5) == -math.inf and s.lower(2.5) == -math.inf


def test_hull_sampler_is_laplace() -> None:
    # T = {-1, 1}: u(x) = 1/2 - |x|, so s_T is the Laplace density.
    s = ARS(h_norm, dh_norm, [-1.0, 1.0])
    rng = random.Random(1)
    m = 40000
    xs = [s._sample_hull(rng) for _ in range(m)]

    def laplace(t):
        return 0.5 * math.exp(t) if t < 0 else 1 - 0.5 * math.exp(-t)

    assert ks_statistic(xs, laplace) < ks_threshold(m)


def test_normal_ks_and_few_evaluations() -> None:
    rng = random.Random(1992)
    s = ARS(h_norm, dh_norm, [-1.0, 1.0])
    m = 40000
    xs = s.sample(m, rng)
    assert ks_statistic(xs, phi) < ks_threshold(m)
    assert s.evals < 200  # the hull gets tight fast: h is evaluated for under 0.5% of outputs


def test_gamma_on_half_line() -> None:
    # Gamma(3, 1): h(x) = 2 ln x - x on (0, inf).
    rng = random.Random(7)
    s = ARS(lambda x: 2 * math.log(x) - x, lambda x: 2 / x - 1, [1.0, 4.0], lo=0.0)
    m = 40000
    xs = s.sample(m, rng)

    def cdf(t):
        return 0.0 if t <= 0 else 1 - math.exp(-t) * (1 + t + t * t / 2)

    assert min(xs) > 0
    assert ks_statistic(xs, cdf) < ks_threshold(m)
    assert abs(sum(xs) / m - 3.0) < 6 * math.sqrt(3.0 / m)


def first_draws(update_first: bool, m: int, rng) -> list:
    """The first output of m fresh samplers that start from T = {-1, 1}."""
    out = []
    for _ in range(m):
        s = ARS(h_norm, dh_norm, [-1.0, 1.0])
        if not update_first:
            out.append(s.sample(1, rng)[0])
            continue
        # Wrong order: add X to T, then test against the new hull.
        while True:
            t = s._sample_hull(rng)
            w = rng.random()
            if w <= math.exp(s.lower(t) - s.upper(t)):
                out.append(t)
                break
            s._add(t)
            s._build()
            if w <= math.exp(h_norm(t) - s.upper(t)):
                out.append(t)
                break
    return out


def test_first_draw_is_exact_and_wrong_order_fails() -> None:
    m = 20000
    good = first_draws(False, m, random.Random(3))
    assert ks_statistic(good, phi) < ks_threshold(m)
    bad = first_draws(True, m, random.Random(4))
    assert ks_statistic(bad, phi) > ks_threshold(m)


def test_errors() -> None:
    with pytest.raises(ValueError):
        ARS(h_norm, dh_norm, [0.5, 2.0])
    with pytest.raises(ValueError):
        ARS(h_norm, dh_norm, [-2.0, -0.5])
