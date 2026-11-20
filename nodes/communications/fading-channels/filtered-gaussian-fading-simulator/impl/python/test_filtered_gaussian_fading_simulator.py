# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filtered-gaussian-fading-simulator/. The authors are listed in prov/K4JBF8.jsonl.

import math
import random

from filtered_gaussian_fading_simulator import (
    doppler_filter,
    exact_autocorrelation,
    filtered_gaussian,
    j0,
)


def test_filter_shape() -> None:
    n, fm = 128, 1 / 16
    f = doppler_filter(n, fm)
    km = 8
    assert f[0] == 0.0
    assert all(f[k] == 0.0 for k in range(km + 1, n - km))
    assert all(f[k] == f[n - k] for k in range(1, km + 1))
    # F[k]^2 = 1 / (2 sqrt(1 - (k / 8)^2)) below the edge
    assert abs(f[1] ** 2 - 1 / (2 * math.sqrt(1 - 1 / 64))) < 1e-12
    # the edge bin holds the area of the spectrum over [k_m - 1, k_m]
    area = (km / 2) * (math.pi / 2 - math.asin((km - 1) / km))
    assert abs(f[km] ** 2 - area) < 1e-12


def test_covariance_from_unit_inputs() -> None:
    # The map from the inputs g to h is linear, so the covariance of h is the
    # sum over k of the outer products of the outputs for g = e_k.
    n, fm = 64, 1 / 8
    rng = random.Random(0)
    cols = []
    for k in range(n):
        e = [0j] * n
        e[k] = 1 + 0j
        cols.append(filtered_gaussian(n, fm, rng, g=e))
    for d in (0, 1, 2, 3, 5, 8):
        r = exact_autocorrelation(n, fm, d)
        for i in (0, 7, 33, 63):
            c = sum(col[(i + d) % n] * col[i].conjugate() for col in cols)
            assert abs(c - r) < 1e-9
    assert abs(exact_autocorrelation(n, fm, 0) - 1.0) < 1e-12


def test_sample_power_and_autocorrelation() -> None:
    n, fm = 128, 1 / 8
    rng = random.Random(8001)
    runs = 60
    lags = (0, 1, 2, 3, 4, 8)
    acc = [0j] * len(lags)
    for _ in range(runs):
        h = filtered_gaussian(n, fm, rng, omega=2.0)
        for j, d in enumerate(lags):
            acc[j] += sum(h[(i + d) % n] * h[i].conjugate() for i in range(n)) / n
    for j, d in enumerate(lags):
        assert abs(acc[j] / runs - exact_autocorrelation(n, fm, d, omega=2.0)) < 0.2


def test_close_to_clarke_and_better_with_more_bins() -> None:
    # N = 256 and f_m = 1/8 give k_m = 32: within 0.05 of J0 for f_D tau <= 1
    for d in range(0, 9):
        x = 2 * math.pi * d / 8
        assert abs(exact_autocorrelation(256, 1 / 8, d) - j0(x)) < 0.05
    # the error at f_D tau = 0.375, near the first zero of J0, shrinks as k_m grows
    errs = []
    for n in (128, 256, 512, 1024):  # k_m = 8, 16, 32, 64, and lag 6 is f_D tau = 0.375
        errs.append(abs(exact_autocorrelation(n, 1 / 16, 6) - j0(2 * math.pi * 6 / 16)))
    assert all(errs[i + 1] < errs[i] for i in range(3))
    assert abs(errs[0] - 0.10537) < 1e-4 and errs[-1] < 0.03


def test_bad_parameters() -> None:
    for n, fm in ((64, 1 / 64), (64, 0.5)):
        try:
            doppler_filter(n, fm)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
