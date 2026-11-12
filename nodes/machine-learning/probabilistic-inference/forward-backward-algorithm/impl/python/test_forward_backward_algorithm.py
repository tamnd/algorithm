# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-backward-algorithm/. The authors are listed in prov/JYNY94.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

import pytest

from forward_backward_algorithm import forward_backward, forward_backward_scaled, posterior_decode

PI = [F(1, 2), F(1, 2)]
A = [[F(7, 10), F(3, 10)], [F(2, 10), F(8, 10)]]
B = [[F(9, 10), F(1, 10)], [F(2, 10), F(8, 10)]]
OBS = [0, 0, 1, 0]


def rand_row(rng: random.Random, m: int) -> list:
    while True:
        w = [rng.randint(0, 5) for _ in range(m)]
        if sum(w):
            return [F(x, sum(w)) for x in w]


def rand_hmm(rng: random.Random, n: int, m: int):
    return rand_row(rng, n), [rand_row(rng, n) for _ in range(n)], [rand_row(rng, m) for _ in range(n)]


def floats(pi, a, b):
    return [float(x) for x in pi], [[float(x) for x in r] for r in a], [[float(x) for x in r] for r in b]


def path_prob(pi, a, b, obs, q):
    p = pi[q[0]] * b[q[0]][obs[0]]
    for t in range(1, len(obs)):
        p *= a[q[t - 1]][q[t]] * b[q[t]][obs[t]]
    return p


def brute(pi, a, b, obs):
    """Exact gamma, xi and P(O) by a sum over all N^T paths."""
    n, T = len(pi), len(obs)
    gamma = [[F(0)] * n for _ in range(T)]
    xi = [[[F(0)] * n for _ in range(n)] for _ in range(T - 1)]
    total = F(0)
    for q in product(range(n), repeat=T):
        p = path_prob(pi, a, b, obs, q)
        total += p
        for t in range(T):
            gamma[t][q[t]] += p
        for t in range(T - 1):
            xi[t][q[t]][q[t + 1]] += p
    if total:
        gamma = [[x / total for x in r] for r in gamma]
        xi = [[[x / total for x in r] for r in m] for m in xi]
    return gamma, xi, total


def test_worked_example() -> None:
    gamma, xi, p = forward_backward(PI, A, B, OBS)
    assert p == F(982301, 20000000)
    assert [[round(float(x), 4) for x in r] for r in gamma] == [[0.877, 0.123], [0.7974, 0.2026], [0.3086, 0.6914], [0.6478, 0.3522]]
    assert [[round(float(x), 4) for x in r] for r in xi[1]] == [[0.2965, 0.5009], [0.0121, 0.1905]]
    # posterior decoding R R D R differs from the Viterbi path R R R R here
    assert posterior_decode(gamma) == [0, 0, 1, 0]
    best = max(product(range(2), repeat=4), key=lambda q: path_prob(PI, A, B, OBS, q))
    assert best == (0, 0, 0, 0)


def test_against_enumeration() -> None:
    rng = random.Random(31)
    checked = 0
    for _ in range(600):
        n, m, T = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 5)
        pi, a, b = rand_hmm(rng, n, m)
        obs = [rng.randrange(m) for _ in range(T)]
        g0, x0, p0 = brute(pi, a, b, obs)
        if p0 == 0:
            with pytest.raises(ValueError):
                forward_backward(pi, a, b, obs)
            continue
        gamma, xi, p = forward_backward(pi, a, b, obs)
        assert (gamma, xi, p) == (g0, x0, p0)
        gs, xs, lp = forward_backward_scaled(*floats(pi, a, b), obs)
        assert math.isclose(lp, math.log(p0), rel_tol=1e-9, abs_tol=1e-12)
        for t in range(T):
            for i in range(n):
                assert math.isclose(gs[t][i], float(g0[t][i]), abs_tol=1e-12)
        for t in range(T - 1):
            for i in range(n):
                for j in range(n):
                    assert math.isclose(xs[t][i][j], float(x0[t][i][j]), abs_tol=1e-12)
        checked += 1
    assert checked > 300


def test_consistency_of_gamma_and_xi() -> None:
    rng = random.Random(4)
    for _ in range(100):
        n, m, T = rng.randint(1, 4), rng.randint(1, 3), rng.randint(2, 8)
        pi, a, b = rand_hmm(rng, n, m)
        obs = [rng.randrange(m) for _ in range(T)]
        try:
            gamma, xi, _ = forward_backward(pi, a, b, obs)
        except ValueError:
            continue
        for t in range(T):
            assert sum(gamma[t]) == 1
        for t in range(T - 1):
            for i in range(n):
                assert sum(xi[t][i]) == gamma[t][i]
                assert sum(xi[t][k][i] for k in range(n)) == gamma[t + 1][i]


def test_posterior_argmax_path_can_have_probability_zero() -> None:
    # States 0, 1, 2 and one symbol. Paths: (0,0) with 0.4, (1,1) with 0.3, (1,2) with 0.3.
    pi = [F(4, 10), F(6, 10), F(0)]
    a = [[F(1), F(0), F(0)], [F(0), F(1, 2), F(1, 2)], [F(0), F(0), F(1)]]
    b = [[F(1)], [F(1)], [F(1)]]
    obs = [0, 0]
    gamma, _, p = forward_backward(pi, a, b, obs)
    assert p == 1
    assert gamma == [[F(4, 10), F(6, 10), F(0)], [F(4, 10), F(3, 10), F(3, 10)]]
    post = posterior_decode(gamma)
    assert post == [1, 0]
    assert path_prob(pi, a, b, obs, post) == 0  # uses the transition 1 -> 0 with A = 0
    best = max(product(range(3), repeat=2), key=lambda q: path_prob(pi, a, b, obs, q))
    assert best == (0, 0) and path_prob(pi, a, b, obs, best) == F(4, 10)


def test_long_sequence_scaled() -> None:
    rng = random.Random(8)
    pi = [0.5, 0.3, 0.2]
    a = [[0.8, 0.1, 0.1], [0.2, 0.7, 0.1], [0.1, 0.2, 0.7]]
    b = [[0.6, 0.3, 0.1], [0.1, 0.6, 0.3], [0.2, 0.2, 0.6]]
    obs = [rng.randrange(3) for _ in range(3000)]
    gamma, xi, lp = forward_backward_scaled(pi, a, b, obs)
    assert math.isfinite(lp) and lp < -1000
    assert all(math.isclose(sum(g), 1.0, abs_tol=1e-9) for g in gamma)
    assert all(math.isclose(sum(map(sum, x)), 1.0, abs_tol=1e-9) for x in xi)
