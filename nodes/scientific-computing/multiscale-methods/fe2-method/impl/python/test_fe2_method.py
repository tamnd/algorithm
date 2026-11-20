# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fe2-method/. The authors are listed in prov/6626AA.jsonl.
import random

from fe2_method import fe2_bar, fine_bar, micro_law, solve_rve

TWO_PHASE = [1.0] * 5 + [4.0] * 5


def test_rve_is_in_equilibrium_with_the_given_mean_strain():
    rng = random.Random(2)
    c = [rng.uniform(0.5, 5.0) for _ in range(12)]
    for E in (-0.4, 0.05, 0.7):
        sigma, _, w, it = solve_rve(c, 1.0, E)
        n = len(c)
        strain = [E + (w[j + 1] - w[j]) * n for j in range(n)]
        stress = [micro_law(c[j], 1.0, strain[j])[0] for j in range(n)]
        assert max(stress) - min(stress) < 1e-12
        assert abs(sum(strain) / n - E) < 1e-14
        assert abs(sigma - stress[0]) < 1e-12
        assert it <= 8


def test_consistent_tangent_matches_finite_differences_and_the_harmonic_mean():
    for E in (0.0, 0.3, -0.8):
        sigma, C, w, _ = solve_rve(TWO_PHASE, 1.0, E)
        h = 1e-6
        fd = (solve_rve(TWO_PHASE, 1.0, E + h)[0] - solve_rve(TWO_PHASE, 1.0, E - h)[0]) / (2 * h)
        assert abs(C - fd) < 1e-7 * C
        strain = [E + (w[j + 1] - w[j]) * 10 for j in range(10)]
        k = [micro_law(TWO_PHASE[j], 1.0, strain[j])[1] for j in range(10)]
        assert abs(C - 10 / sum(1 / v for v in k)) < 1e-12
    sigma, C, _, _ = solve_rve(TWO_PHASE, 1.0, 0.3)
    assert abs(sigma - 0.558889792228) < 1e-11


def test_linear_material_gives_the_harmonic_mean_and_the_exact_bar():
    sigma, C, _, _ = solve_rve(TWO_PHASE, 0.0, 0.3)
    assert abs(C - 1.6) < 1e-14 and abs(sigma - 0.48) < 1e-14
    U, _, it = fe2_bar(TWO_PHASE, 0.0, 8, 0.0, 1.0)
    assert it == 1
    for i in range(9):
        x = i / 8
        assert abs(U[i] - x * (1 - x) / 3.2) < 1e-14


def test_without_body_force_fe2_equals_the_resolved_bar():
    for M in (2, 5, 10):
        U, _, _ = fe2_bar(TWO_PHASE, 1.0, M, 0.1, 0.0)
        u = fine_bar(TWO_PHASE, 1.0, M, 0.1, 0.0)
        assert max(abs(U[i] - u[10 * i]) for i in range(M + 1)) < 1e-13


def test_with_body_force_the_difference_decreases_with_the_period():
    diffs = []
    for M in (5, 10, 20):
        U, _, it = fe2_bar(TWO_PHASE, 1.0, M, 0.1, 1.0)
        u = fine_bar(TWO_PHASE, 1.0, M, 0.1, 1.0)
        assert it <= 6
        diffs.append(max(abs(U[i] - u[10 * i]) for i in range(M + 1)))
    assert diffs[0] < 1e-3
    for d1, d2 in zip(diffs, diffs[1:]):
        assert 1.8 < d1 / d2 < 2.4
