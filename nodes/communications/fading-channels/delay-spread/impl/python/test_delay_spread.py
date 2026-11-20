# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-spread/. The authors are listed in prov/T38XE2.jsonl.

import math
import random
from fractions import Fraction

from delay_spread import (
    db_to_linear,
    delay_moments,
    frequency_correlation,
    max_excess_delay,
    rms_delay_spread,
)

# 3GPP TS 36.104, Annex B.2: delays in ns, powers in dB.
EPA = ([0, 30, 70, 90, 110, 190, 410], [0, -1, -2, -3, -8, -17.2, -20.8])
EVA = ([0, 30, 150, 310, 370, 710, 1090, 1730, 2510], [0, -1.5, -1.4, -3.6, -0.6, -9.1, -7, -12, -16.9])
ETU = ([0, 50, 120, 200, 230, 500, 1600, 2300, 5000], [-1, -1, -1, 0, 0, 0, -3, -5, -7])


def test_four_tap_exact() -> None:
    p = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)]
    d = [0, 1, 2, 4]
    mu, var = delay_moments(d, p)
    assert mu == 1 and var == Fraction(7, 4)
    assert abs(rms_delay_spread(d, p)[1] - 1.3228756555) < 1e-9
    pf = [float(x) for x in p]
    assert max_excess_delay(d, pf, 10) == 4
    assert max_excess_delay(d, pf, 5) == 1


def test_two_equal_taps() -> None:
    mu, var = delay_moments([0, 1], [1, 1])
    assert mu == Fraction(1, 2) and var == Fraction(1, 4)
    # |R| = |cos(pi df)| equals Fleury's bound cos(2 pi sigma df) with sigma = 1/2.
    for k in range(1, 50):
        df = k / 100
        assert abs(abs(frequency_correlation([0, 1], [1, 1], df)) - math.cos(math.pi * df)) < 1e-12


def test_exponential_profile() -> None:
    # A fine sampling of exp(-t) on [0, 40] gives mean and spread close to 1.
    h = 0.001
    d = [(i + 0.5) * h for i in range(40000)]
    p = [math.exp(-t) for t in d]
    mu, s = rms_delay_spread(d, p)
    assert abs(mu - 1) < 1e-4 and abs(s - 1) < 1e-4


def test_3gpp_profiles() -> None:
    for (d, pdb), mean, rms in ((EPA, 44.20, 43), (EVA, 253.92, 357), (ETU, 561.24, 991)):
        mu, s = rms_delay_spread(d, db_to_linear(pdb))
        assert abs(mu - mean) < 0.01
        assert round(s) == rms


def test_dB_weights_are_wrong() -> None:
    d, pdb = EPA
    wrong = rms_delay_spread(d, [-x + 21 for x in pdb])[1]
    assert abs(wrong - 43) > 10


def test_shift_and_scale() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 8)
        d = [Fraction(rng.randint(0, 1000)) for _ in range(n)]
        p = [Fraction(rng.randint(1, 100)) for _ in range(n)]
        mu, var = delay_moments(d, p)
        c, a = Fraction(rng.randint(-500, 500)), Fraction(rng.randint(1, 9), rng.randint(1, 9))
        mu2, var2 = delay_moments([x + c for x in d], p)
        assert mu2 == mu + c and var2 == var
        mu3, var3 = delay_moments([a * x for x in d], p)
        assert mu3 == a * mu and var3 == a * a * var
        # Range: the variance is at most a quarter of the squared span.
        assert 0 <= var <= (max(d) - min(d)) ** 2 / 4


def test_fleury_bound_and_taylor() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        n = rng.randint(2, 6)
        p = [rng.random() ** 3 + 1e-9 for _ in range(n)]
        d = [rng.random() * 10 for _ in range(n)]
        _, s = rms_delay_spread(d, p)
        for k in range(1, 26):
            df = 0.01 * k / s
            r = abs(frequency_correlation(d, p, df))
            assert r >= math.cos(2 * math.pi * s * df) - 1e-12
            assert r >= 1 - 2 * math.pi ** 2 * s * s * df * df - 1e-12
        # Taylor: 1 - Re(exp(j 2 pi df mu) R(df)) is close to 2 pi^2 sigma^2 df^2 for small df.
        mu, _ = rms_delay_spread(d, p)
        span = max(abs(t - mu) for t in d)
        if s < 0.1 * span:
            continue
        df = 2e-3 / span
        r = frequency_correlation(d, p, df) * complex(math.cos(2 * math.pi * df * mu), math.sin(2 * math.pi * df * mu))
        assert abs((1 - r.real) / (2 * math.pi ** 2 * s * s * df * df) - 1) < 1e-3


def test_bad_input() -> None:
    for d, p in (([], []), ([0, 1], [1]), ([0, 1], [0, 0]), ([0, 1], [1, -1])):
        try:
            delay_moments(d, p)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
