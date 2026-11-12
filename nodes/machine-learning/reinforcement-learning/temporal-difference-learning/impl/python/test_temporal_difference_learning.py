# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/temporal-difference-learning/. The authors are listed in prov/WDFA4D.jsonl.

import random
from fractions import Fraction as F

from temporal_difference_learning import batch_td0, td0

# Random walk of Sutton and Barto, Example 6.2: A..E, right end pays 1.
EP1 = [("C", 0), ("B", 0), ("C", 0), ("D", 0), ("E", 1)]
EP2 = [("C", 0), ("D", 0), ("E", 0), ("D", 0), ("C", 0), ("B", 0), ("A", 0)]


def test_worked_example():
    V = {s: F(1, 2) for s in "ABCDE"}
    td0([EP1], F(1, 10), 1, V)
    assert V == {"A": F(1, 2), "B": F(1, 2), "C": F(1, 2), "D": F(1, 2), "E": F(11, 20)}
    td0([EP2], F(1, 10), 1, V)
    assert V["A"] == F(9, 20) and V["D"] == F(1009, 2000) and V["E"] == F(1091, 2000)
    assert V["B"] == V["C"] == F(1, 2)


def test_empty():
    assert td0([], 0.1, 1.0) == {}


def test_alpha_one_gamma_zero_keeps_last_reward():
    rng = random.Random(5)
    for _ in range(500):
        ep = [(rng.randrange(4), rng.randint(-5, 5)) for _ in range(rng.randint(1, 8))]
        V = td0([ep], 1, 0)
        last = {}
        for s, r in ep:
            last[s] = r
        assert V == last


def walk(rng):
    s, ep = 3, []
    while True:
        s2 = s + (1 if rng.random() < 0.5 else -1)
        ep.append((s, 1 if s2 == 6 else 0))
        if s2 in (0, 6):
            return ep
        s = s2


def test_random_walk_converges_with_decreasing_steps():
    rng = random.Random(3)
    V = td0((walk(rng) for _ in range(6000)), lambda n: n ** -0.75, 1.0, v0=0.5)
    for s in range(1, 6):
        assert abs(V[s] - s / 6) < 0.03


def test_you_are_the_predictor():
    # Sutton and Barto, Example 6.4: batch TD(0) gives V(A) = 3/4, batch MC gives V(A) = 0.
    batch = [[("A", 0), ("B", 0)]] + [[("B", 1)]] * 6 + [[("B", 0)]]
    V = batch_td0(batch, 0.05, 1.0)
    assert abs(V["B"] - 0.75) < 1e-9 and abs(V["A"] - 0.75) < 1e-9


def solve(A, b):
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def certainty_equivalence(batch, gamma):
    states = sorted({s for ep in batch for s, _ in ep})
    idx = {s: i for i, s in enumerate(states)}
    k = len(states)
    cnt = [0] * k
    rsum = [F(0)] * k
    trans = [[0] * k for _ in range(k)]
    for ep in batch:
        for t, (s, r) in enumerate(ep):
            cnt[idx[s]] += 1
            rsum[idx[s]] += r
            if t + 1 < len(ep):
                trans[idx[s]][idx[ep[t + 1][0]]] += 1
    A = [[(1 if i == j else 0) - gamma * F(trans[i][j], cnt[i]) for j in range(k)] for i in range(k)]
    b = [rsum[i] / cnt[i] for i in range(k)]
    return dict(zip(states, solve(A, b)))


def test_batch_td0_is_certainty_equivalence():
    rng = random.Random(11)
    for _ in range(60):
        batch = [[(rng.randrange(3), rng.randint(-2, 2)) for _ in range(rng.randint(1, 4))] for _ in range(rng.randint(1, 3))]
        g = F(1, 2)
        exact = certainty_equivalence(batch, g)
        total = sum(len(ep) for ep in batch)
        V = batch_td0(batch, 0.5 / total, 0.5, tol=1e-13)
        for s, v in exact.items():
            assert abs(V[s] - float(v)) < 1e-9
