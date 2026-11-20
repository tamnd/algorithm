# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heterogeneous-multiscale-method/. The authors are listed in prov/HVHGX1.jsonl.
import math

from heterogeneous_multiscale_method import hmm_1d, micro_coefficient

S3 = math.sqrt(3)


def sine(eps):
    return lambda x: 2 + math.sin(2 * math.pi * x / eps)


def test_one_period_gives_the_homogenized_coefficient():
    for eps in (1 / 64, 1e-3, 1e-5):
        a = sine(eps)
        assert abs(micro_coefficient(a, 0.3, eps, 16) - S3) < 1e-8
        assert abs(micro_coefficient(a, 0.3, eps, 32) - S3) < 1e-11


def test_whole_periods_are_exact_and_the_estimate_is_the_harmonic_mean():
    eps = 1 / 64
    a = sine(eps)
    for p in (1, 2, 3, 4):
        assert abs(micro_coefficient(a, 0.41, p * eps, 32 * p) - S3) < 1e-12
    delta, cells = 0.37 * eps, 10
    eta = delta / cells
    left = 0.2 - delta / 2
    harmonic = cells / sum(1 / a(left + (j + 0.5) * eta) for j in range(cells))
    assert abs(micro_coefficient(a, 0.2, delta, cells) - harmonic) < 1e-13


def test_error_of_a_partial_period_decays_like_eps_over_delta():
    eps = 1 / 64
    a = sine(eps)
    x_k = 0.5 + eps / 4
    worst = max(abs(1 / a(k * eps / 1000) - 1 / S3) for k in range(1000))
    scaled = []
    for p in (1, 2, 4, 8, 16):
        delta = (p + 0.5) * eps
        ak = micro_coefficient(a, x_k, delta, int(32 * (p + 0.5)))
        err = abs(1 / ak - 1 / S3)
        assert 0 < err <= (eps / delta) * worst
        scaled.append(err * delta / eps)
    assert max(scaled) - min(scaled) < 1e-10
    assert abs(scaled[0] - 0.0963528) < 1e-6


def test_macro_solution_matches_the_homogenized_solution():
    U, a_K = hmm_1d(sine(1e-3), lambda x: 1.0, 8, 1e-3, 16)
    for i in range(9):
        x = i / 8
        assert abs(U[i] - x * (1 - x) / (2 * S3)) < 1e-9
    assert all(abs(v - S3) < 1e-8 for v in a_K)


def test_an_unresolved_micro_cell_gives_the_wrong_answer():
    U, a_K = hmm_1d(sine(1e-3), lambda x: 1.0, 8, 1e-3, 1)
    assert abs(U[4] - 1 / 16) < 1e-12
    assert abs(U[4] - 1 / (8 * S3)) > 0.009


def test_cost_does_not_depend_on_eps():
    counts = []
    for eps in (1e-2, 1e-4, 1e-6):
        calls = [0]
        base = sine(eps)

        def a(x, base=base, calls=calls):
            calls[0] += 1
            return base(x)

        hmm_1d(a, lambda x: 1.0, 10, eps, 16)
        counts.append(calls[0])
    assert counts == [160, 160, 160]
