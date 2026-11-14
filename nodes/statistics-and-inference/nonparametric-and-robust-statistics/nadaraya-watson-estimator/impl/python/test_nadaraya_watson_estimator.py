# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nadaraya-watson-estimator/. The authors are listed in prov/HA8PMS.jsonl.

import math
import random
from fractions import Fraction

from nadaraya_watson_estimator import (
    choose_bandwidth, epanechnikov, gaussian, loo_cv, loo_cv_brute,
    nadaraya_watson, weights,
)


def test_page_example() -> None:
    xs = list(range(7))
    ys = [2 * x for x in xs]
    got = [nadaraya_watson(Fraction(x), xs, ys, Fraction(2)) for x in range(7)]
    assert got == [Fraction(6, 7), 2, 4, 6, 8, 10, Fraction(78, 7)]
    got = [nadaraya_watson(Fraction(x), xs, ys, Fraction(3)) for x in range(7)]
    assert got == [Fraction(18, 11), Fraction(8, 3), 4, 6, 8, Fraction(28, 3), Fraction(114, 11)]
    assert nadaraya_watson(Fraction(-3), xs, ys, Fraction(2)) is None


def test_reproduces_a_constant_exactly() -> None:
    rng = random.Random(71)
    for _ in range(200):
        n = rng.randint(1, 12)
        xs = [Fraction(rng.randint(-30, 30), rng.randint(1, 5)) for _ in range(n)]
        c = Fraction(rng.randint(-50, 50), rng.randint(1, 7))
        h = Fraction(rng.randint(1, 20), rng.randint(1, 5))
        x = Fraction(rng.randint(-40, 40), rng.randint(1, 5))
        m = nadaraya_watson(x, xs, [c] * n, h)
        assert m is None or m == c


def test_weights_and_range() -> None:
    rng = random.Random(72)
    for _ in range(200):
        n = rng.randint(1, 15)
        xs = [Fraction(rng.randint(-30, 30), rng.randint(1, 5)) for _ in range(n)]
        ys = [Fraction(rng.randint(-30, 30)) for _ in range(n)]
        h = Fraction(rng.randint(1, 20), rng.randint(1, 5))
        x = Fraction(rng.randint(-40, 40), rng.randint(1, 5))
        w = weights(x, xs, h)
        m = nadaraya_watson(x, xs, ys, h)
        if w is None:
            assert m is None
            continue
        assert sum(w) == 1 and min(w) >= 0
        assert m == sum(wi * yi for wi, yi in zip(w, ys))
        assert min(ys) <= m <= max(ys)


def test_boundary_bias_is_of_order_h() -> None:
    # Equally spaced design i/N on [0, 1], m(x) = a + b x, no noise: the
    # estimate at 0 is a + b sum w_i x_i, and bias/(b h) tends to
    # int_0^1 u K / int_0^1 K, which is 3/8 for the Epanechnikov kernel.
    a, b = Fraction(2), Fraction(-3)
    for N, h in ((1000, Fraction(1, 10)), (4000, Fraction(1, 20))):
        xs = [Fraction(i, N) for i in range(N + 1)]
        ys = [a + b * x for x in xs]
        bias = nadaraya_watson(Fraction(0), xs, ys, h) - a
        assert abs(bias / (b * h) - Fraction(3, 8)) < 3 / (N * h)
        # In the interior the design is symmetric around x, and the bias is 0.
        assert nadaraya_watson(Fraction(1, 2), xs, ys, h) == a + b / 2
    # Gaussian kernel: the limit is phi(0) / (1/2) = sqrt(2/pi).
    N, h = 4000, 0.02
    xs = [i / N for i in range(N + 1)]
    bias = nadaraya_watson(0.0, xs, [1 + 5 * x for x in xs], h, gaussian) - 1
    assert abs(bias / (5 * h) - math.sqrt(2 / math.pi)) < 3 / (N * h)


def test_interior_bias_is_of_order_h_squared() -> None:
    # For m(x) = x^2 on a uniform design, bias/h^2 tends to mu2 m''/2 = 1/5.
    for N, h in ((2000, Fraction(1, 10)), (4000, Fraction(1, 20))):
        xs = [Fraction(i, N) for i in range(N + 1)]
        bias = nadaraya_watson(Fraction(1, 2), xs, [x * x for x in xs], h) - Fraction(1, 4)
        assert abs(bias / (h * h) - Fraction(1, 5)) < 5 / (N * h) ** 2 + Fraction(1, 10**9)


def test_leave_one_out_shortcut() -> None:
    rng = random.Random(73)
    for _ in range(30):
        n = rng.randint(2, 10)
        xs = [Fraction(rng.randint(0, 20)) for _ in range(n)]
        ys = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
        h = Fraction(rng.randint(1, 12), 2)
        assert loo_cv(h, xs, ys) == loo_cv_brute(h, xs, ys)


def test_choose_bandwidth_on_a_curve() -> None:
    rng = random.Random(74)
    n = 120
    xs = sorted(rng.random() for _ in range(n))
    ys = [math.sin(2 * math.pi * x) + rng.gauss(0, 0.3) for x in xs]
    cands = [0.02 * k for k in range(2, 26)]
    h = choose_bandwidth(xs, ys, cands)
    assert all(loo_cv_brute(h, xs, ys) <= loo_cv_brute(g, xs, ys) + 1e-12 for g in cands)
    # Measured, not guaranteed: the chosen fit is closer to the truth than
    # the narrowest and the widest candidates.
    err = lambda g: sum((nadaraya_watson(t / 50, xs, ys, g) - math.sin(2 * math.pi * t / 50)) ** 2
                        for t in range(5, 46))
    assert err(h) < err(cands[0]) and err(h) < err(cands[-1])
