# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hidden-semi-markov-model/. The authors are listed in prov/YCP2N2.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

import pytest

from hidden_semi_markov_model import forward, forward_log, from_hmm, validate


def rand_row(rng: random.Random, m: int, banned: int = -1, positive: bool = False) -> list:
    while True:
        w = [0 if k == banned else rng.randint(1 if positive else 0, 4) for k in range(m)]
        if sum(w):
            return [F(x, sum(w)) for x in w]


def rand_hsmm(rng: random.Random, n: int, m: int, D: int):
    pi = rand_row(rng, n)
    A = [rand_row(rng, n, banned=i) if n > 1 else [F(0)] for i in range(n)]
    P = [rand_row(rng, rng.randint(1, D)) for _ in range(n)]
    B = [rand_row(rng, m) for _ in range(n)]
    return pi, A, P, B


def segmentations(T: int, D: int):
    """All lists of durations, each in 1..D, with sum T, plus the open last segments (sum >= T)."""
    def rec(left):
        if left == 0:
            yield []
            return
        for d in range(1, D + 1):
            if d <= left:
                for rest in rec(left - d):
                    yield [d] + rest
    yield from rec(T)


def brute(pi, A, P, B, obs):
    """(p_end, p_censored) by listing every segmentation and every state labeling."""
    n, T = len(pi), len(obs)
    D = max(len(r) for r in P)
    pd = lambda j, d: P[j][d - 1] if d <= len(P[j]) else F(0)
    sv = lambda j, d: sum((P[j][e - 1] for e in range(d, len(P[j]) + 1)), F(0))
    p_end = p_cens = F(0)
    for durs in segmentations(T, D):
        for states in product(range(n), repeat=len(durs)):
            w, pos = F(1), 0
            for k, (j, d) in enumerate(zip(states, durs)):
                w *= pi[j] if k == 0 else A[states[k - 1]][j]
                for s in range(pos, pos + d):
                    w *= B[j][obs[s]]
                pos += d
            if w == 0:
                continue
            last_j, last_d = states[-1], durs[-1]
            core = w
            for j, d in zip(states[:-1], durs[:-1]):
                core *= pd(j, d)
            p_end += core * pd(last_j, last_d)
            p_cens += core * sv(last_j, last_d)
    return p_end, p_cens


def test_forward_matches_enumeration_of_segmentations() -> None:
    rng = random.Random(1980)
    for _ in range(150):
        n, m, D, T = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 5)
        pi, A, P, B = rand_hsmm(rng, n, m, D)
        validate(pi, A, P, B)
        obs = [rng.randrange(m) for _ in range(T)]
        _, p_end, p_cens = forward(pi, A, P, B, obs)
        assert (p_end, p_cens) == brute(pi, A, P, B, obs)


def test_censored_likelihoods_sum_to_one() -> None:
    rng = random.Random(4)
    pi, A, P, B = rand_hsmm(rng, 3, 2, 3)
    for T in range(1, 5):
        total = sum(forward(pi, A, P, B, list(o))[2] for o in product(range(2), repeat=T))
        assert total == 1


def hmm_paths(pi, A, B, obs):
    n = len(pi)
    for q in product(range(n), repeat=len(obs)):
        p = pi[q[0]] * B[q[0]][obs[0]]
        for t in range(1, len(obs)):
            p *= A[q[t - 1]][q[t]] * B[q[t]][obs[t]]
        yield q, p


def test_geometric_durations_give_the_hmm() -> None:
    rng = random.Random(9)
    for _ in range(60):
        n, m, T = rng.randint(2, 3), rng.randint(1, 3), rng.randint(1, 5)
        pi = rand_row(rng, n)
        A = [rand_row(rng, n) for _ in range(n)]
        if any(A[j][j] == 1 for j in range(n)):
            continue
        B = [rand_row(rng, m) for _ in range(n)]
        obs = [rng.randrange(m) for _ in range(T)]
        # D = T + 1: P_j(d) is exactly geometric for d <= T, and the tail sits at D
        hsmm = from_hmm(pi, A, B, T + 1)
        validate(*hsmm)
        assert all(sum(r) == 1 for r in hsmm[1] + hsmm[2])
        _, p_end, p_cens = forward(*hsmm, obs)
        paths = list(hmm_paths(pi, A, B, obs))
        assert p_cens == sum(p for _, p in paths)  # P(O) of the HMM
        # ending exactly at T means that the HMM leaves its last state at the next step
        assert p_end == sum(p * (1 - A[q[-1]][q[-1]]) for q, p in paths)


def hmm_log_likelihood(pi, A, B, obs) -> float:
    row = [pi[j] * B[j][obs[0]] for j in range(len(pi))]
    ll = 0.0
    for t in range(len(obs)):
        if t:
            row = [B[j][obs[t]] * sum(row[i] * A[i][j] for i in range(len(pi))) for j in range(len(pi))]
        s = sum(row)
        ll += math.log(s)
        row = [x / s for x in row]
    return ll


def test_log_space_on_a_long_sequence() -> None:
    rng = random.Random(77)
    pi = [0.5, 0.3, 0.2]
    A = [[0.9, 0.05, 0.05], [0.1, 0.85, 0.05], [0.2, 0.2, 0.6]]
    B = [[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.3, 0.3, 0.4]]
    T = 300
    obs = [rng.randrange(3) for _ in range(T)]
    hsmm = from_hmm(pi, A, B, T)
    _, lc = forward_log(*hsmm, obs)
    ref = hmm_log_likelihood(pi, A, B, obs)
    assert ref < -200  # far below the smallest float, as a probability
    assert math.isclose(lc, ref, rel_tol=1e-9)


def test_log_space_matches_exact_forward() -> None:
    rng = random.Random(12)
    for _ in range(40):
        pi, A, P, B = rand_hsmm(rng, 3, 3, 4)
        obs = [rng.randrange(3) for _ in range(rng.randint(1, 8))]
        _, pe, pc = forward(pi, A, P, B, obs)
        le, lc = forward_log([float(x) for x in pi], [[float(x) for x in r] for r in A],
                             [[float(x) for x in r] for r in P], [[float(x) for x in r] for r in B], obs)
        for exact, lg in ((pe, le), (pc, lc)):
            if exact == 0:
                assert lg == -math.inf
            else:
                assert math.isclose(lg, math.log(exact), rel_tol=1e-9, abs_tol=1e-12)


def test_worked_example() -> None:
    # the example on the page: two states, durations up to 3, O = (u, u, n, u)
    pi = [F(1, 2), F(1, 2)]
    A = [[F(0), F(1)], [F(1), F(0)]]
    P = [[F(1, 5), F(3, 10), F(1, 2)], [F(1, 2), F(1, 4), F(1, 4)]]
    B = [[F(9, 10), F(1, 10)], [F(2, 10), F(8, 10)]]
    obs = [0, 0, 1, 0]
    alpha, p_end, p_cens = forward(pi, A, P, B, obs)
    assert (p_end, p_cens) == brute(pi, A, P, B, obs)
    assert alpha[0] == [F(9, 100), F(1, 20)]
    assert alpha[1] == [F(261, 2000), F(7, 500)]
    assert p_end == F(4259, 200000)
    assert p_cens == F(72389, 1000000)


def test_errors() -> None:
    with pytest.raises(ValueError):
        validate([1.0, 0.0], [[0.5, 0.5], [1.0, 0.0]], [[1.0], [1.0]], [[1.0], [1.0]])
    with pytest.raises(ValueError):
        forward([1.0], [[0.0]], [[1.0]], [[1.0]], [])
