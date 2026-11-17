# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wright-fisher-diffusion/. The authors are listed in prov/ET1T47.jsonl.

import math

from wright_fisher_diffusion import (
    absorption_time,
    exact_chain,
    fixation_probability,
    generator_coefficients,
    kimura_genic,
    moments,
    neutral_absorption_time,
    scale_density,
)


def test_moments_and_generator():
    m, v = moments(0.3, 50, 0.02, 0.5)
    assert abs(m - 0.01 * 0.3 * 0.7) < 1e-15
    assert abs(v - 0.21 / 100) < 1e-15
    a, b = generator_coefficients(0.3, 50, 0.02, 0.5)
    assert abs(a - 100 * m) < 1e-12 and abs(b - 0.105) < 1e-12
    assert scale_density(0.0, 50, 0.1, 0.3) == 1.0


def test_numeric_integral_matches_kimura_formula():
    for N, s_k in ((10, 0.05), (100, 0.01), (100, -0.01), (20, 0.2), (500, 0.001)):
        for p in (1 / (2 * N), 0.1, 0.5, 0.9):
            assert abs(fixation_probability(p, N, 2 * s_k, 0.5) - kimura_genic(p, N, s_k)) < 1e-9


def test_check_value_and_limits():
    assert abs(kimura_genic(1 / 200, 100, 0.01) - 0.020171) < 5e-7
    assert kimura_genic(0.3, 100, 0.0) == 0.3
    assert fixation_probability(0.3, 100, 0.0) == 0.3
    # Small s gives p; large positive N s gives about 2 s for one copy.
    assert abs(kimura_genic(0.01, 50, 1e-9) - 0.01) < 1e-8
    assert abs(kimura_genic(1 / 20000, 10000, 0.01) / (1 - math.exp(-0.02)) - 1) < 1e-12


def test_neutral_time_green_function():
    for N, p in ((10, 0.5), (50, 0.01), (50, 0.3)):
        assert abs(absorption_time(p, N) / neutral_absorption_time(p, N) - 1) < 1e-4


def test_diffusion_close_to_chain_when_s_small():
    # N = 50 and s_K = 0.01 (N s_K = 0.5): the relative error is under 1 percent.
    u, _ = exact_chain(100, 0.02, 0.5)
    assert abs(u[1] - 0.022793) < 5e-7
    assert abs(kimura_genic(0.01, 50, 0.01) / u[1] - 1) < 0.01
    # Recessive (h = 0) and dominant (h = 1) alleles, s = 0.1, N = 50.
    for h, tol in ((0.0, 0.02), (1.0, 0.05)):
        u, _ = exact_chain(100, 0.1, h)
        assert abs(fixation_probability(0.01, 50, 0.1, h) / u[1] - 1) < tol
    # Neutral fixation is exact in both: u(p) = p.
    u, _ = exact_chain(20)
    assert all(abs(u[i] - i / 20) < 1e-12 for i in range(21))


def test_diffusion_fails_when_s_large():
    # N = 10 and s_K = 0.5: the diffusion is about 12 percent too high.
    u, _ = exact_chain(20, 1.0, 0.5)
    assert abs(u[1] - 0.56423) < 5e-6
    err = kimura_genic(0.05, 10, 0.5) / u[1] - 1
    assert 0.10 < err < 0.14


def test_absorption_time_against_chain():
    u, t = exact_chain(20)
    assert abs(t[10] - 26.229) < 5e-4
    # The diffusion is about 6 percent too high at 2N = 20 and 1.5 percent at 2N = 100.
    assert 0.04 < neutral_absorption_time(0.5, 10) / t[10] - 1 < 0.08
    u, t = exact_chain(100)
    assert 0.005 < neutral_absorption_time(0.5, 50) / t[50] - 1 < 0.025
    u, t = exact_chain(100, 0.04, 0.5)
    assert abs(absorption_time(0.01, 50, 0.04, 0.5) / t[1] - 1) < 0.06


def test_invalid():
    try:
        fixation_probability(1.5, 10, 0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    assert absorption_time(0.0, 10) == 0.0
