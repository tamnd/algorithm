# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moran-model/. The authors are listed in prov/QM5Y7F.jsonl.

import math
import random
from fractions import Fraction

from biostoch import chi2_sf
from moran_model import (
    absorption_times,
    fixation_by_sums,
    fixation_formula,
    rates,
    run_to_absorption,
    simulate,
    step,
    transition_matrix,
)


def test_one_step_law():
    rng = random.Random(1958)
    x, N, r, reps = 4, 10, 1.5, 4000
    b, d = rates(x, N, r)
    probs = {x + 1: b, x - 1: d, x: 1 - b - d}
    counts = {k: 0 for k in probs}
    for _ in range(reps):
        counts[step(rng, x, N, r)] += 1
    stat = sum((counts[k] - reps * p) ** 2 / (reps * p) for k, p in probs.items())
    assert chi2_sf(stat, 2) > 0.001


def test_fixation_formula_matches_birth_death_sums():
    for N in (2, 5, 10, 15):
        for r in (Fraction(1), Fraction(11, 10), Fraction(1, 2), Fraction(3)):
            for i in range(N + 1):
                assert fixation_formula(i, N, r) == fixation_by_sums(i, N, r)
    assert fixation_formula(3, 10, 1) == Fraction(3, 10)
    assert abs(float(fixation_formula(1, 10, Fraction(11, 10))) - 0.147950) < 5e-7


def test_neutral_absorption_time_closed_form():
    # t_i = N ((N - i) sum_{j=1}^{i} 1/(N - j) + i sum_{j=i+1}^{N-1} 1/j) steps.
    for N in (2, 6, 10):
        t, _ = absorption_times(N)
        for i in range(1, N):
            closed = N * ((N - i) * sum(Fraction(1, N - j) for j in range(1, i + 1))
                          + i * sum(Fraction(1, j) for j in range(i + 1, N)))
            assert t[i] == closed
    t, _ = absorption_times(10)
    assert t[1] == 10 * sum(Fraction(1, j) for j in range(1, 10))


def test_martingale_and_heterozygosity_decay():
    # Neutral: E[X'] = X and E[X'(N - X')] = X (N - X) (1 - 2/N^2) per step.
    N, steps = 8, 5
    P = transition_matrix(N)
    for i in range(N + 1):
        d = [Fraction(int(k == i)) for k in range(N + 1)]
        for _ in range(steps):
            d = [sum(d[a] * P[a][b] for a in range(N + 1)) for b in range(N + 1)]
        assert sum(k * dk for k, dk in enumerate(d)) == i
        het = sum(k * (N - k) * dk for k, dk in enumerate(d))
        assert het == i * (N - i) * (1 - Fraction(2, N * N)) ** steps


def test_simulated_fixation():
    rng = random.Random(10)
    N, r, reps = 10, 1.1, 8000
    u = float(fixation_formula(1, N, Fraction(11, 10)))
    fixed = sum(run_to_absorption(rng, 1, N, r)[0] for _ in range(reps))
    z = 4
    assert abs(fixed / reps - u) <= z * math.sqrt(u * (1 - u) / reps)


def test_simulated_absorption_time():
    rng = random.Random(64)
    N, i0, reps = 10, 5, 3000
    t, m2 = absorption_times(N)
    mu = float(t[i0])
    var = float(m2[i0] - t[i0] ** 2)
    total = sum(run_to_absorption(rng, i0, N)[1] for _ in range(reps))
    z = 4
    assert abs(total / reps - mu) <= z * math.sqrt(var / reps)


def test_edges():
    rng = random.Random(1)
    assert simulate(rng, 0, 5, 10) == [0]
    assert simulate(rng, 5, 5, 10) == [5]
    assert fixation_by_sums(1, 1, Fraction(2)) == 1
    assert rates(0, 5, 2) == (0, 0)
    try:
        simulate(rng, 6, 5, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
