# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/level-crossing-rate/. The authors are listed in prov/Y8DDW4.jsonl.

import cmath
import math
import random

from level_crossing_rate import count_crossings, lcr_afd_clarke, lcr_afd_rayleigh


def test_check_values() -> None:
    n, t = lcr_afd_clarke(1.0, 1.0)
    assert abs(n - 0.92214) < 5e-6 and abs(t - 0.68550) < 5e-6
    assert abs(n * t - (1 - math.exp(-1))) < 1e-15
    table = [
        (1 / math.sqrt(2), 1.07505, 0.36600),
        (10 ** (-10 / 20), 0.71723, 0.13268),
        (0.1, 0.24817, 0.04009),
        (10 ** (-30 / 20), 0.07919, 0.01262),
    ]
    for rho, nr, tr in table:
        n, t = lcr_afd_clarke(rho, 1.0)
        assert abs(n - nr) < 5e-6 and abs(t - tr) < 5e-6


def test_example_numbers() -> None:
    fd = 30 * 900e6 / 299_792_458.0
    n, t = lcr_afd_clarke(1.0, fd)
    assert abs(n - 83.05) < 0.01 and abs(t * 1e3 - 7.611) < 1e-3
    n, t = lcr_afd_clarke(0.1, fd)
    assert abs(n - 22.35) < 0.01 and abs(t * 1e3 - 0.4452) < 1e-4
    fd = (3 / 3.6) * 2.4e9 / 299_792_458.0
    n, t = lcr_afd_clarke(10 ** (-0.5), fd)
    assert abs(n - 4.785) < 1e-3 and abs(t * 1e3 - 19.89) < 0.01


def test_scaling_and_maximum() -> None:
    for rho in (0.05, 0.3, 1.0, 1.7):
        n1, t1 = lcr_afd_clarke(rho, 10.0)
        n2, t2 = lcr_afd_clarke(rho, 20.0)
        assert abs(n2 - 2 * n1) < 1e-12 and abs(t2 - t1 / 2) < 1e-15
        # Clarke is the general formula with sigma_nu = f_D / sqrt(2).
        ng, tg = lcr_afd_rayleigh(rho, 10.0 / math.sqrt(2))
        assert abs(ng - n1) < 1e-12 and abs(tg - t1) < 1e-15
    grid = [i / 10000 for i in range(1, 30000)]
    best = max(grid, key=lambda r: lcr_afd_clarke(r, 1.0)[0])
    assert abs(best - 1 / math.sqrt(2)) < 2e-4
    assert abs(lcr_afd_clarke(1 / math.sqrt(2), 1.0)[0] - math.sqrt(math.pi) * math.exp(-0.5)) < 1e-15


def envelope_path(rng: random.Random, m: int, fd: float, dt: float, n: int) -> list:
    """|h(k dt)| for h = sum of m sinusoids with random angles and phases, power 1."""
    amp = 1 / math.sqrt(m)
    z = [amp * cmath.exp(1j * rng.uniform(0, 2 * math.pi)) for _ in range(m)]
    w = [cmath.exp(2j * math.pi * fd * math.cos(rng.uniform(0, 2 * math.pi)) * dt) for _ in range(m)]
    out = []
    for _ in range(n):
        out.append(abs(sum(z)))
        z = [a * b for a, b in zip(z, w)]
    return out


def test_counts_on_sample_paths() -> None:
    # Tolerance 10%: a sum of 32 sinusoids is close to, not exactly, a Gaussian process.
    rng = random.Random(11)
    fd, dt, n, reps = 1.0, 0.01, 8000, 16
    paths = [envelope_path(rng, 32, fd, dt, n) for _ in range(reps)]
    for rho in (1.0, 10 ** (-10 / 20)):
        crossings = below = 0
        for r in paths:
            nr, tr = count_crossings(r, rho, dt)
            crossings += round(nr * n * dt)
            below += sum(1 for x in r if x < rho)
        est_n = crossings / (reps * n * dt)
        est_t = below * dt / crossings
        exact_n, exact_t = lcr_afd_clarke(rho, fd)
        assert abs(est_n / exact_n - 1) < 0.10
        assert abs(est_t / exact_t - 1) < 0.10


def test_count_small_cases() -> None:
    r = [2.0, 0.5, 2.0, 0.5, 0.5, 2.0]
    n, t = count_crossings(r, 1.0, 0.5)
    assert n == 2 / 3 and t == 0.75
    assert count_crossings([2.0, 2.0], 1.0, 1.0) == (0.0, math.inf)
    for bad in ((0.0, 1.0), (1.0, 0.0)):
        try:
            lcr_afd_clarke(*bad)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
