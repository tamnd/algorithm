# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gillespie-algorithm/. The authors are listed in prov/TDM41K.jsonl.
"""Tests of the shared helper biostoch.py and of the direct method.

Every simulation test compares a sample statistic with an exact value. A
sample mean of n values with exact mean mu and variance var must satisfy
|mean - mu| <= 4 sqrt(var / n). A whole distribution must pass a chi-square
test with chi2_sf(statistic, df) > 0.001.
"""

import math
import random
import statistics

import biostoch
from biostoch import (
    binom_pmf,
    binomial,
    categorical,
    check_mean,
    chi2_sf,
    hypergeom_pmf,
    log_choose,
    logsumexp,
    mean_var,
    multinomial,
    nbinom_pmf,
    normal_sf,
    poisson,
    poisson_pmf,
    ssa_direct,
)
from gillespie_algorithm import direct_method, mass_action, state_at

Z = 4.0

# Networks with exact laws.
DEATH = [(-1,)]


def death_prop(x):
    return (1.0 * x[0],)


IMMIG_DEATH = [(1,), (-1,)]


def immig_death_prop(x):
    return (10.0, 1.0 * x[0])


def chi_square_ok(samples, pmf, support):
    """Chi-square test of samples against pmf on the integers of support.

    Cells with expected count below 5 are pooled from each end inward; the
    mass outside the support goes into the two end cells.
    """
    n = len(samples)
    counts = {}
    for s in samples:
        counts[s] = counts.get(s, 0) + 1
    lo, hi = support[0], support[-1]
    cells = []
    for k in support:
        e = n * pmf(k)
        o = counts.get(k, 0)
        cells.append([o, e])
    below = sum(c for s, c in counts.items() if s < lo)
    above = sum(c for s, c in counts.items() if s > hi)
    mass_in = sum(pmf(k) for k in support)
    cells[0][0] += below
    cells[-1][0] += above
    cells[-1][1] += n * max(0.0, 1.0 - mass_in)
    pooled = []
    acc = [0, 0.0]
    for o, e in cells:
        acc[0] += o
        acc[1] += e
        if acc[1] >= 5.0:
            pooled.append(acc)
            acc = [0, 0.0]
    if acc[1] > 0 or acc[0] > 0:
        if pooled:
            pooled[-1][0] += acc[0]
            pooled[-1][1] += acc[1]
        else:
            pooled.append(acc)
    if len(pooled) < 2:
        return True
    stat = sum((o - e) ** 2 / e for o, e in pooled)
    return chi2_sf(stat, len(pooled) - 1) > 0.001


# The helper: random variates

def test_poisson_small_and_large():
    rng = random.Random(1)
    for lam, n in ((0.7, 4000), (4.0, 4000), (75.0, 1500)):
        xs = [poisson(rng, lam) for _ in range(n)]
        m, v = mean_var(xs)
        assert check_mean(m, lam, lam, n, Z)
        hi = int(lam + 8 * math.sqrt(lam) + 8)
        assert chi_square_ok(xs, lambda k: poisson_pmf(k, lam), list(range(hi + 1)))
    assert poisson(rng, 0.0) == 0


def test_binomial_and_multinomial():
    rng = random.Random(2)
    n, p, reps = 20, 0.3, 4000
    xs = [binomial(rng, n, p) for _ in range(reps)]
    m, _ = mean_var(xs)
    assert check_mean(m, n * p, n * p * (1 - p), reps, Z)
    assert chi_square_ok(xs, lambda k: binom_pmf(k, n, p), list(range(n + 1)))
    assert binomial(rng, 0, 0.5) == 0 and binomial(rng, 7, 1.0) == 7
    probs = [0.2, 0.0, 0.5, 0.3]
    reps = 2000
    draws = [multinomial(rng, 50, probs) for _ in range(reps)]
    assert all(sum(d) == 50 and d[1] == 0 for d in draws)
    for i, q in enumerate(probs):
        if q > 0:
            m, _ = mean_var([d[i] for d in draws])
            assert check_mean(m, 50 * q, 50 * q * (1 - q), reps, Z)
    # Weights that do not sum to 1 are normalized.
    d = multinomial(random.Random(3), 10, [2, 2])
    assert sum(d) == 10


def test_categorical():
    rng = random.Random(4)
    w = [1.0, 0.0, 3.0, 6.0]
    n = 5000
    xs = [categorical(rng, w) for _ in range(n)]
    assert 1 not in xs
    assert chi_square_ok(xs, lambda k: w[k] / 10.0, [0, 2, 3])


# The helper: the direct method on networks with exact laws

def test_ssa_direct_pure_death_moments():
    # X -> 0 at rate 1 per molecule from 100: X(1) ~ Binomial(100, e^-1).
    rng = random.Random(5)
    reps = 150  # about 63 events per run
    xs = []
    for _ in range(reps):
        times, states, complete = ssa_direct(rng, (100,), DEATH, death_prop, 1.0)
        assert complete
        assert all(t <= 1.0 for t in times)
        xs.append(states[-1][0])
    mu = 100 * math.exp(-1)
    var = 100 * math.exp(-1) * (1 - math.exp(-1))
    assert abs(mu - 36.787944) < 1e-6 and abs(var - 23.254416) < 1e-6
    m, v = mean_var(xs)
    assert check_mean(m, mu, var, reps, Z)
    assert abs(v / var - 1) <= Z * math.sqrt(2 / (reps - 1))


