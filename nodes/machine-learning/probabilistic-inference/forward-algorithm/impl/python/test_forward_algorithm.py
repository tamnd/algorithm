# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-algorithm/. The authors are listed in prov/T75G2W.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

from forward_algorithm import forward, forward_log, forward_scaled

PI = [F(1, 2), F(1, 2)]
A = [[F(7, 10), F(3, 10)], [F(2, 10), F(8, 10)]]
B = [[F(9, 10), F(1, 10)], [F(2, 10), F(8, 10)]]
OBS = [0, 0, 1, 0]  # umbrella, umbrella, none, umbrella


def rand_row(rng: random.Random, m: int, zeros: bool = True) -> list:
    while True:
        w = [rng.randint(0 if zeros else 1, 5) for _ in range(m)]
        if sum(w):
            return [F(x, sum(w)) for x in w]


def rand_hmm(rng: random.Random, n: int, m: int):
    return rand_row(rng, n), [rand_row(rng, n) for _ in range(n)], [rand_row(rng, m) for _ in range(n)]


def brute_likelihood(pi, a, b, obs):
    """Sum of P(Q, O) over all N^T state paths Q."""
    total = F(0) if obs else F(1)
    if not obs:
        return total
    for q in product(range(len(pi)), repeat=len(obs)):
        p = pi[q[0]] * b[q[0]][obs[0]]
        for t in range(1, len(obs)):
            p *= a[q[t - 1]][q[t]] * b[q[t]][obs[t]]
        total += p
    return total


def floats(pi, a, b):
    return [float(x) for x in pi], [[float(x) for x in r] for r in a], [[float(x) for x in r] for r in b]


def test_worked_example() -> None:
    alpha, p = forward(PI, A, B, OBS)
    assert alpha[0] == [F(9, 20), F(1, 10)]
    assert alpha[1] == [F(603, 2000), F(43, 1000)]
    assert alpha[2] == [F(4393, 200000), F(2497, 25000)]
    assert alpha[3] == [F(636327, 20000000), F(172987, 10000000)]
    assert p == F(982301, 20000000)
    _, norms, lp = forward_scaled(*floats(PI, A, B), OBS)
    assert [round(x, 6) for x in norms] == [0.55, 0.626364, 0.353687, 0.403095]
    assert math.isclose(lp, math.log(0.04911505), rel_tol=1e-12)


def test_edges() -> None:
    assert forward(PI, A, B, []) == ([], 1)
    assert forward_log(*floats(PI, A, B), []) == 0.0
    # one state, one symbol: every sequence has probability 1
    assert forward([F(1)], [[F(1)]], [[F(1)]], [0] * 7)[1] == 1
    # an impossible observation: state 0 emits only symbol 0, and the chain stays in 0
    pi, a, b = [F(1), F(0)], [[F(1), F(0)], [F(0), F(1)]], [[F(1), F(0)], [F(0), F(1)]]
    assert forward(pi, a, b, [0, 1])[1] == 0
    assert forward_scaled(*floats(pi, a, b), [0, 1])[2] == -math.inf
    assert forward_log(*floats(pi, a, b), [0, 1]) == -math.inf


def test_against_enumeration_exact() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        n, m, t = rng.randint(1, 3), rng.randint(1, 3), rng.randint(0, 5)
        pi, a, b = rand_hmm(rng, n, m)
        obs = [rng.randrange(m) for _ in range(t)]
        assert forward(pi, a, b, obs)[1] == brute_likelihood(pi, a, b, obs)


def test_probabilities_sum_to_one() -> None:
    rng = random.Random(7)
    for _ in range(30):
        n, m, t = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 4)
        pi, a, b = rand_hmm(rng, n, m)
        assert sum(forward(pi, a, b, list(o))[1] for o in product(range(m), repeat=t)) == 1


def test_scaled_rows_are_filtered_distributions() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n, m, t = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 6)
        pi, a, b = rand_hmm(rng, n, m)
        obs = [rng.randrange(m) for _ in range(t)]
        alpha, p = forward(pi, a, b, obs)
        hat, norms, lp = forward_scaled(*floats(pi, a, b), obs)
        if p == 0:
            assert lp == -math.inf
            continue
        assert math.isclose(lp, math.log(p), rel_tol=1e-9, abs_tol=1e-12)
        for s in range(t):
            z = sum(alpha[s])
            for j in range(n):
                assert math.isclose(hat[s][j], float(alpha[s][j] / z), abs_tol=1e-12)
            # the product of the first s+1 norms is P(o_1..o_(s+1))
            assert math.isclose(math.fsum(math.log(x) for x in norms[: s + 1]), math.log(z), rel_tol=1e-9, abs_tol=1e-12)


def test_long_sequence_exact_log_likelihood() -> None:
    rng = random.Random(5)
    pi = [F(1, 3), F(1, 3), F(1, 3)]
    a = [[F(8, 10), F(1, 10), F(1, 10)], [F(2, 10), F(7, 10), F(1, 10)], [F(1, 10), F(2, 10), F(7, 10)]]
    b = [[F(6, 10), F(3, 10), F(1, 10)], [F(1, 10), F(6, 10), F(3, 10)], [F(2, 10), F(2, 10), F(6, 10)]]
    obs = [rng.randrange(3) for _ in range(400)]
    exact = forward(pi, a, b, obs)[1]
    log_exact = math.log(exact.numerator) - math.log(exact.denominator)
    fp = floats(pi, a, b)
    assert math.isclose(forward_scaled(*fp, obs)[2], log_exact, rel_tol=1e-10)
    assert math.isclose(forward_log(*fp, obs), log_exact, rel_tol=1e-10)


def test_plain_floats_underflow_but_scaled_do_not() -> None:
    rng = random.Random(9)
    r = random.Random(3)
    pi = rand_row(r, 3, zeros=False)
    a = [rand_row(r, 3, zeros=False) for _ in range(3)]
    b = [rand_row(r, 3, zeros=False) for _ in range(3)]
    fp = floats(pi, a, b)
    obs = [rng.randrange(3) for _ in range(2000)]
    assert forward(*fp, obs)[1] == 0.0  # underflow: the true value is about e^-2000 or less
    lp = forward_scaled(*fp, obs)[2]
    assert math.isfinite(lp) and lp < -700
    assert math.isclose(lp, forward_log(*fp, obs), rel_tol=1e-9)
