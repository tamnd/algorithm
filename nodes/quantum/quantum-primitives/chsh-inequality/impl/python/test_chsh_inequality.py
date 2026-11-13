# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chsh-inequality/. The authors are listed in prov/9NC848.jsonl.

import math
import random

from chsh_inequality import (
    OPTIMAL_ANGLES,
    chsh_value,
    classical_chsh_max,
    classical_game_value,
    correlation,
    deterministic_strategies,
    observable,
    play_chsh_game,
)
from qsim import eigvalsh, identity, kron_mat, kron_vec, mat_add, matmul, max_abs_diff, random_state

PHI_PLUS = [2 ** -0.5, 0, 0, 2 ** -0.5]
TOL = 1e-12


def test_optimal_angles_reach_two_sqrt_two() -> None:
    assert abs(chsh_value(PHI_PLUS, *OPTIMAL_ANGLES) - 2 * math.sqrt(2)) < TOL
    a0, a1, b0, b1 = OPTIMAL_ANGLES
    for a in (a0, a1):
        for b in (b0, b1):
            assert abs(correlation(PHI_PLUS, a, b) - math.cos(a - b)) < TOL


def test_classical_bound_is_two_by_brute_force() -> None:
    assert classical_chsh_max() == 2
    values = {a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1 for a0, a1, b0, b1 in deterministic_strategies()}
    assert values == {-2, 2}


def test_game_values() -> None:
    assert classical_game_value() == 0.75
    s = chsh_value(PHI_PLUS, *OPTIMAL_ANGLES)
    assert abs((0.5 + s / 8) - math.cos(math.pi / 8) ** 2) < TOL


def test_sampled_game_matches_cos_squared_pi_over_8() -> None:
    rounds = 20000
    wins = play_chsh_game(PHI_PLUS, random.Random(2024), rounds)
    # Hoeffding: P(|rate - p| >= 0.015) <= 2 exp(-2 * 20000 * 0.015^2) < 3e-4.
    assert abs(wins / rounds - math.cos(math.pi / 8) ** 2) < 0.015
    assert wins / rounds > 0.75 + 0.05


def test_no_state_or_angles_beat_tsirelson_and_products_stay_below_two() -> None:
    rng = random.Random(11)
    for _ in range(300):
        angles = [rng.uniform(-math.pi, math.pi) for _ in range(4)]
        assert abs(chsh_value(random_state(2, rng), *angles)) <= 2 * math.sqrt(2) + 1e-9
        product = kron_vec(random_state(1, rng), random_state(1, rng))
        assert abs(chsh_value(product, *angles)) <= 2 + 1e-9


def test_square_of_the_chsh_operator() -> None:
    rng = random.Random(5)
    for _ in range(20):
        A0, A1, B0, B1 = (observable(rng.uniform(-math.pi, math.pi)) for _ in range(4))
        S = mat_add(kron_mat(A0, mat_add(B0, B1)), kron_mat(A1, mat_add(B0, B1, 1, -1)))
        cA = mat_add(matmul(A0, A1), matmul(A1, A0), 1, -1)
        cB = mat_add(matmul(B0, B1), matmul(B1, B0), 1, -1)
        rhs = mat_add(identity(4), kron_mat(cA, cB), 4, -1)
        assert max_abs_diff(matmul(S, S), rhs) < 1e-12
        assert max(abs(v) for v in eigvalsh(S)) <= 2 * math.sqrt(2) + 1e-9
