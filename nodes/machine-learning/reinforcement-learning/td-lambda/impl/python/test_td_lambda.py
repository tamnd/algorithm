# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/td-lambda/. The authors are listed in prov/8STJSN.jsonl.

import random
from fractions import Fraction as F

from td_lambda import lambda_return, offline_lambda_return, td_lambda

EP1 = [("C", 0), ("B", 0), ("C", 0), ("D", 0), ("E", 1)]


def rand_case(rng):
    eps = [[(rng.randrange(3), F(rng.randint(-3, 3))) for _ in range(rng.randint(1, 7))] for _ in range(rng.randint(1, 3))]
    g = F(rng.randint(0, 4), 4)
    lam = F(rng.randint(0, 4), 4)
    a = F(1, rng.randint(1, 6))
    V = {s: F(rng.randint(-4, 4), 2) for s in range(3)}
    return eps, g, lam, a, V


def test_worked_example():
    V = {s: F(1, 2) for s in "ABCDE"}
    td_lambda([EP1], F(1, 2), F(1, 10), 1, V)
    assert V == {"A": F(1, 2), "B": F(81, 160), "C": F(33, 64), "D": F(21, 40), "E": F(11, 20)}


def test_forward_equals_backward_offline():
    rng = random.Random(12)
    for _ in range(500):
        eps, g, lam, a, V = rand_case(rng)
        assert td_lambda(eps, lam, a, g, dict(V), offline=True) == offline_lambda_return(eps, lam, a, g, dict(V))


def test_lambda_zero_online_is_td0():
    rng = random.Random(13)
    for _ in range(300):
        eps, g, _, a, V = rand_case(rng)
        W = dict(V)
        for ep in eps:
            for t, (s, r) in enumerate(ep):
                W[s] += a * (r + (g * W[ep[t + 1][0]] if t + 1 < len(ep) else 0) - W[s])
        assert td_lambda(eps, 0, a, g, dict(V)) == W


def test_lambda_one_offline_is_every_visit_mc():
    rng = random.Random(14)
    for _ in range(300):
        eps, g, _, a, V = rand_case(rng)
        W = dict(V)
        for ep in eps:
            inc = {}
            for t, (s, _) in enumerate(ep):
                G = sum(g**k * ep[t + k][1] for k in range(len(ep) - t))
                inc[s] = inc.get(s, 0) + a * (G - W[s])
            for s, d in inc.items():
                W[s] += d
        assert td_lambda(eps, 1, a, g, dict(V), offline=True) == W


def test_lambda_return_error_is_sum_of_td_errors():
    rng = random.Random(15)
    for _ in range(300):
        eps, g, lam, _, V = rand_case(rng)
        ep = eps[0]
        T = len(ep)
        v = lambda t: V[ep[t][0]] if t < T else 0
        d = [ep[t][1] + g * v(t + 1) - v(t) for t in range(T)]
        for t in range(T):
            assert lambda_return(ep, t, lam, g, V) - v(t) == sum((g * lam) ** (k - t) * d[k] for k in range(t, T))


def test_lambda_return_end_cases():
    ep = [("a", 1), ("b", 0), ("a", 2)]
    V = {"a": F(1), "b": F(2)}
    g = F(1, 2)
    assert lambda_return(ep, 0, 0, g, V) == 1 + g * 2
    assert lambda_return(ep, 0, 1, g, V) == 1 + 0 + g * g * 2


def test_empty():
    assert td_lambda([], 0.5, 0.1, 1.0) == {}


def test_random_walk_online_converges():
    rng = random.Random(16)

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
        td_lambda([walk()], 0.8, 0.3 / k**0.6, 1.0, V)
    for s in range(1, 6):
        assert abs(V[s] - s / 6) < 0.04
