# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/westfall-young-procedure/. The authors are listed in prov/3E4H4P.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from westfall_young_procedure import (
    max_t_adjusted,
    single_step_max_t,
    splits,
    two_sample_statistics,
    westfall_young_two_sample,
)


def closed_testing_brute_force(t_obs: list, t_perm: list) -> list[Fraction]:
    """Closed testing with the maxT permutation test for every intersection H_I.

    The local p-value of H_I is #{g : max_{j in I} T_j(g) >= max_{j in I} t_j} / |G|, and the adjusted
    p-value of H_i is the largest local p-value over the sets I that contain i.
    """
    m, b = len(t_obs), len(t_perm)
    adjusted = [Fraction(0)] * m
    for size in range(1, m + 1):
        for subset in itertools.combinations(range(m), size):
            t_max = max(t_obs[j] for j in subset)
            local = Fraction(sum(1 for row in t_perm if max(row[j] for j in subset) >= t_max), b)
            for i in subset:
                adjusted[i] = max(adjusted[i], local)
    return adjusted


def marginal_p_values(t_obs: list, t_perm: list) -> list[Fraction]:
    b = len(t_perm)
    return [Fraction(sum(1 for row in t_perm if row[j] >= t), b) for j, t in enumerate(t_obs)]


def holm_adjusted(p: list) -> list:
    m = len(p)
    order = sorted(range(m), key=lambda i: p[i])
    out, run = [0] * m, 0
    for k, i in enumerate(order):
        run = max(run, min(1, (m - k) * p[i]))
        out[i] = run
    return out


