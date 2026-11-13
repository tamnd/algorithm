# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/state-discrimination-problem/. The authors are listed in prov/YN47TX.jsonl.

import math
import random

from state_discrimination_problem import (
    helstrom_measurement,
    helstrom_success,
    pure_helstrom_success,
    success_of,
    unambiguous_povm,
)
from qsim import eigvalsh, inner, outer, random_state, reduced_density, trace, matmul

TOL = 1e-9
ZERO, PLUS = [1, 0], [2 ** -0.5, 2 ** -0.5]


def rho_of(v):
    return outer(v, v)


def bloch_grid(steps):
    for i in range(steps + 1):
        t = math.pi * i / steps
        for j in range(2 * steps):
            f = math.pi * j / steps
            yield [math.cos(t / 2), complex(math.cos(f), math.sin(f)) * math.sin(t / 2)]


def best_projective_by_grid(p, rho, sigma, steps=60):
    """The best two-outcome projective measurement: P = 0, P = I, or P of rank one on a grid."""
    trivial = max(success_of(p, rho, sigma, [[0, 0], [0, 0]]), success_of(p, rho, sigma, [[1, 0], [0, 1]]))
    return max(trivial, max(success_of(p, rho, sigma, outer(v, v)) for v in bloch_grid(steps)))


def test_zero_and_plus_with_equal_priors() -> None:
    value = helstrom_success(0.5, rho_of(ZERO), rho_of(PLUS))
    assert abs(value - math.cos(math.pi / 8) ** 2) < TOL
    assert abs(value - (1 + 2 ** -0.5) / 2) < TOL
    P = helstrom_measurement(0.5, rho_of(ZERO), rho_of(PLUS))
    assert abs(success_of(0.5, rho_of(ZERO), rho_of(PLUS), P) - value) < TOL


def test_edge_cases() -> None:
    assert abs(helstrom_success(0.5, rho_of(ZERO), rho_of([0, 1])) - 1) < TOL
    for p in (0.1, 0.5, 0.8):
        assert abs(helstrom_success(p, rho_of(PLUS), rho_of(PLUS)) - max(p, 1 - p)) < TOL


def test_closed_form_for_pure_states_and_the_measurement_reaches_it() -> None:
    rng = random.Random(51)
    for _ in range(100):
        a, b, p = random_state(1, rng), random_state(1, rng), rng.random()
        value = helstrom_success(p, rho_of(a), rho_of(b))
        assert abs(value - pure_helstrom_success(p, abs(inner(a, b)))) < TOL
        P = helstrom_measurement(p, rho_of(a), rho_of(b))
        assert abs(success_of(p, rho_of(a), rho_of(b), P) - value) < TOL


def test_no_projective_measurement_beats_helstrom_on_mixed_states() -> None:
    rng = random.Random(52)
    for _ in range(10):
        rho = reduced_density(random_state(2, rng), 2, [1])
        sigma = reduced_density(random_state(2, rng), 2, [1])
        p = rng.random()
        best = helstrom_success(p, rho, sigma)
        grid = best_projective_by_grid(p, rho, sigma)
        assert grid <= best + 1e-12
        assert grid >= best - 2e-3
        assert grid >= max(p, 1 - p) - 1e-12


def test_unambiguous_measurement_never_errs() -> None:
    rng = random.Random(53)
    for a, b in [(ZERO, PLUS)] + [(random_state(1, rng), random_state(1, rng)) for _ in range(50)]:
        e_a, e_b, e_fail = unambiguous_povm(a, b)
        assert min(eigvalsh(e_fail)) > -1e-12
        assert abs(trace(matmul(e_a, rho_of(b)))) < 1e-12
        assert abs(trace(matmul(e_b, rho_of(a)))) < 1e-12
        success = 0.5 * trace(matmul(e_a, rho_of(a))).real + 0.5 * trace(matmul(e_b, rho_of(b))).real
        assert abs(success - (1 - abs(inner(a, b)))) < 1e-12
    e_a, e_b, _ = unambiguous_povm(ZERO, PLUS)
    s = 0.5 * trace(matmul(e_a, rho_of(ZERO))).real + 0.5 * trace(matmul(e_b, rho_of(PLUS))).real
    assert abs(s - (1 - 2 ** -0.5)) < 1e-12


def test_trine_states_square_root_measurement() -> None:
    trine = [[math.cos(2 * math.pi * k / 3), math.sin(2 * math.pi * k / 3)] for k in range(3)]
    povm = [[[2 / 3 * x for x in row] for row in outer(v, v)] for v in trine]
    total = [[sum(E[i][j] for E in povm) for j in range(2)] for i in range(2)]
    assert all(abs(total[i][j] - (1 if i == j else 0)) < 1e-12 for i in range(2) for j in range(2))
    success = sum(trace(matmul(E, outer(v, v))).real for E, v in zip(povm, trine)) / 3
    assert abs(success - 2 / 3) < 1e-12
