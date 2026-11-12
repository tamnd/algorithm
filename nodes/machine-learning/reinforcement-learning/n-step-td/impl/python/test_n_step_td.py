# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/n-step-td/. The authors are listed in prov/FP2Z3F.jsonl.

import random
from fractions import Fraction as F

import pytest

from n_step_td import n_step_return, n_step_td

EP1 = [("C", 0), ("B", 0), ("C", 0), ("D", 0), ("E", 1)]
EP2 = [("C", 0), ("D", 0), ("E", 0), ("D", 0), ("C", 0), ("B", 0), ("A", 0)]


def online_box(episodes, n, alpha, gamma, V):
    """The online loop of Sutton and Barto, Section 7.1, step by step."""
    for ep in episodes:
        T = len(ep)
        S = [s for s, _ in ep]
        Rw = [None] + [r for _, r in ep]
        t = 0
        while True:
            tau = t - n + 1
            if tau >= 0:
                G = sum(gamma ** (i - tau - 1) * Rw[i] for i in range(tau + 1, min(tau + n, T) + 1))
                if tau + n < T:
                    G += gamma**n * V[S[tau + n]]
                V[S[tau]] += alpha * (G - V[S[tau]])
            if tau == T - 1:
                break
            t += 1
    return V


def td0(episodes, alpha, gamma, V):
    for ep in episodes:
        for t, (s, r) in enumerate(ep):
            tgt = r + (gamma * V[ep[t + 1][0]] if t + 1 < len(ep) else 0)
            V[s] += alpha * (tgt - V[s])
    return V


def mc(episodes, alpha, gamma, V):
    for ep in episodes:
        for t, (s, _) in enumerate(ep):
            G = sum(gamma**k * ep[t + k][1] for k in range(len(ep) - t))
            V[s] += alpha * (G - V[s])
    return V


def test_worked_example_n2():
    V = {s: F(1, 2) for s in "ABCDE"}
    n_step_td([EP1, EP2], 2, F(1, 10), 1, V)
    assert V == {"A": F(9, 20), "B": F(9, 20), "C": F(1009, 2000), "D": F(109, 200), "E": F(1091, 2000)}


def test_n1_is_td0_and_large_n_is_mc():
    rng = random.Random(9)
    for _ in range(500):
        eps = [[(rng.randrange(3), F(rng.randint(-2, 2))) for _ in range(rng.randint(1, 6))] for _ in range(2)]
        g = F(rng.randint(1, 4), 4)
        a = F(1, rng.randint(1, 5))
        start = {s: F(rng.randint(-2, 2)) for s in range(3)}
        assert n_step_td(eps, 1, a, g, dict(start)) == td0(eps, a, g, dict(start))
        assert n_step_td(eps, 6, a, g, dict(start)) == mc(eps, a, g, dict(start))
        n = rng.randint(1, 7)
        assert n_step_td(eps, n, a, g, dict(start)) == online_box(eps, n, a, g, dict(start))


def test_bad_n():
    with pytest.raises(ValueError):
        n_step_td([], 0, 0.1, 1.0)


def matpow_apply(P, k, x):
    for _ in range(k):
        x = [sum(P[i][j] * x[j] for j in range(len(x))) for i in range(len(x))]
    return x


def test_error_reduction_property_exact():
    # A Markov reward process on 3 states with a terminal state; P is substochastic.
    rng = random.Random(4)
    for _ in range(200):
        P = []
        for i in range(3):
            w = [rng.randint(0, 3) for _ in range(3)] + [rng.randint(1, 3)]  # the last entry is the terminal state
            P.append([F(x, sum(w)) for x in w[:3]])
        r = [F(rng.randint(-3, 3)) for _ in range(3)]
        g = F(rng.randint(1, 4), 4)
        # v = r + g P v, solved by Gauss-Jordan on (I - g P).
        A = [[(1 if i == j else 0) - g * P[i][j] for j in range(3)] + [r[i]] for i in range(3)]
        for c in range(3):
            p = next(k for k in range(c, 3) if A[k][c] != 0)
            A[c], A[p] = A[p], A[c]
            for k in range(3):
                if k != c and A[k][c] != 0:
                    f = A[k][c] / A[c][c]
                    A[k] = [x - f * y for x, y in zip(A[k], A[c])]
        v = [A[i][3] / A[i][i] for i in range(3)]
        V = [F(rng.randint(-6, 6), 2) for _ in range(3)]
        err = max(abs(V[i] - v[i]) for i in range(3))
        for n in range(1, 6):
            # E[G_(t:t+n) | S_t] = sum_k g^k P^k r + g^n P^n V
            ex = [F(0)] * 3
            for k in range(n):
                pk = matpow_apply(P, k, r)
                ex = [ex[i] + g**k * pk[i] for i in range(3)]
            pv = matpow_apply(P, n, V)
            ex = [ex[i] + g**n * pv[i] for i in range(3)]
            assert max(abs(ex[i] - v[i]) for i in range(3)) <= g**n * err


def test_n_step_return_definition():
    ep = [("a", 1), ("b", 0), ("a", 2)]
    V = {"a": F(1), "b": F(2)}
    g = F(1, 2)
    assert n_step_return(ep, 0, 1, g, V) == 1 + g * 2
    assert n_step_return(ep, 0, 2, g, V) == 1 + 0 + g * g * 1
    assert n_step_return(ep, 0, 3, g, V) == 1 + 0 + g * g * 2
    assert n_step_return(ep, 1, 5, g, V) == 0 + g * 2


def test_random_walk_converges():
    rng = random.Random(8)

    def walk():
        s, ep = 3, []
        while True:
            s2 = s + (1 if rng.random() < 0.5 else -1)
            ep.append((s, 1 if s2 == 6 else 0))
            if s2 in (0, 6):
                return ep
            s = s2

    V = {s: 0.5 for s in range(1, 6)}
    for k in range(1, 4001):
        n_step_td([walk()], 3, 0.5 / k**0.6, 1.0, V)
    for s in range(1, 6):
        assert abs(V[s] - s / 6) < 0.04
