# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-entropy-leakage/. The authors are listed in prov/7HY8Q8.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

from min_entropy_leakage import (
    deterministic_channel,
    leakage_ratio,
    min_capacity,
    min_entropy_leakage,
    posterior_vulnerability,
    prior_vulnerability,
)


def uniform(n):
    return [F(1, n)] * n


def best_strategy(pi, c):
    """Oracle: try every map from outputs to guesses and keep the best success chance."""
    nx, ny = len(pi), len(c[0])
    best = F(0)
    for guess in itertools.product(range(nx), repeat=ny):
        win = sum(pi[guess[y]] * c[guess[y]][y] for y in range(ny))
        best = max(best, win)
    return best


def random_channel(rng, nx, ny):
    c = []
    for _ in range(nx):
        w = [rng.randint(0, 4) for _ in range(ny)]
        if sum(w) == 0:
            w[rng.randrange(ny)] = 1
        s = sum(w)
        c.append([F(v, s) for v in w])
    return c


def random_prior(rng, nx):
    w = [rng.randint(1, 6) for _ in range(nx)]
    return [F(v, sum(w)) for v in w]


def grid_priors(nx, d):
    for parts in itertools.product(range(d + 1), repeat=nx - 1):
        if sum(parts) <= d:
            yield [F(p, d) for p in parts] + [F(d - sum(parts), d)]


def test_mod_four() -> None:
    c, outs = deterministic_channel(lambda h: h % 4, 8)
    pi = uniform(8)
    assert outs == [0, 1, 2, 3]
    assert prior_vulnerability(pi) == F(1, 8)
    assert posterior_vulnerability(pi, c) == F(1, 2)
    assert leakage_ratio(pi, c) == 4
    assert min_entropy_leakage(pi, c) == 2.0


def test_binary_symmetric_channel() -> None:
    c = [[F(9, 10), F(1, 10)], [F(1, 10), F(9, 10)]]
    assert leakage_ratio(uniform(2), c) == F(9, 5)
    assert abs(min_entropy_leakage(uniform(2), c) - 0.847997) < 1e-6
    assert abs(min_capacity(c) - 0.847997) < 1e-6
    # A skewed prior: the best guess is 0 before and after, so nothing leaks.
    skew = [F(9, 10), F(1, 10)]
    assert posterior_vulnerability(skew, c) == F(9, 10)
    assert min_entropy_leakage(skew, c) == 0.0


def test_password_checker() -> None:
    c, _ = deterministic_channel(lambda h: h == 5, 8)
    assert posterior_vulnerability(uniform(8), c) == F(1, 4)
    assert min_entropy_leakage(uniform(8), c) == 1.0


def test_shannon_contrast() -> None:
    a, outs_a = deterministic_channel(lambda h: h if h % 8 == 0 else 1, 256)
    b, outs_b = deterministic_channel(lambda h: h & 7, 256)
    pi = uniform(256)
    assert len(outs_a) == 33 and len(outs_b) == 8
    assert posterior_vulnerability(pi, a) == F(33, 256)
    assert posterior_vulnerability(pi, b) == F(1, 32)
    assert abs(min_entropy_leakage(pi, a) - math.log2(33)) < 1e-12
    assert min_entropy_leakage(pi, b) == 3.0


def test_edges() -> None:
    # One secret: nothing to learn.
    assert min_entropy_leakage([F(1)], [[F(1, 2), F(1, 2)]]) == 0.0
    # A constant program and the identity program.
    pi = [F(1, 2), F(1, 4), F(1, 4)]
    const, _ = deterministic_channel(lambda h: 0, 3)
    ident, _ = deterministic_channel(lambda h: h, 3)
    assert min_entropy_leakage(pi, const) == 0.0
    assert posterior_vulnerability(pi, ident) == 1
    assert min_entropy_leakage(pi, ident) == 1.0
    # A point prior: the attacker already knows the secret.
    assert min_entropy_leakage([F(0), F(1), F(0)], ident) == 0.0


def test_against_strategy_enumeration() -> None:
    rng = random.Random(2009)
    for _ in range(600):
        nx, ny = rng.randint(1, 3), rng.randint(1, 3)
        c = random_channel(rng, nx, ny)
        pi = random_prior(rng, nx)
        v1 = posterior_vulnerability(pi, c)
        assert v1 == best_strategy(pi, c)
        assert v1 >= prior_vulnerability(pi)
        assert min_entropy_leakage(pi, c) >= 0.0
        assert min_entropy_leakage(pi, c) <= min_capacity(c) + 1e-12


def test_capacity_against_prior_grid() -> None:
    rng = random.Random(42)
    for _ in range(120):
        nx, ny = rng.randint(2, 3), rng.randint(1, 3)
        c = random_channel(rng, nx, ny)
        cap = sum(max(row[y] for row in c) for y in range(ny))
        best = max(leakage_ratio(p, c) for p in grid_priors(nx, 12))
        # The grid contains the uniform prior, which attains the capacity.
        assert best == cap
        assert leakage_ratio(uniform(nx), c) == cap


def test_deterministic_capacity_counts_outputs() -> None:
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(1, 8)
        table = [rng.randrange(4) for _ in range(n)]
        c, outs = deterministic_channel(lambda h: table[h], n)
        assert abs(min_capacity(c) - math.log2(len(outs))) < 1e-12
        assert abs(min_entropy_leakage(uniform(n), c) - math.log2(len(outs))) < 1e-12
