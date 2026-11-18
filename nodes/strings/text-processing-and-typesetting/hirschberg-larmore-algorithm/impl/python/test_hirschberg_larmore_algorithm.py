# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hirschberg-larmore-algorithm/. The authors are listed in prov/HFGGSH.jsonl.

import math
import random
from fractions import Fraction

from hirschberg_larmore_algorithm import breaks, hirschberg_larmore, lws_dp


def concave_weight(rng, n, line=None):
    """w(i, j) = f(S_j - S_i - l) + a(i) + b(j) with f convex: concave in the sense of the page."""
    widths = [rng.randint(1, 6) for _ in range(n)]
    S = [0]
    for x in widths:
        S.append(S[-1] + x)
    a = [rng.randint(0, 20) for _ in range(n + 1)]
    b = [rng.randint(0, 20) for _ in range(n + 1)]
    l = rng.randint(5, 30)
    kind = rng.randrange(3)

    def w(i, j):
        d = S[j] - S[i] - l
        if line is not None and S[j] - S[i] > line:
            return math.inf
        if kind == 0:
            f = d * d
        elif kind == 1:
            f = abs(d) ** 3
        else:
            f = max(0, d) * 7 + max(0, -d)
        return f + a[i] + b[j]

    return w


def quadrangle_holds(n, w):
    for i in range(n + 1):
        for i2 in range(i, n + 1):
            for j in range(max(i2, i + 1), n + 1):
                for j2 in range(j, n + 1):
                    if i2 >= j:
                        continue
                    if w(i, j) + w(i2, j2) > w(i, j2) + w(i2, j):
                        return False
    return True


def test_check_value():
    w = lambda i, j: (j - i - 3) ** 2
    F, P = hirschberg_larmore(10, w)
    assert F == [0, 4, 1, 0, 1, 1, 0, 1, 1, 0, 1]
    assert F[10] == 1
    assert F == lws_dp(10, w)[0]
    assert sum(w(i, j) for i, j in zip([0] + breaks(P, 10), breaks(P, 10))) == F[10]
    assert breaks(P, 10) in ([3, 6, 10], [3, 7, 10], [4, 7, 10])
    assert breaks(lws_dp(10, w)[1], 10) == [3, 6, 10]


def test_weights_used_are_concave():
    rng = random.Random(5)
    for _ in range(20):
        n = rng.randint(1, 12)
        assert quadrangle_holds(n, concave_weight(rng, n))


def test_matches_dynamic_program():
    rng = random.Random(1987)
    for _ in range(150):
        n = rng.randint(1, 60)
        w = concave_weight(rng, n)
        F, P = hirschberg_larmore(n, w)
        G, _ = lws_dp(n, w)
        assert F == G
        b = breaks(P, n)
        assert sum(w(i, j) for i, j in zip([0] + b, b)) == F[n]


def test_fractions_and_ties():
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(1, 30)
        c = Fraction(rng.randint(1, 5), rng.randint(1, 5))
        w = lambda i, j, c=c: c * (j - i - 2) ** 2  # many ties
        assert hirschberg_larmore(n, w)[0] == lws_dp(n, w)[0]


def test_lines_that_are_too_long():
    rng = random.Random(11)
    for _ in range(100):
        n = rng.randint(1, 50)
        w = concave_weight(rng, n, line=rng.randint(6, 30))
        F, _ = hirschberg_larmore(n, w)
        G, _ = lws_dp(n, w)
        assert F == G


def test_not_concave_can_fail():
    # w(i, j) is small only for j - i = 1 or j - i = 4: not concave, and the method is wrong
    w = lambda i, j: 0 if j - i == 4 else (1 if j - i == 1 else 10)
    assert not quadrangle_holds(8, w)
    found = False
    for n in range(1, 13):
        if hirschberg_larmore(n, w)[0] != lws_dp(n, w)[0]:
            found = True
    assert found


def test_evaluations_are_n_log_n():
    rng = random.Random(3)
    for n in (256, 1024, 4096):
        w = concave_weight(rng, n)
        st = {}
        hirschberg_larmore(n, w, st)
        assert st["evals"] <= 4 * n * math.log2(n)
