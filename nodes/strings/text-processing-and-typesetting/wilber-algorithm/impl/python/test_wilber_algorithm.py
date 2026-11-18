# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wilber-algorithm/. The authors are listed in prov/BV1WAB.jsonl.

import math
import random
from fractions import Fraction

from wilber_algorithm import smawk, wilber


def lws_dp(n, w):
    F = [0] + [math.inf] * n
    for j in range(1, n + 1):
        F[j] = min(F[i] + w(i, j) for i in range(j))
    return F


def concave_weight(rng, n, line=None):
    """w(i, j) = f(S_j - S_i - l) + a(i) + b(j) with f convex: the quadrangle inequality holds."""
    S = [0]
    for _ in range(n):
        S.append(S[-1] + rng.randint(1, 6))
    a = [rng.randint(0, 20) for _ in range(n + 1)]
    b = [rng.randint(0, 20) for _ in range(n + 1)]
    l = rng.randint(5, 30)
    kind = rng.randrange(3)

    def w(i, j):
        if line is not None and S[j] - S[i] > line:
            return math.inf
        d = S[j] - S[i] - l
        if kind == 0:
            f = d * d
        elif kind == 1:
            f = abs(d) ** 3
        else:
            f = max(0, d) * 7 + max(0, -d)
        return f + a[i] + b[j]

    return w


def test_smawk_on_random_monge_arrays():
    rng = random.Random(1987)
    for _ in range(200):
        m, k = rng.randint(1, 15), rng.randint(1, 15)
        # a sum of a row term, a column term and a convex function of the difference is Monge
        u = sorted(rng.randint(0, 30) for _ in range(m))
        v = sorted(rng.randint(0, 30) for _ in range(k))
        ra = [rng.randint(0, 50) for _ in range(m)]
        cb = [rng.randint(0, 50) for _ in range(k)]
        f = lambda r, c: (u[r] - v[c]) ** 2 + ra[r] + cb[c]
        got = smawk(list(range(m)), list(range(k)), f)
        for r in range(m):
            vals = [f(r, c) for c in range(k)]
            assert got[r] == vals.index(min(vals))  # the leftmost minimum


def test_check_value():
    w = lambda i, j: (j - i - 3) ** 2
    F, P = wilber(10, w)
    assert F == [0, 4, 1, 0, 1, 1, 0, 1, 1, 0, 1]
    j, b = 10, []
    while j > 0:
        b.append(j)
        j = P[j]
    b.reverse()
    assert sum(w(i, j) for i, j in zip([0] + b, b)) == 1


def test_matches_dynamic_program():
    rng = random.Random(1988)
    for _ in range(200):
        n = rng.randint(1, 70)
        w = concave_weight(rng, n)
        F, P = wilber(n, w)
        assert F == lws_dp(n, w)
        for j in range(1, n + 1):
            assert F[P[j]] + w(P[j], j) == F[j]


def test_fractions_and_ties():
    rng = random.Random(8)
    for _ in range(60):
        n = rng.randint(1, 40)
        c = Fraction(rng.randint(1, 5), rng.randint(1, 5))
        w = lambda i, j, c=c: c * (j - i - 2) ** 2
        assert wilber(n, w)[0] == lws_dp(n, w)
        w2 = lambda i, j, c=c: c * (j - i) * (j - i)
        assert wilber(n, w2)[0] == lws_dp(n, w2)


def test_infinite_weights_can_fail():
    # math.inf for a line that is too long: inf == inf ties break SMAWK
    rng = random.Random(12)
    bad = 0
    for _ in range(150):
        n = rng.randint(1, 60)
        w = concave_weight(rng, n, line=rng.randint(6, 30))
        if wilber(n, w)[0] != lws_dp(n, w):
            bad += 1
    assert bad > 0


def test_lines_that_are_too_long_with_a_finite_penalty():
    rng = random.Random(12)
    K = 10**9
    for _ in range(150):
        n = rng.randint(1, 60)
        line = rng.randint(6, 30)
        S = [0]
        for _ in range(n):
            S.append(S[-1] + rng.randint(1, 6))
        l = rng.randint(5, line)
        w_inf = lambda i, j: math.inf if S[j] - S[i] > line else (S[j] - S[i] - l) ** 2
        w_fin = lambda i, j: (S[j] - S[i] - l) ** 2 + K * max(0, S[j] - S[i] - line)
        F = wilber(n, w_fin)[0]
        G = lws_dp(n, w_inf)
        assert F == lws_dp(n, w_fin)
        # every line fits here (word widths are at most 6 <= line), so the penalty is never paid
        assert F == G


def test_evaluations_are_linear():
    rng = random.Random(4)
    ratios = []
    for n in (500, 2000, 8000):
        w = concave_weight(rng, n)
        st = {}
        wilber(n, w, st)
        ratios.append(st["evals"] / n)
        assert st["evals"] <= 20 * n
    w = lambda i, j: (j - i - 3) ** 2
    st = {}
    wilber(8000, w, st)
    assert st["evals"] <= 20 * 8000
