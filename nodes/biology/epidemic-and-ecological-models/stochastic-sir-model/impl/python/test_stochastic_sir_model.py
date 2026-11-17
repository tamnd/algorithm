# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-sir-model/. The authors are listed in prov/EFGZYZ.jsonl.

import random
from fractions import Fraction as F

from biostoch import check_mean, chi2_sf, ssa_direct
from stochastic_sir_model import STOICH, final_size, final_size_distribution, propensity, simulate


def test_exact_final_size_small():
    # N = 3, one case, R0 = 2: the first event is an infection with
    # probability 2 * 2 / (2 * 2 + 3) = 4/7.
    d = final_size_distribution(3, 2, 1, F(2))
    assert d == {0: F(3, 7), 1: F(36, 175), 2: F(64, 175)}


def test_exact_law_sums_to_one():
    for n, i0, r0 in ((6, 1, F(3, 2)), (8, 2, F(1, 2)), (10, 1, F(4))):
        d = final_size_distribution(n, n - i0, i0, r0)
        assert sum(d.values()) == 1
        assert set(d) <= set(range(n - i0 + 1))


def test_same_path_as_ssa_direct():
    for seed in (1, 4, 9):
        _, ours = simulate(random.Random(seed), 50, 48, 2, 1.8, 1.0)
        _, ref, complete = ssa_direct(random.Random(seed), (48, 2), STOICH,
                                      propensity(1.8, 1.0, 50), float("inf"))
        assert complete and ours == ref


def test_simulated_final_size_matches_exact_law():
    rng = random.Random(20261118)
    n, runs, beta, gamma = 20, 3000, 1.5, 1.0
    exact = final_size_distribution(n, n - 1, 1, beta / gamma)
    counts = [0] * n
    for _ in range(runs):
        _, states = simulate(rng, n, n - 1, 1, beta, gamma)
        counts[final_size(states)] += 1
    stat = sum((counts[k] - runs * exact[k]) ** 2 / (runs * exact[k]) for k in range(n))
    assert chi2_sf(stat, n - 1) > 0.001


def test_minor_outbreak_probability_near_one_over_r0_power():
    # Truncate at N / 10 infections: the rest of the mass is a major outbreak.
    for n, r0, i0, approx in ((1000, 2.0, 1, 0.5), (1000, 2.0, 3, 0.125), (1000, 1.5, 1, 2 / 3)):
        minor = sum(final_size_distribution(n, n - i0, i0, r0, max_size=n // 10).values())
        assert minor > approx and minor - approx < 0.01


def test_simulated_minor_outbreak_frequency():
    rng = random.Random(3)
    n, runs, cut = 200, 1500, 20
    exact = sum(final_size_distribution(n, n - 1, 1, 2.0, max_size=cut).values())
    minor = 0
    for _ in range(runs):
        _, states = simulate(rng, n, n - 1, 1, 2.0, 1.0)
        minor += final_size(states) <= cut
    assert check_mean(minor / runs, exact, exact * (1 - exact), runs)


def test_t_end_stops_the_run():
    times, states = simulate(random.Random(2), 100, 99, 1, 3.0, 1.0, t_end=1.0)
    assert times[-1] <= 1.0
    assert all(s + i <= 100 for s, i in states)
