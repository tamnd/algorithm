# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wang-landau/. The authors are listed in prov/V5BYBD.jsonl.

import functools
import itertools
import math
import random
from fractions import Fraction as F

import pytest

from wang_landau import frozen_walk_matrix, wang_landau

SIZE = 4
N = SIZE * SIZE
EDGES = [(i * SIZE + j, w) for i in range(SIZE) for j in range(SIZE) for w in (i * SIZE + (j + 1) % SIZE, ((i + 1) % SIZE) * SIZE + j)]
NB = [[w for u, w in EDGES if u == v] + [u for u, w in EDGES if w == v] for v in range(N)]
BETA_C = math.log(1 + math.sqrt(2)) / 2


@functools.lru_cache(maxsize=None)
def exact_g():
    g = {}
    for code in range(1 << N):
        s = [1 if code >> v & 1 else -1 for v in range(N)]
        e = -sum(s[u] * s[v] for u, v in EDGES)
        g[e] = g.get(e, 0) + 1
    return g


def propose(x, e, rng):
    v = rng.randrange(N)
    y = list(x)
    y[v] = -y[v]
    return y, e + 2 * x[v] * sum(x[w] for w in NB[v])


def normalized(ln_g):
    # fix the additive constant so that the estimated g sums to 2^N
    top = max(ln_g.values())
    ln_z = top + math.log(sum(math.exp(v - top) for v in ln_g.values()))
    return {e: v - ln_z + N * math.log(2) for e, v in ln_g.items()}


def max_error(ln_g):
    est = normalized(ln_g)
    return max(abs(est[e] - math.log(c)) for e, c in exact_g().items())


@functools.lru_cache(maxsize=None)
def run(ln_f_final, one_over_t, seed):
    levels = sorted(exact_g())
    ln_g, steps = wang_landau(levels, propose, [1] * N, -2 * N, random.Random(seed), ln_f_final=ln_f_final, one_over_t=one_over_t)
    return ln_g, steps


def test_exact_density_of_states() -> None:
    g = exact_g()
    assert sum(g.values()) == 2**N
    assert [g[e] for e in sorted(g)] == [2, 32, 64, 424, 1728, 6688, 13568, 20524, 13568, 6688, 1728, 424, 64, 32, 2]


def test_one_over_t_schedule_converges() -> None:
    ln_g, steps = run(1e-5, True, 1)
    assert steps == 15 * 10**5  # the 1/t rule stops when 15 / t < 1e-5
    assert max_error(ln_g) < 0.1


def test_halving_schedule_saturates() -> None:
    errors = [max_error(run(fin, False, 1)[0]) for fin in (1e-6, 1e-8)]
    # making the final factor 100 times smaller hardly changes the estimate: the error is frozen in
    assert abs(errors[0] - errors[1]) < 0.01
    assert min(errors) > 2 * max_error(run(1e-5, True, 1)[0])


def test_thermodynamics_at_the_critical_point() -> None:
    def mean_energy(ln_g):
        w = {e: v - BETA_C * e for e, v in ln_g.items()}
        top = max(w.values())
        z = sum(math.exp(v - top) for v in w.values())
        return sum(e * math.exp(v - top) for e, v in w.items()) / z

    exact = mean_energy({e: math.log(c) for e, c in exact_g().items()})
    assert exact == pytest.approx(-25.04998, abs=1e-5)
    assert mean_energy(run(1e-5, True, 1)[0]) == pytest.approx(exact, rel=0.01)


def test_frozen_walk_with_true_g_has_flat_energy_histogram() -> None:
    # Ising chain on the cycle of 5 vertices: energies -5, -1, 3 with g = 2, 20, 10
    n = 5
    states = list(itertools.product((-1, 1), repeat=n))

    def energy(s):
        return -sum(s[i] * s[(i + 1) % n] for i in range(n))

    g = {}
    for s in states:
        g[energy(s)] = g.get(energy(s), 0) + 1
    assert g == {-5: 2, -1: 20, 3: 10}

    def neighbours(s):
        return [s[:i] + (-s[i],) + s[i + 1 :] for i in range(n)]

    exact = {e: F(c) for e, c in g.items()}
    mat = frozen_walk_matrix(states, energy, neighbours, exact)
    pi = [1 / exact[energy(s)] for s in states]
    z = sum(pi)
    pi = [p / z for p in pi]
    m = len(states)
    assert all(sum(row) == 1 for row in mat)
    assert all(pi[i] * mat[i][j] == pi[j] * mat[j][i] for i in range(m) for j in range(m))
    for e in g:
        assert sum(p for p, s in zip(pi, states) if energy(s) == e) == F(1, 3)


def test_bad_inputs() -> None:
    rng = random.Random(7)
    with pytest.raises(ValueError):
        wang_landau([0, 1], propose, [1] * N, 5, rng)
    with pytest.raises(ValueError):
        wang_landau([0, 1], propose, [1] * N, 0, rng, flatness=1.5)
    with pytest.raises(ValueError):
        wang_landau([0, 1], propose, [1] * N, 0, rng, ln_f_final=0.0)