def random_data(rng: random.Random, n: int, m: int, shift: list, rho_scale: int = 3) -> list[list[int]]:
    """n units, m integer variables with a common unit effect; column j is shifted by shift[j] in rows 0..n/2-1."""
    rows = []
    for i in range(n):
        common = rng.gauss(0, 1) * rho_scale
        rows.append([round(10 * (common + rng.gauss(0, 1) + (shift[j] if i < n // 2 else 0))) for j in range(m)])
    return rows


def test_hand_example_two_copies() -> None:
    # Two identical variables, perfectly separated groups. Only the observed split and its mirror reach the
    # observed statistic |4 * 46 - 4 * 6| = 160, so every p-value is 2/70 = 1/35 = 0.0286.
    data = [[10, 10], [11, 11], [12, 12], [13, 13], [0, 0], [1, 1], [2, 2], [3, 3]]
    assert two_sample_statistics(data, range(4)) == [160, 160]
    reject, adjusted = westfall_young_two_sample(data, 4, Fraction(1, 20))
    assert adjusted == [Fraction(1, 35), Fraction(1, 35)]
    assert reject == [True, True]
    # Holm on the marginal permutation p-values pays for two tests: 2/35 = 0.057 > 0.05, nothing rejected.
    t_obs = two_sample_statistics(data, range(4))
    t_perm = [two_sample_statistics(data, s) for s in splits(8, 4)]
    assert holm_adjusted(marginal_p_values(t_obs, t_perm)) == [Fraction(2, 35), Fraction(2, 35)]


def test_hand_example_null_column() -> None:
    # The second variable is constant, so its statistic is 0 for every split and its adjusted p-value is 1.
    data = [[10, 5], [11, 5], [12, 5], [13, 5], [0, 5], [1, 5], [2, 5], [3, 5]]
    reject, adjusted = westfall_young_two_sample(data, 4)
    assert adjusted == [Fraction(1, 35), Fraction(1)]
    assert reject == [True, False]


def test_step_down_equals_closed_testing_on_matrices() -> None:
    rng = random.Random(1999)
    for _ in range(300):
        m = rng.randint(1, 6)
        b = rng.randint(1, 15)
        t_perm = [[rng.randint(0, 6) for _ in range(m)] for _ in range(b)]
        t_obs = t_perm[0]  # the identity row is the observed one
        assert max_t_adjusted(t_obs, t_perm) == closed_testing_brute_force(t_obs, t_perm)


def test_step_down_equals_closed_testing_on_two_sample_data() -> None:
    rng = random.Random(2003)
    for _ in range(25):
        m = rng.randint(1, 5)
        data = random_data(rng, 8, m, [rng.choice([0, 0, 2, 4]) for _ in range(m)])
        t_obs = two_sample_statistics(data, range(4))
        t_perm = [two_sample_statistics(data, s) for s in splits(8, 4)]
        assert len(t_perm) == 70
        assert max_t_adjusted(t_obs, t_perm) == closed_testing_brute_force(t_obs, t_perm)


def test_ordering_against_single_step_and_marginal() -> None:
    """marginal <= step-down <= single-step, for each hypothesis."""
    rng = random.Random(77)
    for _ in range(300):
        m = rng.randint(1, 6)
        t_perm = [[rng.randint(0, 9) for _ in range(m)] for _ in range(rng.randint(1, 12))]
        t_obs = [rng.randint(0, 9) for _ in range(m)]
        step = max_t_adjusted(t_obs, t_perm)
        single = single_step_max_t(t_obs, t_perm)
        marginal = marginal_p_values(t_obs, t_perm)
        assert all(a <= s for a, s in zip(step, single))
        assert all(mg <= a for mg, a in zip(marginal, step))
        # Adjusted p-values are monotone in the observed statistic.
        for i in range(m):
            for j in range(m):
                if t_obs[i] > t_obs[j]:
                    assert step[i] <= step[j]


def test_invalid_input() -> None:
    assert max_t_adjusted([], [[]]) == []
    with pytest.raises(ValueError):
        max_t_adjusted([1.0, 2.0], [])
    with pytest.raises(ValueError):
        max_t_adjusted([1.0, 2.0], [[1.0]])


def test_monte_carlo_fwer_and_power() -> None:
    """Correlated data, 2 true nulls and 2 false nulls, exact enumeration of the 70 splits in each run."""
    rng = random.Random(1993)
    alpha, reps = Fraction(1, 20), 500
    shift = [0, 0, 5, 5]
    fwer = 0
    rejections = {"wy": 0, "single": 0, "holm": 0}
    split_list = list(splits(8, 4))
    for _ in range(reps):
        data = random_data(rng, 8, 4, shift)
        t_obs = two_sample_statistics(data, range(4))
        t_perm = [two_sample_statistics(data, s) for s in split_list]
        wy = max_t_adjusted(t_obs, t_perm)
        single = single_step_max_t(t_obs, t_perm)
        holm = holm_adjusted(marginal_p_values(t_obs, t_perm))
        fwer += any(a <= alpha for a in wy[:2])
        rejections["wy"] += sum(a <= alpha for a in wy[2:])
        rejections["single"] += sum(a <= alpha for a in single[2:])
        rejections["holm"] += sum(a <= alpha for a in holm[2:])
    # The FWER is at most alpha = 0.05 by the theorem. With this seed it measures 0.030; the standard error
    # with 500 runs is about 0.01.
    assert fwer / reps <= 0.05 + 0.03
    # The smallest marginal permutation p-value is 2/70, so Holm needs 4 * 2/70 = 0.114 <= 0.05 and never
    # rejects. maxT rejects 28% of the false nulls here, and the step-down version at least as much as single-step.
    assert rejections["holm"] == 0
    assert rejections["wy"] >= rejections["single"] > 0
    assert 0.2 < rejections["wy"] / (2 * reps) < 0.36


def test_full_null_level_is_exact_for_the_global_test() -> None:
    """Under the complete null the identity row is uniform over the 70 rows, so P(min adjusted <= a) <= a."""
    rng = random.Random(5)
    data = random_data(rng, 8, 3, [0, 0, 0])
    split_list = list(splits(8, 4))
    # Relabeling the units by every split gives the exact distribution of the observed statistics.
    hits = 0
    for s in split_list:
        relabeled = [data[i] for i in s] + [data[i] for i in range(8) if i not in s]
        hits += min(max_t_adjusted(two_sample_statistics(relabeled, range(4)), [two_sample_statistics(relabeled, g) for g in split_list])) <= Fraction(4, 70)
    assert Fraction(hits, 70) <= Fraction(4, 70)
