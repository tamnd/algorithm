# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/policy-iteration/. The authors are listed in prov/BW714H.jsonl.

import itertools
import random
from fractions import Fraction as F

from policy_iteration import evaluate_policy, policy_iteration

P2 = [[[(1, 0)], [(F(1, 2), 1), (F(1, 2), 0)]], [[(1, 1)], [(1, 0)]]]
R2 = [[F(1), F(0)], [F(2), F(0)]]
G2 = F(9, 10)


def gauss(A, b):
    """Independent exact solver (Gauss-Jordan, first nonzero pivot)."""
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


def value_of(P, R, g, pi):
    n = len(P)
    A = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for s in range(n):
        for p, t in P[s][pi[s]]:
            A[s][t] -= g * p
    return gauss(A, [R[s][pi[s]] for s in range(n)])


def brute_force(P, R, g):
    vals = [value_of(P, R, g, pi) for pi in itertools.product(*[range(len(a)) for a in P])]
    return [max(v[s] for v in vals) for s in range(len(P))]


def bellman(P, R, g, V):
    return [max(R[s][a] + g * sum(p * V[t] for p, t in P[s][a]) for a in range(len(P[s]))) for s in range(len(P))]


def random_mdp(rng, n, k):
    P, R = [], []
    for _ in range(n):
        rows, rew = [], []
        for _ in range(k):
            w = [rng.randrange(4) for _ in range(n)]
            w[rng.randrange(n)] += 1
            rows.append([(F(x, sum(w)), t) for t, x in enumerate(w) if x])
            rew.append(F(rng.randrange(-3, 4)))
        P.append(rows)
        R.append(rew)
    return P, R


def test_example():
    hist = []
    pi, V, k = policy_iteration(P2, R2, G2, [0, 0], history=hist)
    assert pi == [1, 0] and V == [F(180, 11), F(20)] and k == 2
    assert hist[0] == ([0, 0], [F(10), F(20)])


def test_edges():
    pi, V, k = policy_iteration([[[(1, 0)]]], [[F(3)]], F(1, 2))
    assert pi == [0] and V == [F(6)] and k == 1
    pi, V, k = policy_iteration(P2, R2, F(0), [1, 1])
    assert pi == [0, 0] and V == [1, 2]
    # all actions equal: the start policy is kept
    P = [[[(1, 0)], [(1, 0)]]]
    assert policy_iteration(P, [[F(1), F(1)]], F(1, 2), [1])[0] == [1]


def test_floats_with_tolerance():
    pi, V, k = policy_iteration(P2, [[1.0, 0.0], [2.0, 0.0]], 0.9, tol=1e-9)
    assert pi == [1, 0] and abs(V[0] - 180 / 11) < 1e-9


def test_against_brute_force_and_monotone():
    rng = random.Random(11)
    for _ in range(500):
        n, k = rng.randint(1, 3), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([F(1, 2), F(2, 3), F(9, 10)])
        pi0 = [rng.randrange(k) for _ in range(n)]
        hist = []
        pi, V, its = policy_iteration(P, R, g, pi0, history=hist)
        assert V == brute_force(P, R, g)
        assert V == value_of(P, R, g, pi)
        assert its <= k**n
        W = hist[0][1]
        for j in range(1, len(hist)):
            prev, cur = hist[j - 1][1], hist[j][1]
            assert all(c >= p for c, p in zip(cur, prev)) and cur != prev
            W = bellman(P, R, g, W)
            assert all(c >= w for c, w in zip(cur, W))
        assert evaluate_policy(P, R, g, pi) == V