def test_ssa_direct_pure_death_distribution():
    rng = random.Random(6)
    reps = 1200  # about 6.3 events per run
    q = math.exp(-1)
    xs = [ssa_direct(rng, (10,), DEATH, death_prop, 1.0)[1][-1][0] for _ in range(reps)]
    assert chi_square_ok(xs, lambda k: binom_pmf(k, 10, q), list(range(11)))


def test_ssa_direct_immigration_death_stationary():
    # 0 -> X at rate 10, X -> 0 at rate 1 per molecule. Start from the
    # stationary law Poisson(10); then X(t) ~ Poisson(10) for every t.
    rng = random.Random(7)
    reps = 800  # about 10 events per run
    xs = []
    for _ in range(reps):
        x0 = poisson(rng, 10.0)
        xs.append(ssa_direct(rng, (x0,), IMMIG_DEATH, immig_death_prop, 0.5)[1][-1][0])
    m, v = mean_var(xs)
    assert check_mean(m, 10.0, 10.0, reps, Z)
    assert abs(v / 10.0 - 1) <= Z * math.sqrt(2 / (reps - 1))
    assert chi_square_ok(xs, lambda k: poisson_pmf(k, 10.0), list(range(40)))


def test_ssa_direct_stops_and_repeats():
    # An absorbing state stops the run with complete = True.
    times, states, complete = ssa_direct(random.Random(8), (3,), DEATH, death_prop, 1e9)
    assert complete and states[-1] == (0,) and len(times) == 4
    # max_events cuts the run.
    times, states, complete = ssa_direct(random.Random(8), (0,), IMMIG_DEATH, immig_death_prop, 1e9, 25)
    assert not complete and len(times) == 26
    # The same seed gives the same trajectory.
    a = ssa_direct(random.Random(9), (5,), IMMIG_DEATH, immig_death_prop, 3.0)
    b = ssa_direct(random.Random(9), (5,), IMMIG_DEATH, immig_death_prop, 3.0)
    assert a == b


# The helper: statistics and exact functions

def test_mean_var_and_check_mean():
    rng = random.Random(10)
    xs = [rng.random() * 7 - 2 for _ in range(500)]
    m, v = mean_var(xs)
    assert abs(m - statistics.fmean(xs)) < 1e-12
    assert abs(v - statistics.variance(xs)) < 1e-12
    assert mean_var([3.0]) == (3.0, 0.0)
    assert check_mean(10.5, 10.0, 1.0, 64)  # 0.5 = 4 * sqrt(1 / 64)
    assert not check_mean(10.51, 10.0, 1.0, 64)


def test_pmfs_sum_to_one():
    assert abs(sum(binom_pmf(k, 30, 0.37) for k in range(31)) - 1) < 1e-12
    assert abs(sum(poisson_pmf(k, 10.0) for k in range(200)) - 1) < 1e-12
    assert abs(sum(nbinom_pmf(k, 5.0, 0.5) for k in range(2000)) - 1) < 1e-12
    assert abs(sum(hypergeom_pmf(k, 20, 7, 9) for k in range(10)) - 1) < 1e-12
    assert binom_pmf(0, 5, 0.0) == 1.0 and binom_pmf(5, 5, 1.0) == 1.0


def test_exact_functions():
    for n in range(12):
        for k in range(n + 1):
            assert abs(log_choose(n, k) - math.log(math.comb(n, k))) < 1e-12
    assert log_choose(4, 5) == -math.inf
    mu, alpha = 5.0, 0.5
    mean = sum(k * nbinom_pmf(k, mu, alpha) for k in range(3000))
    second = sum(k * k * nbinom_pmf(k, mu, alpha) for k in range(3000))
    assert abs(mean - mu) < 1e-9
    assert abs(second - mean ** 2 - (mu + alpha * mu ** 2)) < 1e-8
    assert nbinom_pmf(3, 2.0, 0.0) == poisson_pmf(3, 2.0)
    assert abs(hypergeom_pmf(2, 10, 4, 3) - math.comb(4, 2) * math.comb(6, 1) / math.comb(10, 3)) < 1e-14
    assert abs(logsumexp([1000.0, 1000.0]) - (1000.0 + math.log(2))) < 1e-12
    assert logsumexp([]) == -math.inf
    assert abs(normal_sf(1.959963984540054) - 0.025) < 1e-12
    assert abs(normal_sf(0.0, 3.0, 2.0) - normal_sf(-1.5)) < 1e-15


