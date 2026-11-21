# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-leakage/. The authors are listed in prov/XKQ40D.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

from g_leakage import (
    g_leakage,
    g_vulnerability,
    identity_gain,
    k_tries_gain,
    partition_gain,
    posterior_g_vulnerability,
)


def uniform(n):
    return [F(1, n)] * n


def min_entropy_ratio(pi, c):
    """Min-entropy leakage ratio written out directly, without a gain function."""
    post = sum(max(pi[x] * c[x][y] for x in range(len(pi))) for y in range(len(c[0])))
    return post / max(pi)


def min_capacity_ratio(c):
    return sum(max(row[y] for row in c) for y in range(len(c[0])))


def best_strategy(pi, c, gain):
    """Oracle: try every map from outputs to guesses and keep the best expected gain."""
    ny, nw = len(c[0]), len(gain)
    best = F(-1)
    for choice in itertools.product(range(nw), repeat=ny):
        val = sum(pi[x] * c[x][y] * gain[choice[y]][x] for y in range(ny) for x in range(len(pi)))
        best = max(best, val)
    return best


def random_channel(rng, nx, ny):
    c = []
    for _ in range(nx):
        w = [rng.randint(0, 4) for _ in range(ny)]
        if sum(w) == 0:
            w[rng.randrange(ny)] = 1
        c.append([F(v, sum(w)) for v in w])
    return c


def random_gain(rng, nw, nx):
    g = [[F(rng.randint(0, 4), 4) for _ in range(nx)] for _ in range(nw)]
    g[0][rng.randrange(nx)] = F(1)  # some guess has a positive gain
    return g


def grid_priors(nx, d):
    for parts in itertools.product(range(d + 1), repeat=nx - 1):
        if sum(parts) <= d:
            yield [F(p, d) for p in parts] + [F(d - sum(parts), d)]


def test_alvim_example_4() -> None:
    # Example 4 of Alvim, Chatzikokolakis, Palamidessi and Smith (CSF 2012).
    c = [[F(1, 2), F(1, 2)], [F(1), F(0)], [F(0), F(1)]]
    g = [[F(1), F(0), F(0)], [F(0), F(1), F(98, 100)], [F(0), F(98, 100), F(1)]]
    pi = uniform(3)
    assert g_vulnerability(pi, g) == F(33, 50)
    assert posterior_g_vulnerability(pi, c, g) == F(2, 3)
    assert abs(g_leakage(pi, c, g) - 0.014500) < 1e-6
    assert g_leakage(pi, c, identity_gain(3)) == 1.0


def test_partition_gain_sees_what_one_guess_misses() -> None:
    c = [[F(3, 5), F(2, 5)], [F(0), F(1)], [F(0), F(1)]]
    pi = [F(3, 5), F(1, 5), F(1, 5)]
    assert g_leakage(pi, c, identity_gain(3)) == 0.0
    g = partition_gain([[0], [1, 2]], 3)
    assert g_vulnerability(pi, g) == F(3, 5)
    assert posterior_g_vulnerability(pi, c, g) == F(19, 25)
    assert abs(g_leakage(pi, c, g) - math.log2(F(19, 15))) < 1e-12
    # Example 5 of Alvim et al. (2012): the same channel and prior with the gain of Example 4.
    gd = [[F(1), F(0), F(0)], [F(0), F(1), F(98, 100)], [F(0), F(98, 100), F(1)]]
    assert g_vulnerability(pi, gd) == F(3, 5)
    assert posterior_g_vulnerability(pi, c, gd) == F(756, 1000)
    assert abs(g_leakage(pi, c, gd) - 0.333424) < 1e-6


def test_k_tries_on_mod_four() -> None:
    c = [[F(int(h % 4 == y)) for y in range(4)] for h in range(8)]
    g = k_tries_gain(8, 2)
    assert len(g) == 28
    assert g_vulnerability(uniform(8), g) == F(1, 4)
    assert posterior_g_vulnerability(uniform(8), c, g) == 1
    assert g_leakage(uniform(8), c, g) == 2.0


def test_edges() -> None:
    # One output: nothing leaks for any gain.
    c = [[F(1)], [F(1)], [F(1)]]
    g = [[F(1, 2), F(1), F(0)], [F(1), F(0), F(1, 4)]]
    assert g_leakage([F(1, 2), F(1, 4), F(1, 4)], c, g) == 0.0
    # A single guess: V_g(pi, C) = V_g(pi), so nothing leaks.
    ident = [[F(1), F(0)], [F(0), F(1)]]
    assert g_leakage(uniform(2), ident, [[F(1), F(1, 3)]]) == 0.0


def test_against_strategies_and_theorems() -> None:
    rng = random.Random(2012)
    for _ in range(600):
        nx, ny, nw = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 3)
        c = random_channel(rng, nx, ny)
        w = [rng.randint(1, 5) for _ in range(nx)]
        pi = [F(v, sum(w)) for v in w]
        g = random_gain(rng, nw, nx)
        v0 = g_vulnerability(pi, g)
        v1 = posterior_g_vulnerability(pi, c, g)
        assert v1 == best_strategy(pi, c, g)
        # Theorem 4.1: g-leakage is never negative.
        assert v1 >= v0
        # Theorem 4.2: zero leakage iff one guess is best for every output.
        one_guess = any(
            all(
                sum(pi[x] * c[x][y] * g[k][x] for x in range(nx))
                == max(sum(pi[x] * c[x][y] * row[x] for x in range(nx)) for row in g)
                for y in range(ny)
            )
            for k in range(nw)
        )
        assert (v1 == v0) == one_guess
        # The identity gain gives min-entropy leakage.
        assert posterior_g_vulnerability(pi, c, identity_gain(nx)) / g_vulnerability(pi, identity_gain(nx)) == min_entropy_ratio(pi, c)


def test_miracle_bound_on_prior_grid() -> None:
    rng = random.Random(77)
    for _ in range(100):
        nx, ny, nw = rng.randint(2, 3), rng.randint(1, 3), rng.randint(1, 3)
        c = random_channel(rng, nx, ny)
        g = random_gain(rng, nw, nx)
        cap = min_capacity_ratio(c)
        for p in grid_priors(nx, 6):
            if g_vulnerability(p, g) > 0:
                # Theorem 5.1: the g-leakage never exceeds the min-capacity.
                assert posterior_g_vulnerability(p, c, g) <= cap * g_vulnerability(p, g)
