# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/value-iteration/. The authors are listed in prov/XRA79Y.jsonl.

import itertools
import random
from fractions import Fraction as F

from value_iteration import greedy_policy, value_iteration

# The example of the page: states L = 0 and H = 1, actions stay = 0 and move = 1.
P2 = [[[(1, 0)], [(F(1, 2), 1), (F(1, 2), 0)]], [[(1, 1)], [(1, 0)]]]
R2 = [[F(1), F(0)], [F(2), F(0)]]
G2 = F(9, 10)


def solve(A, b):
    """Exact Gauss-Jordan elimination over fractions."""
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


def policy_value(P, R, gamma, pi):
    n = len(P)
    A = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for s in range(n):
        for p, t in P[s][pi[s]]:
            A[s][t] -= F(gamma) * F(p)
    return solve(A, [F(R[s][pi[s]]) for s in range(n)])


def brute_force(P, R, gamma):
    """V* as the componentwise max over all deterministic policies."""
    vals = [policy_value(P, R, gamma, pi) for pi in itertools.product(*[range(len(a)) for a in P])]
    return [max(v[s] for v in vals) for s in range(len(P))]


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


def test_example_iterates():
    want = [[F(1), F(2)], [F(19, 10), F(38, 10)], [F(271, 100), F(542, 100)]]
    for k, w in enumerate(want, 1):
        V, pi, its = value_iteration(P2, R2, G2, F(0), max_iter=k)
        assert V == w and its == k
    V, pi, _ = value_iteration(P2, R2, G2, F(0), max_iter=2)
    assert pi == [0, 0]
    V, pi, _ = value_iteration(P2, R2, G2, F(0), max_iter=3)
    assert pi == [1, 0]


def test_example_converges():
    V, pi, k = value_iteration(P2, R2, 0.9, 0.01)
    assert pi == [1, 0]
    assert abs(V[0] - 180 / 11) < 0.005 and abs(V[1] - 20) < 0.005
    assert brute_force(P2, R2, G2) == [F(180, 11), F(20)]


def test_edges():
    V, pi, k = value_iteration([[[(1, 0)]]], [[3.0]], 0.5, 1e-9)
    assert abs(V[0] - 6.0) < 1e-8 and pi == [0]
    V, pi, k = value_iteration(P2, R2, 0, 1e-9)
    assert V == [1, 2] and k == 1 and pi == [0, 0]
    assert value_iteration([], [], 0.5, 0.1, max_iter=1)[0] == []


def test_contraction_rate_exact():
    rng = random.Random(7)
    for _ in range(40):
        P, R = random_mdp(rng, rng.randint(1, 3), rng.randint(1, 3))
        g = F(rng.choice([1, 2, 3]), 4)
        vs = brute_force(P, R, g)
        top = max(abs(x) for x in vs)
        for k in range(1, 5):
            V, _, _ = value_iteration(P, R, g, F(0), max_iter=k)
            assert max(abs(a - b) for a, b in zip(V, vs)) <= g**k * top


def test_against_brute_force():
    rng = random.Random(2024)
    for _ in range(500):
        n, k = rng.randint(1, 3), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([F(1, 2), F(2, 3), F(9, 10)])
        eps = 1e-4
        V, pi, _ = value_iteration(P, R, float(g), eps)
        vs = brute_force(P, R, g)
        assert all(abs(V[s] - vs[s]) <= eps / 2 for s in range(n))
        vp = policy_value(P, R, g, pi)
        assert all(vs[s] - vp[s] <= eps for s in range(n))
        assert greedy_policy(P, R, g, vs) is not None
