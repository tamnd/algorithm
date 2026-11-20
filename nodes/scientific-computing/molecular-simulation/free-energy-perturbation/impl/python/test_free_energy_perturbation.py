# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-energy-perturbation/. The authors are listed in prov/1TXW31.jsonl.
import math
import random

import pytest

from free_energy_perturbation import fep, fep_error, fep_from_samples, staged_fep


def test_hand_example():
    # du = 0, 1, 2 in units of kT: dA = -ln((1 + e^-1 + e^-2) / 3).
    assert fep([0.0, 1.0, 2.0], 1.0) == pytest.approx(0.691006, abs=1e-6)


def test_constant_difference_is_exact():
    assert fep([2.5] * 7, 0.4) == pytest.approx(2.5, abs=1e-12)
    assert fep([-1.25], 3.0) == pytest.approx(-1.25, abs=1e-12)


def test_no_overflow_for_large_differences():
    du = [1000.0, 1001.0, 1002.0]
    assert fep(du, 1.0) == pytest.approx(1000.0 + 0.691006, abs=1e-6)
    du = [-1000.0, -999.0]
    assert math.isfinite(fep(du, 1.0))


def test_jensen_bound_estimate_never_exceeds_mean():
    rng = random.Random(11)
    for _ in range(50):
        du = [rng.uniform(-3, 3) for _ in range(rng.randint(1, 20))]
        assert fep(du, 1.0) <= sum(du) / len(du) + 1e-12
        assert fep(du, 1.0) >= min(du) - 1e-12


def test_harmonic_wells_against_exact_value():
    # U_0 = x^2 / 2, U_1 = x^2 (k_0 = 1, k_1 = 2), kT = 1: dA = ln(2) / 2.
    exact = 0.5 * math.log(2.0)
    rng = random.Random(1)
    xs = [rng.gauss(0.0, 1.0) for _ in range(20000)]
    est = fep_from_samples(xs, lambda x: 0.5 * x * x, lambda x: x * x, 1.0)
    se = fep_error([0.5 * x * x for x in xs], 1.0)
    assert abs(est - exact) < 4 * se
    # The exact large-N error: var(w) / (N E[w]^2) with E[w] = 1/sqrt(2), E[w^2] = 1/sqrt(3).
    assert se == pytest.approx(math.sqrt((1 / math.sqrt(3) - 0.5) / 0.5 / 20000), rel=0.05)


def test_temperature_scaling():
    # dA = (kT / 2) ln(k_1 / k_0) for each kT.
    for kT in (0.5, 2.0):
        beta = 1.0 / kT
        rng = random.Random(2)
        xs = [rng.gauss(0.0, math.sqrt(kT)) for _ in range(20000)]
        du = [0.5 * x * x for x in xs]
        assert abs(fep(du, beta) - 0.5 * kT * math.log(2.0)) < 4 * fep_error(du, beta)


def test_small_samples_are_biased_upward():
    # E[fep] >= dA by Jensen's inequality; the first-order bias is var(w) / (2 N beta E[w]^2).
    exact = 0.5 * math.log(2.0)
    rng = random.Random(3)
    n, reps = 5, 4000
    vals = [fep([0.5 * rng.gauss(0, 1) ** 2 for _ in range(n)], 1.0) for _ in range(reps)]
    mean = sum(vals) / reps
    sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (reps - 1))
    first_order = (1 / math.sqrt(3) - 0.5) / 0.5 / (2 * n)
    se = sd / math.sqrt(reps)
    assert mean - exact > 4 * se
    assert abs(mean - exact - first_order) < 4 * se + 0.5 * first_order


def shifted(a):
    def sample(lam, n, rng):
        return [a * lam + rng.gauss(0.0, 1.0) for _ in range(n)]

    def energy(lam, x):
        return 0.5 * (x - a * lam) ** 2

    return sample, energy


def test_staged_fep_on_shifted_well():
    # Moving a unit well by a = 3 does not change A, so dA = 0.
    sample, energy = shifted(3.0)
    lams = [k / 6 for k in range(7)]
    est, se = staged_fep(lams, sample, energy, 1.0, 200, random.Random(1))
    assert abs(est) < 4 * se
    assert se < 0.12


def test_one_window_with_poor_overlap_fails_its_own_error_bar():
    # One window with the same 1200 samples: the error bar of the estimator is too small.
    sample, energy = shifted(3.0)
    est, se = staged_fep([0.0, 1.0], sample, energy, 1.0, 1200, random.Random(1))
    assert abs(est) > 4 * se


def test_staged_harmonic_matches_exact():
    def sample(lam, n, rng):
        return [rng.gauss(0.0, 1.0 / math.sqrt(1 + 15 * lam)) for _ in range(n)]

    def energy(lam, x):
        return 0.5 * (1 + 15 * lam) * x * x

    est, se = staged_fep([0, 1 / 15, 3 / 15, 7 / 15, 1], sample, energy, 1.0, 2000, random.Random(5))
    assert abs(est - 0.5 * math.log(16.0)) < 4 * se


def test_empty_input_raises():
    with pytest.raises(ValueError):
        fep([], 1.0)
