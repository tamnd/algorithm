# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modified-policy-iteration/. The authors are listed in prov/1RG9V7.jsonl.

import itertools
import random
from fractions import Fraction as F

from modified_policy_iteration import modified_policy_iteration as mpi

P2 = [[[(1, 0)], [(F(1, 2), 1), (F(1, 2), 0)]], [[(1, 1)], [(1, 0)]]]
R2 = [[F(1), F(0)], [F(2), F(0)]]
G2 = F(9, 10)


def gauss(A, b):
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


def q(P, R, g, V, s, a):
    return R[s][a] + g * sum(p * V[t] for p, t in P[s][a])


def bellman(P, R, g, V):
    return [max(q(P, R, g, V, s, a) for a in range(len(P[s]))) for s in range(len(P))]


def greedy_keep(P, R, g, V, pi):
    out = []
    for s in range(len(P)):
        qs = [q(P, R, g, V, s, a) for a in range(len(P[s]))]
        out.append(pi[s] if qs[pi[s]] == max(qs) else qs.index(max(qs)))
    return out


def ref_value_iteration(P, R, g, V, k):
    out = []
    for _ in range(k):
        V = bellman(P, R, g, V)
        out.append(V)
    return out


def ref_policy_iteration(P, R, g, V0):
    pi = greedy_keep(P, R, g, V0, [0] * len(P))
    out = []
    while True:
        V = value_of(P, R, g, pi)
        out.append((pi, V))
        new = greedy_keep(P, R, g, V, pi)
        if new == pi:
            return out
        pi = new


def brute_force(P, R, g):
    vals = [value_of(P, R, g, pi) for pi in itertools.product(*[range(len(a)) for a in P])]
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


def test_example():
    for m, its in ((0, None), (2, None), (None, None)):
        V, pi, k = mpi(P2, R2, 0.9, m, 1e-6)
        assert pi == [1, 0] and abs(V[0] - 180 / 11) < 1e-6 and abs(V[1] - 20) < 1e-6
    h = []
    mpi(P2, R2, G2, 2, F(1, 10**6), max_iter=2, history=h)
    assert h[0] == ([0, 0], [F(271, 100), F(542, 100)])


def test_m_zero_is_value_iteration():
    rng = random.Random(5)
    for _ in range(300):
        P, R = random_mdp(rng, rng.randint(1, 3), rng.randint(1, 3))
        g = rng.choice([F(1, 2), F(9, 10)])
        V0 = [F(rng.randrange(-5, 6)) for _ in P]
        h = []
        mpi(P, R, g, 0, F(1, 10**9), v0=V0, max_iter=6, history=h)
        ref = ref_value_iteration(P, R, g, V0, 6)
        assert [v for _, v in h] == ref[: len(h)]


def test_m_infinity_is_policy_iteration():
    rng = random.Random(6)
    for _ in range(500):
        P, R = random_mdp(rng, rng.randint(1, 3), rng.randint(1, 3))
        g = rng.choice([F(1, 2), F(2, 3), F(9, 10)])
        V0 = [F(rng.randrange(-5, 6)) for _ in P]
        h = []
        V, pi, k = mpi(P, R, g, None, F(1, 10**9), v0=V0, history=h)
        vs = brute_force(P, R, g)
        if V0 == vs:  # the start is already the fixed point: stop before any solve
            assert h == [] and k == 1
        else:
            assert h == ref_policy_iteration(P, R, g, V0)
        assert V == vs and k == len(h) + 1


def test_sandwich_and_limit():
    rng = random.Random(8)
    for _ in range(500):
        n, k = rng.randint(1, 3), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([F(1, 2), F(2, 3), F(9, 10)])
        lo = min(min(r) for r in R) / (1 - g)
        V0 = [lo] * n
        vs = brute_force(P, R, g)
        m = rng.randint(1, 4)
        h = []
        mpi(P, R, g, m, F(1, 10**9), v0=V0, max_iter=4, history=h)
        W = V0
        for _, V in h:
            W = bellman(P, R, g, W)
            assert all(w <= v <= x for w, v, x in zip(W, V, vs))
        V, pi, _ = mpi(P, R, float(g), m, 1e-4, v0=[float(lo)] * n)
        vp = value_of(P, R, g, pi)
        assert all(x - y <= 1e-4 for x, y in zip(vs, vp))
