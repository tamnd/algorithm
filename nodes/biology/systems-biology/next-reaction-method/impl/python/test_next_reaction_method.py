# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-reaction-method/. The authors are listed in prov/KRZQSZ.jsonl.
"""Tests of the next reaction method.

A sample mean of n values with exact mean mu and variance var must satisfy
|mean - mu| <= 4 sqrt(var / n). A distribution must pass a chi-square test
with chi2_sf(statistic, df) > 0.001.
"""

import math
import random

from biostoch import (
    binom_pmf,
    check_mean,
    chi2_sf,
    mean_var,
    poisson,
    poisson_pmf,
    ssa_direct,
)
from next_reaction_method import (
    IndexedMinHeap,
    dependency_graph,
    mass_action_rates,
    next_reaction_method,
)

Z = 4.0

DEATH = [(-1,)]
DEATH_RATE, DEATH_DEP = mass_action_rates([(1,)], [1.0])
IMMIG_DEATH = [(1,), (-1,)]
ID_RATE, ID_DEP = mass_action_rates([(0,), (1,)], [10.0, 1.0])

# 0 -> A (c = 4), 2A -> B (c = 0.5, propensity 0.5 x_A (x_A - 1) / 2),
# B -> 2A (c = 1).
DIMER = [(1, 0), (-2, 1), (2, -1)]
DIMER_REACTANTS = [(0, 0), (2, 0), (0, 1)]
DIMER_RATE, DIMER_DEP = mass_action_rates(DIMER_REACTANTS, [4.0, 0.5, 1.0])


def dimer_prop(x):
    return [DIMER_RATE(j, x) for j in range(3)]


def pooled_stat(cells):
    pooled, acc = [], [0, 0.0]
    for o, e in cells:
        acc = [acc[0] + o, acc[1] + e]
        if acc[1] >= 5.0:
            pooled.append(acc)
            acc = [0, 0.0]
    if acc != [0, 0.0]:
        pooled[-1] = [pooled[-1][0] + acc[0], pooled[-1][1] + acc[1]]
    return sum((o - e) ** 2 / e for o, e in pooled), len(pooled) - 1


def chi_square_ok(samples, pmf, support):
    n = len(samples)
    counts = {}
    for s in samples:
        counts[s] = counts.get(s, 0) + 1
    assert all(s in support for s in counts)
    stat, df = pooled_stat([(counts.get(k, 0), n * pmf(k)) for k in support])
    return chi2_sf(stat, df) > 0.001


def two_sample_ok(xs, ys):
    keys = sorted(set(xs) | set(ys))
    cx, cy = {}, {}
    for v in xs:
        cx[v] = cx.get(v, 0) + 1
    for v in ys:
        cy[v] = cy.get(v, 0) + 1
    cells, acc = [], [0, 0]
    for k in keys:
        acc = [acc[0] + cx.get(k, 0), acc[1] + cy.get(k, 0)]
        if (acc[0] + acc[1]) / 2 >= 5:
            cells.append(acc)
            acc = [0, 0]
    if acc != [0, 0]:
        cells[-1] = [cells[-1][0] + acc[0], cells[-1][1] + acc[1]]
    nx, ny = len(xs), len(ys)
    stat = 0.0
    for ox, oy in cells:
        ex, ey = (ox + oy) * nx / (nx + ny), (ox + oy) * ny / (nx + ny)
        stat += (ox - ex) ** 2 / ex + (oy - ey) ** 2 / ey
    return chi2_sf(stat, len(cells) - 1) > 0.001


def test_indexed_heap_against_brute_force():
    rng = random.Random(31)
    keys = [rng.random() for _ in range(17)]
    heap = IndexedMinHeap(keys)
    for _ in range(2000):
        j = rng.randrange(17)
        k = math.inf if rng.random() < 0.1 else rng.random()
        heap.update(j, k)
        keys[j] = k
        top_key, top_j = heap.top()
        assert top_key == min(keys) and keys[top_j] == top_key
        assert all(heap.heap[heap.pos[i]] == i for i in range(17))


