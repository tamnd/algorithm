# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extremal-optimization/. The authors are listed in prov/ZRWP63.jsonl.

import itertools
import math
import random

from extremal_optimization import (
    draw_rank,
    energy,
    ground_state,
    local_fitness,
    random_pm_j,
    rank_probabilities,
    tau_eo,
)

J12 = random_pm_j(12, random.Random(1))


def test_energy_identities() -> None:
    rng = random.Random(4)
    for _ in range(50):
        s = [rng.choice((-1, 1)) for _ in range(12)]
        lam = local_fitness(s, J12)
        e = energy(s, J12)
        assert e == -sum(lam) / 2
        for i in range(12):
            t = list(s)
            t[i] = -t[i]
            assert energy(t, J12) - e == 2 * lam[i]


def test_rank_distribution() -> None:
    n, tau = 12, 1 + 1 / math.log(12)
    p = rank_probabilities(n, tau)
    assert math.isclose(sum(p), 1.0)
    assert all(math.isclose(p[k] / p[k + 1], ((k + 2) / (k + 1)) ** tau) for k in range(n - 1))
    cum = list(itertools.accumulate(p))
    rng = random.Random(1)
    draws = 100000
    counts = [0] * n
    for _ in range(draws):
        counts[draw_rank(cum, rng) - 1] += 1
    assert max(abs(c / draws - q) for c, q in zip(counts, p)) < 0.01


def test_trace_flips_the_ranked_spin() -> None:
    for seed in range(10):
        trace = []
        s = [1] * 12
        best, eb = tau_eo(s, J12, 1.4, 100, random.Random(seed), trace)
        running = energy(s, J12)
        for k, i, lam_i, e in trace:
            lam = local_fitness(s, J12)
            order = sorted(range(12), key=lambda j: (lam[j], j))
            assert order[k - 1] == i and lam[i] == lam_i and energy(s, J12) == e
            s[i] = -s[i]
            running = min(running, energy(s, J12))
        assert eb == running == energy(best, J12)


def test_large_tau_flips_the_worst_spin() -> None:
    trace = []
    tau_eo([1] * 12, J12, 60.0, 50, random.Random(0), trace)
    assert all(k == 1 for k, _, _, _ in trace)


def test_fixed_seed_reaches_ground_state() -> None:
    _, eg = ground_state(J12)
    assert eg == -28
    best, eb = tau_eo([1] * 12, J12, 1 + 1 / math.log(12), 200, random.Random(0))
    assert eb == eg == energy(best, J12)