def test_chi2_sf():
    assert abs(chi2_sf(3.841, 1) - 0.05) < 1e-3
    for x in (0.01, 0.5, 1.0, 3.0, 10.0, 40.0):
        assert abs(chi2_sf(x, 2) - math.exp(-x / 2)) < 1e-12
        assert abs(chi2_sf(x, 1) - math.erfc(math.sqrt(x / 2))) < 1e-12
        # df = 4: Q(2, x/2) = e^(-x/2) (1 + x/2).
        assert abs(chi2_sf(x, 4) - math.exp(-x / 2) * (1 + x / 2)) < 1e-12
    assert chi2_sf(0.0, 3) == 1.0
    assert abs(chi2_sf(0.454936, 1) - 0.5) < 1e-6


def test_helper_header():
    with open(biostoch.__file__, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines[1].startswith("# Shared helper of the biology pages")


# The slug file: the direct method

# Dimerization 2A <-> B with A from a source: 0 -> A (c = 4), 2A -> B
# (c = 0.5, propensity 0.5 x_A (x_A - 1) / 2), B -> 2A (c = 1).
DIMER_STOICH = [(1, 0), (-2, 1), (2, -1)]
DIMER_PROP = mass_action([(0, 0), (2, 0), (0, 1)], [4.0, 0.5, 1.0])


def test_mass_action_counts_combinations():
    prop = mass_action([(0, 0), (1, 0), (1, 1), (2, 0)], [2.0, 3.0, 0.5, 0.5])
    assert prop((5, 4)) == [2.0, 15.0, 10.0, 5.0]
    assert prop((1, 0)) == [2.0, 3.0, 0.0, 0.0]


def test_direct_method_matches_helper():
    for seed in range(5):
        a = direct_method(random.Random(seed), (3, 1), DIMER_STOICH, DIMER_PROP, 5.0)
        b = ssa_direct(random.Random(seed), (3, 1), DIMER_STOICH, DIMER_PROP, 5.0)
        assert a == b and len(a[0]) > 10
    a = direct_method(random.Random(11), (7,), IMMIG_DEATH, immig_death_prop, 2.0, 5)
    b = ssa_direct(random.Random(11), (7,), IMMIG_DEATH, immig_death_prop, 2.0, 5)
    assert a == b and a[2] is False


def test_direct_method_pure_death():
    rng = random.Random(12)
    q = math.exp(-1)
    xs = [direct_method(rng, (10,), DEATH, death_prop, 1.0)[1][-1][0] for _ in range(1500)]
    assert chi_square_ok(xs, lambda k: binom_pmf(k, 10, q), list(range(11)))
    m, _ = mean_var(xs)
    assert check_mean(m, 10 * q, 10 * q * (1 - q), len(xs), Z)
    # Until extinction, the run has exactly x0 events.
    times, states, complete = direct_method(rng, (40,), DEATH, death_prop, math.inf)
    assert complete and len(times) == 41 and states[-1] == (0,)


def test_direct_method_immigration_death_from_zero():
    # From x0 = 0, X(t) ~ Poisson(10 (1 - e^(-t))).
    rng = random.Random(13)
    lam = 10 * (1 - math.exp(-1))
    xs = [direct_method(rng, (0,), IMMIG_DEATH, immig_death_prop, 1.0)[1][-1][0] for _ in range(1500)]
    m, _ = mean_var(xs)
    assert check_mean(m, lam, lam, len(xs), Z)
    assert chi_square_ok(xs, lambda k: poisson_pmf(k, lam), list(range(30)))


def test_direct_method_event_count():
    # In the stationary immigration-death process, events come at mean rate
    # 10 + E[X] = 20, so E[events in time T] = 20 T. Var(count) <= its mean
    # times 3 (a loose bound) is used for the tolerance.
    rng = random.Random(14)
    reps, t_end = 400, 1.0
    counts = []
    for _ in range(reps):
        x0 = poisson(rng, 10.0)
        counts.append(len(direct_method(rng, (x0,), IMMIG_DEATH, immig_death_prop, t_end)[0]) - 1)
    m, v = mean_var(counts)
    assert v < 3 * 20.0
    assert check_mean(m, 20.0 * t_end, 3 * 20.0, reps, Z)


def test_direct_method_one_step_law():
    # From x = (5, 4) the first event comes after Exp(a0) and is reaction j
    # with probability a_j / a0.
    a = DIMER_PROP((5, 4))
    a0 = sum(a)
    rng = random.Random(15)
    reps = 3000
    waits, picks = [], []
    for _ in range(reps):
        times, states, _ = direct_method(rng, (5, 4), DIMER_STOICH, DIMER_PROP, math.inf, 1)
        waits.append(times[1])
        d = (states[1][0] - 5, states[1][1] - 4)
        picks.append(DIMER_STOICH.index(d))
    m, _ = mean_var(waits)
    assert check_mean(m, 1 / a0, 1 / a0 ** 2, reps, Z)
    assert chi_square_ok(picks, lambda j: a[j] / a0, [0, 1, 2])


def test_state_at():
    times = [0.0, 0.5, 1.25]
    states = [(3,), (2,), (1,)]
    assert state_at(times, states, 0.0) == (3,)
    assert state_at(times, states, 0.49) == (3,)
    assert state_at(times, states, 0.5) == (2,)
    assert state_at(times, states, 9.0) == (1,)
