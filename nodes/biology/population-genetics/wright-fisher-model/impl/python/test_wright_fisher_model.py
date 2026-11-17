# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wright-fisher-model/. The authors are listed in prov/ZKD5QR.jsonl.

import math
import random
from fractions import Fraction

from biostoch import binom_pmf, chi2_sf
from wright_fisher_model import (
    absorption,
    heterozygosity_decay,
    propagate,
    run_to_absorption,
    selected_frequency,
    simulate,
    transition_matrix,
)


def chi2_against(counts, probs, reps):
    """Pearson statistic with the cells of expected count < 5 pooled into one."""
    stat, df = 0.0, -1
    pool_o, pool_e = 0, 0.0
    for k, p in enumerate(probs):
        e = reps * p
        if e < 5:
            pool_o += counts.get(k, 0)
            pool_e += e
        else:
            stat += (counts.get(k, 0) - e) ** 2 / e
            df += 1
    if pool_e > 0:
        stat += (pool_o - pool_e) ** 2 / pool_e
        df += 1
    return stat, df


def test_one_step_is_binomial():
    rng = random.Random(1931)
    two_n, i, reps = 20, 7, 4000
    for s, h in ((0.0, 0.5), (0.3, 0.25)):
        counts = {}
        for _ in range(reps):
            x = simulate(rng, i, two_n, 1, s, h)[1]
            counts[x] = counts.get(x, 0) + 1
        p = selected_frequency(i / two_n, s, h)
        probs = [binom_pmf(k, two_n, p) for k in range(two_n + 1)]
        stat, df = chi2_against(counts, probs, reps)
        assert chi2_sf(stat, df) > 0.001


def test_selected_frequency():
    # Genic selection: fitnesses 1 + 2s', 1 + s', 1 gives p' = p (1 + s' + s' p) / (1 + 2 s' p).
    sp = Fraction(1, 10)
    p = Fraction(3, 10)
    assert selected_frequency(p, 2 * sp, Fraction(1, 2)) == p * (1 + sp + sp * p) / (1 + 2 * sp * p)
    assert selected_frequency(p, 0) == p
    assert selected_frequency(Fraction(0), Fraction(1, 2)) == 0
    assert selected_frequency(Fraction(1), Fraction(1, 2)) == 1


def test_rows_sum_to_one_and_martingale():
    for two_n in (1, 2, 5, 10):
        P = transition_matrix(two_n, exact=True)
        for i, row in enumerate(P):
            assert sum(row) == 1
            assert sum(j * pj for j, pj in enumerate(row)) == i


def test_neutral_fixation_is_initial_frequency():
    for two_n in (2, 6, 10):
        res = absorption(two_n, exact=True)
        assert res["fix"] == [Fraction(i, two_n) for i in range(two_n + 1)]
    res = absorption(20)
    for i in range(21):
        assert abs(res["fix"][i] - i / 20) < 1e-12


def test_exact_moments_by_propagation():
    # E[X_t] = X_0, E[H_t] = H_0 (1 - 1/(2N))^t and Var(p_t) = p0 q0 (1 - (1 - 1/(2N))^t).
    two_n, i0, t = 10, 3, 6
    P = transition_matrix(two_n, exact=True)
    d = propagate([Fraction(int(k == i0)) for k in range(two_n + 1)], P, t)
    p0 = Fraction(i0, two_n)
    lam = 1 - Fraction(1, two_n)
    mean_p = sum(Fraction(k, two_n) * dk for k, dk in enumerate(d))
    het = sum(2 * Fraction(k, two_n) * (1 - Fraction(k, two_n)) * dk for k, dk in enumerate(d))
    var_p = sum((Fraction(k, two_n) - p0) ** 2 * dk for k, dk in enumerate(d))
    assert mean_p == p0
    assert het == 2 * p0 * (1 - p0) * lam ** t
    assert var_p == p0 * (1 - p0) * (1 - lam ** t)


def test_heterozygosity_check_value():
    assert abs(heterozygosity_decay(50, 10) - 0.904382) < 5e-7


def test_simulated_fixation_against_exact_chain():
    # N = 10 diploids (2N = 20), fitnesses 1 + 2s, 1 + s, 1 with s = 0.05, one copy.
    rng = random.Random(1962)
    two_n, s, reps = 20, 0.05, 6000
    res = absorption(two_n, 2 * s, 0.5)
    u = res["fix"][1]
    assert abs(u - 0.10765) < 5e-6
    fixed = sum(run_to_absorption(rng, 1, two_n, 2 * s, 0.5)[0] for _ in range(reps))
    z = 4
    assert abs(fixed / reps - u) <= z * math.sqrt(u * (1 - u) / reps)


def test_simulated_absorption_time_against_exact_chain():
    rng = random.Random(2)
    two_n, i0, reps = 20, 10, 3000
    res = absorption(two_n)
    mu = res["time"][i0]
    var = res["time2"][i0] - mu * mu
    assert abs(mu - 26.229) < 5e-4
    total = sum(run_to_absorption(rng, i0, two_n)[1] for _ in range(reps))
    z = 4
    assert abs(total / reps - mu) <= z * math.sqrt(var / reps)


def test_edges():
    rng = random.Random(0)
    assert simulate(rng, 0, 10, 5) == [0]
    assert simulate(rng, 10, 10, 5) == [10]
    assert absorption(1, exact=True)["fix"] == [0, 1]
    try:
        simulate(rng, 11, 10, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
