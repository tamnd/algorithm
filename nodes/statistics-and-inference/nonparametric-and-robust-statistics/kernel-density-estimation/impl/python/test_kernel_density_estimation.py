# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-density-estimation/. The authors are listed in prov/29Z7ZM.jsonl.

import math
import random
from fractions import Fraction

from kernel_density_estimation import (
    KERNEL_CONSTANTS, amise, amise_bandwidth, binned_direct, epanechnikov,
    exact_mise_gaussian, gaussian, kde, kde_binned_fft, kde_grid_direct,
    normal_density,
)

PAGE_DATA = [1, 2, 4, 7, 8]


def simpson(f, a, b, m):
    """Composite Simpson rule with m (even) panels; exact for quadratics."""
    step = (b - a) / m
    s = f(a) + f(b)
    for k in range(1, m):
        s += (4 if k % 2 else 2) * f(a + k * step)
    return s * step / 3


def test_page_example() -> None:
    f = lambda x: kde(Fraction(x), PAGE_DATA, Fraction(2), epanechnikov)
    assert f(2) == Fraction(21, 160)
    assert f(3) == Fraction(9, 80)
    assert f(4) == Fraction(3, 40)
    assert f(Fraction(11, 2)) == Fraction(21, 320)
    assert f(Fraction(15, 2)) == Fraction(9, 64)
    assert f(-1) == 0 and f(10) == 0


def test_epanechnikov_integrates_to_one_exactly() -> None:
    rng = random.Random(51)
    for _ in range(20):
        data = [Fraction(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(rng.randint(1, 8))]
        h = Fraction(rng.randint(1, 12), rng.randint(1, 4))
        # The estimate is a quadratic between consecutive breakpoints X_i +- h,
        # so Simpson's rule on each piece is exact.
        cuts = sorted({xi + s * h for xi in data for s in (-1, 1)})
        total = sum(simpson(lambda x: kde(x, data, h, epanechnikov), a, b, 2)
                    for a, b in zip(cuts, cuts[1:]))
        assert total == 1


def test_gaussian_integrates_to_one() -> None:
    rng = random.Random(52)
    data = [rng.gauss(0, 1) for _ in range(50)]
    h = 0.4
    a, b = min(data) - 10 * h, max(data) + 10 * h
    assert abs(simpson(lambda x: kde(x, data, h), a, b, 4000) - 1) < 1e-9


def test_fft_convolution_matches_direct_binned_sum() -> None:
    rng = random.Random(53)
    data = [rng.gauss(0, 1) for _ in range(300)]
    for kernel in (gaussian, epanechnikov):
        fast = kde_binned_fft(data, 0.35, -5.0, 5.0, 129, kernel)
        slow = binned_direct(data, 0.35, -5.0, 5.0, 129, kernel)
        assert max(abs(u - v) for u, v in zip(fast, slow)) < 1e-12


def test_binned_fft_against_direct_within_bound() -> None:
    # Linear binning replaces K_h(g - x) by its linear interpolation between
    # grid points, so the error is at most delta^2 sup|K''| / (8 h^3).
    rng = random.Random(54)
    data = [rng.gauss(0, 1) for _ in range(1000)]
    h, lo, hi = 0.3, -7.0, 7.0
    for m in (65, 129, 257):
        delta = (hi - lo) / (m - 1)
        grid = [lo + k * delta for k in range(m)]
        err = max(abs(u - v) for u, v in zip(kde_binned_fft(data, h, lo, hi, m),
                                              kde_grid_direct(grid, data, h)))
        bound = delta ** 2 / (8 * h ** 3 * math.sqrt(2 * math.pi))
        assert err <= bound + 1e-12


def test_bias_and_variance_expansions() -> None:
    # For N(0,1) data and the Gaussian kernel, E f(x) = phi_{sqrt(1+h^2)}(x)
    # and E K_h(x - X)^2 = phi_{sqrt(1 + h^2/2)}(x) / (2 h sqrt(pi)).
    f = lambda x: normal_density(x, 1.0)
    f2 = lambda x: (x * x - 1) * f(x)  # f''
    rk = KERNEL_CONSTANTS["gaussian"][0]
    for x in (0.0, 0.7, 1.5):
        for h in (1e-1, 1e-2):
            mean = normal_density(x, math.sqrt(1 + h * h))
            bias = mean - f(x)
            assert abs(bias / (h * h / 2 * f2(x)) - 1) < 3 * h * h + 1e-6
            ek2 = normal_density(x, math.sqrt(1 + h * h / 2)) / (2 * h * math.sqrt(math.pi))
            nh_var = h * (ek2 - mean * mean)  # n h Var for any n
            assert abs(nh_var - rk * f(x)) < 2 * h
    # And a Monte Carlo check of the mean of the code's estimate.
    rng = random.Random(55)
    h, n, reps = 0.5, 100, 400
    vals = [kde(0.0, [rng.gauss(0, 1) for _ in range(n)], h) for _ in range(reps)]
    m = sum(vals) / reps
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (reps - 1))
    assert abs(m - normal_density(0.0, math.sqrt(1 + h * h))) < 3 * sd / math.sqrt(reps)


def golden(f, a, b, it=200):
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    for _ in range(it):
        if f(c) < f(d):
            b = d
        else:
            a = c
        c, d = b - g * (b - a), a + g * (b - a)
    return (a + b) / 2


def test_amise_bandwidth() -> None:
    rf2 = 3 / (8 * math.sqrt(math.pi))  # R(f'') for N(0, 1)
    for n in (10, 1000, 10**6):
        h = amise_bandwidth(n, rf2)
        assert abs(h - (4 / (3 * n)) ** 0.2) < 1e-12
        # h minimises the AMISE: its derivative h^3 mu2^2 R - R(K)/(n h^2) is 0.
        assert abs(golden(lambda t: amise(t, n, rf2), 1e-4, 3) / h - 1) < 1e-6
    # The exact MISE minimiser approaches the AMISE one as n grows.
    ratios = [golden(lambda t: exact_mise_gaussian(t, n, 1.0), 1e-4, 3) / amise_bandwidth(n, rf2)
              for n in (100, 10**4, 10**6)]
    assert ratios[0] > ratios[1] > ratios[2] > 1
    assert ratios[2] < 1.005
