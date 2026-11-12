# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-programming-for-mdps/. The authors are listed in prov/YX6WMJ.jsonl.

import itertools
import random
from fractions import Fraction as F

from linear_programming_for_mdps import lp_mdp


def values(P, R, g, pi):
    """Independent oracle: V^pi by elimination with back substitution."""
    n = len(P)
    A = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    b = [F(R[s][pi[s]]) for s in range(n)]
    for s in range(n):
        for p, t in P[s][pi[s]]:
            A[s][t] -= g * p
    for c in range(n):
        r = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[r], b[c], b[r] = A[r], A[c], b[r], b[c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            A[r] = [x - f * y for x, y in zip(A[r], A[c])]
            b[r] -= f * b[c]
    x = [F(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x


def value_iteration(P, R, g, sweeps):
    V = [0.0] * len(P)
    for _ in range(sweeps):
        V = [max(R[s][a] + g * sum(p * V[t] for p, t in P[s][a]) for a in range(len(P[s]))) for s in range(len(P))]
    return V


def random_mdp(rng, n, k):
    P, R = [], []
    for _ in range(n):
        rows = []
        for _ in range(k):
            w = [rng.randrange(4) for _ in range(n)]
            w[rng.randrange(n)] += 1
            rows.append([(F(x, sum(w)), t) for t, x in enumerate(w) if x])
        P.append(rows)
        R.append([F(rng.randint(-3, 3)) for _ in range(k)])
    return P, R


def test_example():
    P = [[[(1, 0)], [(F(1, 2), 1), (F(1, 2), 0)]], [[(1, 1)], [(1, 0)]]]
    R = [[1, 0], [2, 0]]
    h = []
    V, x, pi, piv = lp_mdp(P, R, F(9, 10), history=h)
    assert V == [F(180, 11), 20] and pi == [1, 0] and piv == 1
    assert h == [[0, 0], [1, 0]]
    # Occupancy: x(L, move) = 20/11, x(H, stay) = 200/11; the total is 2 / (1 - 0.9).
    assert x[(0, 1)] == F(20, 11) and x[(1, 0)] == F(200, 11) and x[(0, 0)] == 0
    assert sum(x.values()) == 20
    assert x[(0, 1)] * 0 + x[(1, 0)] * 2 == V[0] + V[1]


def test_against_brute_force_and_duality():
    rng = random.Random(51)
    for _ in range(500):
        n, k = rng.randint(1, 4), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([F(1, 2), F(2, 3), F(9, 10)])
        alpha = [F(rng.randint(1, 5), rng.randint(1, 3)) for _ in range(n)]
        pi0 = [rng.randrange(k) for _ in range(n)]
        h = []
        V, x, pi, piv = lp_mdp(P, R, g, alpha, pi0, history=h)
        allv = [values(P, R, g, q) for q in itertools.product(range(k), repeat=n)]
        best = [max(v[s] for v in allv) for s in range(n)]
        assert V == best
        assert values(P, R, g, pi) == best
        # Primal feasibility, dual feasibility and strong duality, all exact.
        for s in range(n):
            for a in range(k):
                assert V[s] >= R[s][a] + g * sum(p * V[t] for p, t in P[s][a])
        assert all(v >= 0 for v in x.values())
        for t in range(n):
            inflow = sum(x[(s, a)] * p for s in range(n) for a in range(k) for p, u in P[s][a] if u == t)
            assert sum(x[(t, a)] for a in range(k)) - g * inflow == alpha[t]
        assert sum(R[s][a] * x[(s, a)] for s in range(n) for a in range(k)) == sum(
            al * v for al, v in zip(alpha, V)
        )
        # Each basis is a policy, each pivot switches one state, and the objective rises.
        assert h[0] == pi0 and len(h) == piv + 1
        objs = [sum(al * v for al, v in zip(alpha, values(P, R, g, q))) for q in h]
        for q0, q1, o0, o1 in zip(h, h[1:], objs, objs[1:]):
            assert sum(a != b for a, b in zip(q0, q1)) == 1 and o1 > o0


def test_against_value_iteration():
    rng = random.Random(52)
    for _ in range(200):
        n, k = rng.randint(1, 5), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([F(1, 2), F(2, 3)])
        V, _, _, _ = lp_mdp(P, R, g)
        Pf = [[[(float(p), t) for p, t in row] for row in st] for st in P]
        Rf = [[float(r) for r in st] for st in R]
        W = value_iteration(Pf, Rf, float(g), 80)
        assert all(abs(float(v) - w) < 1e-9 for v, w in zip(V, W))


def test_edges():
    V, x, pi, piv = lp_mdp([[[(1, 0)]]], [[3]], F(1, 2))
    assert V == [6] and x == {(0, 0): 2} and pi == [0] and piv == 0
    V, x, pi, piv = lp_mdp([[[(1, 0)], [(1, 0)]]], [[1, 5]], 0)
    assert V == [5] and pi == [1] and piv == 1