def test_dependency_graph():
    # R0: 0 -> A, R1: 2A -> B, R2: B -> 2A. R0 changes A, so it affects R1
    # (which reads A) and itself. R1 and R2 change A and B: they affect R1, R2.
    assert dependency_graph(DIMER, DIMER_DEP) == [[0, 1], [1, 2], [1, 2]]
    # A chain A -> B -> C -> 0: firing A -> B changes A and B.
    stoich = [(-1, 1, 0), (0, -1, 1), (0, 0, -1)]
    deps = [{0}, {1}, {2}]
    assert dependency_graph(stoich, deps) == [[0, 1], [1, 2], [2]]


def test_pure_death_law():
    rng = random.Random(32)
    q = math.exp(-1)
    xs = [next_reaction_method(rng, (10,), DEATH, DEATH_RATE, DEATH_DEP, 1.0)[1][-1][0]
          for _ in range(1500)]
    assert chi_square_ok(xs, lambda k: binom_pmf(k, 10, q), list(range(11)))
    reps = 150
    xs = [next_reaction_method(rng, (100,), DEATH, DEATH_RATE, DEATH_DEP, 1.0)[1][-1][0]
          for _ in range(reps)]
    mu, var = 100 * q, 100 * q * (1 - q)
    m, v = mean_var(xs)
    assert check_mean(m, mu, var, reps, Z)
    assert abs(v / var - 1) <= Z * math.sqrt(2 / (reps - 1))


def test_immigration_death():
    rng = random.Random(33)
    lam = 10 * (1 - math.exp(-1))
    xs = [next_reaction_method(rng, (0,), IMMIG_DEATH, ID_RATE, ID_DEP, 1.0)[1][-1][0]
          for _ in range(1500)]
    m, _ = mean_var(xs)
    assert check_mean(m, lam, lam, len(xs), Z)
    assert chi_square_ok(xs, lambda k: poisson_pmf(k, lam), list(range(max(xs) + 1)))
    reps = 800
    xs = []
    for _ in range(reps):
        x0 = poisson(rng, 10.0)
        xs.append(next_reaction_method(rng, (x0,), IMMIG_DEATH, ID_RATE, ID_DEP, 0.5)[1][-1][0])
    m, v = mean_var(xs)
    assert check_mean(m, 10.0, 10.0, reps, Z)
    assert abs(v / 10.0 - 1) <= Z * math.sqrt(2 / (reps - 1))


def test_same_law_as_direct_method():
    # From (1, 0) the reaction 2A -> B starts with propensity 0, so the
    # stored clock of a reaction that wakes up is used.
    reps = 1200
    rng_n, rng_d = random.Random(34), random.Random(35)
    nx = [next_reaction_method(rng_n, (1, 0), DIMER, DIMER_RATE, DIMER_DEP, 2.0)[1][-1]
          for _ in range(reps)]
    dx = [ssa_direct(rng_d, (1, 0), DIMER, dimer_prop, 2.0)[1][-1] for _ in range(reps)]
    assert two_sample_ok([s[0] for s in nx], [s[0] for s in dx])
    assert two_sample_ok([s[1] for s in nx], [s[1] for s in dx])


def test_one_step_law():
    x = (5, 4)
    a = dimer_prop(x)
    a0 = sum(a)
    rng = random.Random(36)
    reps = 3000
    waits, picks = [], []
    for _ in range(reps):
        times, states, _ = next_reaction_method(rng, x, DIMER, DIMER_RATE, DIMER_DEP, math.inf, 1)
        waits.append(times[1])
        picks.append(DIMER.index((states[1][0] - x[0], states[1][1] - x[1])))
    m, _ = mean_var(waits)
    assert check_mean(m, 1 / a0, 1 / a0 ** 2, reps, Z)
    assert chi_square_ok(picks, lambda j: a[j] / a0, [0, 1, 2])


class CountingRandom(random.Random):
    def __init__(self, seed):
        super().__init__(seed)
        self.calls = 0

    def expovariate(self, lambd=1.0):
        self.calls += 1
        return super().expovariate(lambd)


def test_one_random_number_per_event():
    rng = CountingRandom(37)
    times, states, complete = next_reaction_method(rng, (1, 0), DIMER, DIMER_RATE, DIMER_DEP, math.inf, 200)
    assert not complete
    assert rng.calls == 3 + 200
    # Pure death to extinction stops with complete = True.
    times, states, complete = next_reaction_method(random.Random(38), (6,), DEATH, DEATH_RATE, DEATH_DEP, math.inf)
    assert complete and len(times) == 7 and states[-1] == (0,)
