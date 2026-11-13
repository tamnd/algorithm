# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swap-test/. The authors are listed in prov/P7XCAZ.jsonl.

import math
import random

from qsim import SQRT_HALF, kron_vec, matmul, measure_qubit, random_density, random_state, trace
from swap_test import (
    destructive_probability_zero,
    estimate_overlap,
    exact_overlap,
    final_state,
    overlap_by_destructive_test,
    probability_zero,
    probability_zero_mixed,
    runs_needed,
    swap_test,
)


def test_probability_of_zero():
    rng = random.Random(71)
    for n in (1, 2, 3):
        for _ in range(5):
            psi, phi = random_state(rng, 2**n), random_state(rng, 2**n)
            assert abs(probability_zero(psi, phi) - (1 + exact_overlap(psi, phi)) / 2) < 1e-12


def test_example_states():
    zero, one = [1, 0], [0, 1]
    plus = [SQRT_HALF, SQRT_HALF]
    assert abs(probability_zero(zero, zero) - 1) < 1e-12
    assert abs(probability_zero(zero, one) - 0.5) < 1e-12
    assert abs(probability_zero(zero, plus) - 0.75) < 1e-12
    # a global phase does not change the result
    assert abs(probability_zero(plus, [1j * x for x in plus]) - 1) < 1e-12
    rng = random.Random(72)
    assert all(swap_test(plus, plus, rng) == 0 for _ in range(200))


def test_final_state_formula():
    # Before the measurement: (|0>(|phi psi> + |psi phi>) + |1>(|phi psi> - |psi phi>)) / 2,
    # where |phi psi> means phi in register B and psi in register A.
    rng = random.Random(73)
    n = 2
    psi, phi = random_state(rng, 4), random_state(rng, 4)
    same, swapped = kron_vec(phi, psi), kron_vec(psi, phi)
    expected = [(x + y) / 2 for x, y in zip(same, swapped)] + [(x - y) / 2 for x, y in zip(same, swapped)]
    got = final_state(psi, phi)
    assert max(abs(x - y) for x, y in zip(got, expected)) < 1e-12
    assert len(got) == 2 ** (2 * n + 1)


def test_outcome_zero_leaves_a_symmetric_state():
    rng = random.Random(74)
    n = 1
    psi, phi = random_state(rng, 2), random_state(rng, 2)
    state = final_state(psi, phi)
    for _ in range(20):
        outcome, post = measure_qubit(state, 2 * n, rng)
        regs = post[:4] if outcome == 0 else post[4:]
        swapped = [regs[(i >> 1) | ((i & 1) << 1)] for i in range(4)]  # exchange qubits 0 and 1
        sign = 1 if outcome == 0 else -1
        assert max(abs(x - sign * y) for x, y in zip(regs, swapped)) < 1e-12


def test_mixed_states():
    rng = random.Random(75)
    for d in (2, 4):
        for _ in range(3):
            rho, sigma = random_density(rng, d), random_density(rng, d)
            expected = (1 + trace(matmul(rho, sigma)).real) / 2
            assert abs(probability_zero_mixed(rho, sigma) - expected) < 1e-12
    half = [[0.5, 0], [0, 0.5]]
    assert abs(probability_zero_mixed(half, half) - 0.75) < 1e-12  # purity 1/2
    psi = random_state(rng, 2)
    pure = [[a * b.conjugate() for b in psi] for a in psi]
    assert abs(probability_zero_mixed(pure, pure) - 1) < 1e-12


def test_runs_needed():
    assert runs_needed(0.05, 0.01) == 4239
    assert runs_needed(0.1, 0.01) == 1060
    assert runs_needed(0.1, 0.01) == math.ceil(2 * math.log(200) / 0.01)


def test_estimate_within_error():
    rng = random.Random(76)
    eps, delta = 0.1, 0.01
    for _ in range(4):
        psi, phi = random_state(rng, 2), random_state(rng, 2)
        est, runs = estimate_overlap(psi, phi, eps, delta, rng)
        assert runs == 1060
        assert abs(est - exact_overlap(psi, phi)) <= eps
    est, _ = estimate_overlap([1, 0], [0, 1], eps, delta, rng)
    assert est <= eps  # orthogonal states, the estimate is clipped at 0


def test_destructive_variant():
    rng = random.Random(77)
    for n in (1, 2):
        for _ in range(4):
            psi, phi = random_state(rng, 2**n), random_state(rng, 2**n)
            assert abs(destructive_probability_zero(psi, phi) - probability_zero(psi, phi)) < 1e-12
    psi, phi = random_state(rng, 4), random_state(rng, 4)
    runs = 2000
    t = 2 * math.sqrt(math.log(2 / 1e-4) / (2 * runs))  # Hoeffding for the frequency, doubled for 2f - 1
    assert abs(overlap_by_destructive_test(psi, phi, runs, rng) - exact_overlap(psi, phi)) <= t
