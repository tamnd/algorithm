# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-state-projection/. The authors are listed in prov/62X0PG.jsonl.
"""Tests of the finite state projection.

The exact laws are closed forms: Binomial(x0, e^-t) for pure death,
Binomial(x0, e^-t) + Poisson(10 (1 - e^-t)) for immigration-death, and
Binomial(N, p(t)) for N independent molecules that switch A <-> B. A
closed dimerization system is checked against a dense matrix exponential
by scaling and squaring of the Taylor series.
"""

import math

from finite_state_projection import expm_action, finite_state_projection, project_generator


def binom_pmf(k, n, p):
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def poisson_pmf(k, lam):
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def immigration_death_pmf(k, x0, t, b=10.0):
    q = math.exp(-t)
    lam = b * (1 - q)
    return sum(binom_pmf(i, x0, q) * poisson_pmf(k - i, lam) for i in range(min(k, x0) + 1))


DEATH = [(-1,)]


def death_prop(x):
    return (1.0 * x[0],)


IMMIG_DEATH = [(1,), (-1,)]


def immig_death_prop(x):
    return (10.0, 1.0 * x[0])


def test_pure_death_on_the_full_space():
    states = [(k,) for k in range(101)]
    J, p, lost, rounds = finite_state_projection((100,), DEATH, death_prop, 1.0, 1e-12, initial=states)
    assert rounds == 1 and abs(lost) < 1e-12
    q = math.exp(-1)
    assert max(abs(p[s] - binom_pmf(J[s][0], 100, q)) for s in range(len(J))) < 1e-12
    mean = sum(J[s][0] * p[s] for s in range(len(J)))
    var = sum(J[s][0] ** 2 * p[s] for s in range(len(J))) - mean ** 2
    assert abs(mean - 36.787944) < 1e-6 and abs(var - 23.254416) < 1e-6


def test_growth_reaches_the_tolerance_and_bounds_the_error():
    eps = 1e-6
    J, p, lost, rounds = finite_state_projection((0,), IMMIG_DEATH, immig_death_prop, 1.0, eps)
    assert 0 <= lost <= eps and rounds == len(J)
    exact = [immigration_death_pmf(x[0], 0, 1.0) for x in J]
    # The FSP value is below the exact value in every state.
    assert all(p[s] <= exact[s] + 1e-13 for s in range(len(J)))
    # The L1 error over all states is the lost mass.
    l1 = sum(abs(exact[s] - p[s]) for s in range(len(J))) + (1 - sum(exact))
    assert abs(l1 - lost) < 1e-12


def test_immigration_death_from_five():
    J, p, lost, _ = finite_state_projection((5,), IMMIG_DEATH, immig_death_prop, 2.0, 1e-9)
    assert lost <= 1e-9
    assert max(abs(p[s] - immigration_death_pmf(J[s][0], 5, 2.0)) for s in range(len(J))) <= 1e-9


def test_small_projection_loses_mass():
    # J = {0, ..., 5} for immigration-death from 0 at t = 1. Mass that leaves
    # J is lost even if the process could come back, so the lost mass is at
    # least the exact P(X(1) > 5), and it is still the L1 error.
    states = [(k,) for k in range(6)]
    J, p, lost, _ = finite_state_projection((0,), IMMIG_DEATH, immig_death_prop, 1.0, 1.0, initial=states)
    exact = [immigration_death_pmf(k, 0, 1.0) for k in range(6)]
    tail = 1 - sum(exact)
    assert lost >= tail > 0.3
    l1 = sum(abs(exact[s] - p[s]) for s in range(6)) + tail
    assert abs(l1 - lost) < 1e-12


def test_larger_projection_is_larger_everywhere():
    small = [(k,) for k in range(8)]
    large = [(k,) for k in range(15)]
    _, p_small, lost_small, _ = finite_state_projection((0,), IMMIG_DEATH, immig_death_prop, 1.0, 1.0, initial=small)
    _, p_large, lost_large, _ = finite_state_projection((0,), IMMIG_DEATH, immig_death_prop, 1.0, 1.0, initial=large)
    assert lost_large < lost_small
    assert all(p_small[s] <= p_large[s] + 1e-15 for s in range(8))


def test_two_state_molecules_are_binomial():
    # A -> B at rate 2 per molecule and B -> A at rate 1, 12 molecules, all
    # A at t = 0. Each molecule is A at time t with probability
    # 1/3 + 2/3 e^-3t, independently of the others.
    stoich = [(-1, 1), (1, -1)]

    def prop(x):
        return (2.0 * x[0], 1.0 * x[1])

    t = 0.4
    J, p, lost, _ = finite_state_projection((12, 0), stoich, prop, t, 1e-12)
    assert len(J) == 13 and abs(lost) < 1e-12
    pa = 1 / 3 + 2 / 3 * math.exp(-3 * t)
    assert max(abs(p[s] - binom_pmf(J[s][0], 12, pa)) for s in range(13)) < 1e-12


def dense_expm(a):
    """exp(a) by scaling and squaring of the Taylor series (dense)."""
    n = len(a)
    norm = max(sum(abs(v) for v in row) for row in a)
    s = max(0, math.ceil(math.log2(norm / 0.5))) if norm > 0.5 else 0
    b = [[v / 2 ** s for v in row] for row in a]
    result = [[float(i == j) for j in range(n)] for i in range(n)]
    term = [row[:] for row in result]
    for k in range(1, 30):
        term = [[sum(term[i][l] * b[l][j] for l in range(n)) / k for j in range(n)] for i in range(n)]
        result = [[result[i][j] + term[i][j] for j in range(n)] for i in range(n)]
    for _ in range(s):
        result = [[sum(result[i][l] * result[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
    return result


def test_dimerization_against_dense_expm():
    # 2A -> B with propensity 1 * x_A (x_A - 1) / 2 and B -> 2A at rate 0.5
    # per molecule, from (10, 0). The states are (10 - 2b, b), b = 0..5.
    stoich = [(-2, 1), (2, -1)]

    def prop(x):
        return (1.0 * x[0] * (x[0] - 1) / 2, 0.5 * x[1])

    t = 0.7
    J, p, lost, _ = finite_state_projection((10, 0), stoich, prop, t, 1e-12)
    assert sorted(J) == [(10 - 2 * b, b) for b in range(5, -1, -1)]
    # The dense generator, written from the reactions directly.
    n = 6
    gen = [[0.0] * n for _ in range(n)]
    for b in range(n):
        xa = 10 - 2 * b
        forward = xa * (xa - 1) / 2
        backward = 0.5 * b
        gen[b][b] = -(forward + backward)
        if b + 1 < n:
            gen[b + 1][b] += forward
        if b > 0:
            gen[b - 1][b] += backward
    e = dense_expm([[v * t for v in row] for row in gen])
    for s, x in enumerate(J):
        assert abs(p[s] - e[x[1]][0]) < 1e-11


def test_expm_action_of_zero_rates():
    out_rate, edges = project_generator([(0,)], DEATH, death_prop)
    assert out_rate == [0.0] and edges == []
    assert expm_action(out_rate, edges, [1.0], 5.0) == [1.0]
