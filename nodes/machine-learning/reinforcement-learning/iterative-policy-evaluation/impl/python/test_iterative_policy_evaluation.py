# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-policy-evaluation/. The authors are listed in prov/SYAD7P.jsonl.

import random
from fractions import Fraction as F

from iterative_policy_evaluation import iterative_policy_evaluation as ipe


def gridworld():
    """The 4 x 4 grid of Sutton and Barto, Example 4.1: corners 0 and 15 are terminal."""
    P, R = [], []
    for s in range(16):
        r, c = divmod(s, 4)
        if s in (0, 15):
            P.append([[(1, s)]] * 4)
            R.append([0] * 4)
            continue
        rows = []
        for dr, dc in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            rr, cc = r + dr, c + dc
            t = rr * 4 + cc if 0 <= rr < 4 and 0 <= cc < 4 else s
            rows.append([(1, t)])
        P.append(rows)
        R.append([-1] * 4)
    pi = [[F(1, 4)] * 4 for _ in range(16)]
    return P, R, pi


def exact(P, R, g, pi):
    """V^pi by exact Gauss-Jordan elimination on (I - g P_pi) V = r_pi."""
    n = len(P)
    M = [[F(int(i == j)) for j in range(n)] + [F(0)] for i in range(n)]
    for s in range(n):
        for a in range(len(P[s])):
            M[s][n] += pi[s][a] * R[s][a]
            for p, t in P[s][a]:
                M[s][t] -= g * pi[s][a] * p
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def test_gridworld_first_sweeps():
    P, R, pi = gridworld()
    V, _ = ipe(P, R, 1, pi, 0, in_place=False, max_sweeps=1)
    assert V == [0] + [-1] * 14 + [0]
    V, _ = ipe(P, R, 1, pi, 0, in_place=False, max_sweeps=2)
    assert V[1] == F(-7, 4) and V[5] == -2
    V, _ = ipe(P, R, 1, pi, 0, in_place=False, max_sweeps=3)
    assert V[1] == F(-39, 16) and V[2] == F(-47, 16) and V[5] == F(-23, 8) and V[3] == -3


def test_gridworld_limit():
    P, R, pi = gridworld()
    want = [0, -14, -20, -22, -14, -18, -20, -20, -20, -20, -18, -14, -22, -20, -14, 0]
    for mode in (True, False):
        V, k = ipe(P, R, 1.0, pi, 1e-6, in_place=mode)
        assert all(abs(v - w) < 1e-4 for v, w in zip(V, want))


def test_edges():
    V, k = ipe([[[(1, 0)]]], [[2.0]], 0.5, [[1]], 1e-12)
    assert abs(V[0] - 4.0) < 1e-11
    V, k = ipe([[[(1, 0)], [(1, 0)]]], [[1, 3]], 0, [[F(1, 2), F(1, 2)]], F(1, 100))
    assert V == [2] and k == 2


def random_case(rng):
    n, k = rng.randint(1, 4), rng.randint(1, 3)
    P, R, pi = [], [], []
    for _ in range(n):
        rows = []
        for _ in range(k):
            w = [rng.randrange(4) for _ in range(n)]
            w[rng.randrange(n)] += 1
            rows.append([(F(x, sum(w)), t) for t, x in enumerate(w) if x])
        P.append(rows)
        R.append([F(rng.randrange(-4, 5)) for _ in range(k)])
        q = [rng.randrange(3) for _ in range(k)]
        q[rng.randrange(k)] += 1
        pi.append([F(x, sum(q)) for x in q])
    return P, R, pi


def test_against_exact_solve():
    rng = random.Random(31)
    for _ in range(500):
        P, R, pi = random_case(rng)
        g = rng.choice([F(1, 2), F(3, 4), F(9, 10)])
        want = exact(P, R, g, pi)
        theta = 1e-6
        bound = float(g) * theta / (1 - float(g))
        for mode in (True, False):
            V, k = ipe(P, R, float(g), pi, theta, in_place=mode)
            assert max(abs(v - float(w)) for v, w in zip(V, want)) <= bound + 1e-12


def test_contraction_each_sweep():
    rng = random.Random(32)
    for _ in range(200):
        P, R, pi = random_case(rng)
        g = rng.choice([F(1, 2), F(9, 10)])
        want = exact(P, R, g, pi)
        for mode in (True, False):
            V = [F(0)] * len(P)
            for _ in range(4):
                W, _ = ipe(P, R, g, pi, 0, in_place=mode, v0=V, max_sweeps=1)
                e0 = max(abs(a - b) for a, b in zip(V, want))
                e1 = max(abs(a - b) for a, b in zip(W, want))
                assert e1 <= g * e0
                V = W
