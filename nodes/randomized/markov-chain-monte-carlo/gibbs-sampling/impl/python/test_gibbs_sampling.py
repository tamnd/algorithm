# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gibbs-sampling/. The authors are listed in prov/JKAGEE.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from gibbs_sampling import gibbs_sampling, transition_matrix

TABLE = {(0, 0): F(4), (0, 1): F(1), (1, 0): F(2), (1, 1): F(3)}


def table_weight(x):
    return TABLE[tuple(x)]


def target(states, weight):
    z = sum(weight(s) for s in states)
    return [weight(s) / z for s in states]


def is_stationary(pi, p):
    n = len(pi)
    return all(sum(pi[a] * p[a][b] for a in range(n)) == pi[b] for b in range(n))


def is_reversible(pi, p):
    n = len(pi)
    return all(pi[a] * p[a][b] == pi[b] * p[b][a] for a in range(n) for b in range(n))


def solve(a, b):
    n = len(a)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        r = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[r] = m[r], m[c]
        m[c] = [v / m[c][c] for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] for i in range(n)]


def asymptotic_variance(p, pi, f):
    n = len(p)
    mu = sum(a * b for a, b in zip(pi, f))
    g = [v - mu for v in f]
    h = solve([[F(int(i == j)) - p[i][j] + pi[j] for j in range(n)] for i in range(n)], g)
    return sum(pi[i] * g[i] * (2 * h[i] - g[i]) for i in range(n))


def test_example_matrices() -> None:
    dom = [(0, 1), (0, 1)]
    states, ps = transition_matrix(table_weight, dom, "systematic")
    assert states == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert ps[0] == [F(8, 15), F(2, 15), F(2, 15), F(1, 5)]
    assert ps[1] == [F(1, 5), F(1, 20), F(3, 10), F(9, 20)]
    _, pr = transition_matrix(table_weight, dom, "random")
    assert pr[0] == [F(11, 15), F(1, 10), F(1, 6), F(0)]
    pi = target(states, table_weight)
    assert is_stationary(pi, ps) and is_stationary(pi, pr)
    assert is_reversible(pi, pr) and not is_reversible(pi, ps)


def test_random_tables_exact() -> None:
    rng = random.Random(31)
    for _ in range(5):
        dom = [(0, 1, 2), (0, 1), (0, 1, 2)]
        tab = {s: F(rng.randint(1, 9)) for s in itertools.product(*dom)}
        w = lambda x: tab[tuple(x)]
        for scan in ("systematic", "random"):
            states, p = transition_matrix(w, dom, scan)
            pi = target(states, w)
            assert is_stationary(pi, p)
            assert all(sum(row) == 1 for row in p)
            if scan == "random":
                assert is_reversible(pi, p)


def test_reducible_with_zeros() -> None:
    w = lambda x: F(1) if x[0] == x[1] else F(0)
    chain = gibbs_sampling(w, [(0, 1), (0, 1)], (0, 0), 200, random.Random(3))
    assert set(chain) == {(0, 0)}


def ising_cycle_weight(a, n):
    # pi(s) proportional to a^(number of agreeing edges) on the cycle C_n
    def w(x):
        return a ** sum(x[i] == x[(i + 1) % n] for i in range(n))
    return w


def run_and_compare(w_exact, w_float, dom, f, scan, steps, seed):
    states, p = transition_matrix(w_exact, dom, scan)
    pi = target(states, w_exact)
    fv = [F(f(s)) for s in states]
    mean = sum(a * b for a, b in zip(pi, fv))
    sd = math.sqrt(float(asymptotic_variance(p, pi, fv)) / steps)
    chain = gibbs_sampling(w_float, dom, states[0], steps, random.Random(seed), scan)
    est = sum(f(s) for s in chain) / steps
    assert abs(est - float(mean)) < 5 * sd
    return float(mean)


def test_ising_cycle_against_brute_force() -> None:
    n, a = 4, F(3)
    dom = [(-1, 1)] * n
    w_exact = ising_cycle_weight(a, n)
    w_float = ising_cycle_weight(3.0, n)
    agree = lambda s: sum(s[i] == s[(i + 1) % n] for i in range(n))
    # brute force partition function: sum over 2^4 states of 3^agree
    z = sum(3 ** agree(s) for s in itertools.product(*dom))
    assert z == 2 * 3 ** 4 + 12 * 3 ** 2 + 2 * 1 == 272
    m = run_and_compare(w_exact, w_float, dom, agree, "systematic", 40_000, 11)
    assert abs(m - sum(agree(s) * 3 ** agree(s) for s in itertools.product(*dom)) / z) < 1e-12
    run_and_compare(w_exact, w_float, dom, lambda s: sum(s) ** 2, "random", 120_000, 12)


def test_hard_core_cycle_against_brute_force() -> None:
    n = 5
    dom = [(0, 1)] * n

    def make(lam):
        def w(x):
            if any(x[i] and x[(i + 1) % n] for i in range(n)):
                return 0 * lam
            return lam ** sum(x)
        return w

    run_and_compare(make(F(2)), make(2.0), dom, sum, "systematic", 40_000, 13)


def test_bad_scan_name() -> None:
    with pytest.raises(ValueError):
        gibbs_sampling(table_weight, [(0, 1), (0, 1)], (0, 0), 1, random.Random(1), "diagonal")
