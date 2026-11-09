# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alt-godau-algorithm/. The authors are listed in prov/BQ9SVX.jsonl.

import math
import random
from fractions import Fraction

from alt_godau_algorithm import compare, critical_values, frechet_decide, frechet_distance2, sign_two_roots


def discrete_dp(A, B):
    """Discrete Frechet distance (Eiter and Mannila), iterative O(|A| |B|) dynamic program, floats."""
    n, m = len(A), len(B)
    D = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            d = math.dist(A[i], B[j])
            if i == 0 and j == 0:
                D[i][j] = d
            elif i == 0:
                D[i][j] = max(D[i][j - 1], d)
            elif j == 0:
                D[i][j] = max(D[i - 1][j], d)
            else:
                D[i][j] = max(min(D[i - 1][j], D[i][j - 1], D[i - 1][j - 1]), d)
    return D[n - 1][m - 1]


def discrete_brute(A, B):
    """Discrete Frechet distance straight from the definition: minimum over all couplings, by recursion."""

    def go(i, j):
        d = math.dist(A[i], B[j])
        if i == len(A) - 1 and j == len(B) - 1:
            return d
        options = []
        if i + 1 < len(A):
            options.append(go(i + 1, j))
        if j + 1 < len(B):
            options.append(go(i, j + 1))
        if i + 1 < len(A) and j + 1 < len(B):
            options.append(go(i + 1, j + 1))
        return max(d, min(options))

    return go(0, 0)


def refine(C, k):
    out = [C[0]]
    for a, b in zip(C, C[1:]):
        for t in range(1, k + 1):
            out.append((a[0] + (b[0] - a[0]) * t / k, a[1] + (b[1] - a[1]) * t / k))
    return out


def max_seg(C):
    return max((math.dist(a, b) for a, b in zip(C, C[1:])), default=0.0)


def rand_curve(rng, R, lo=1, hi=5):
    return [(rng.randint(-R, R), rng.randint(-R, R)) for _ in range(rng.randint(lo, hi))]


def test_discrete_dp_matches_brute_recursion():
    rng = random.Random(1)
    for _ in range(600):
        A, B = rand_curve(rng, 6, 1, 6), rand_curve(rng, 6, 1, 6)
        assert discrete_dp(A, B) == discrete_brute(A, B)


def test_exact_sign_against_high_precision():
    rng = random.Random(2)
    from decimal import Decimal, getcontext

    getcontext().prec = 80
    for _ in range(2000):
        a, b, c = (Fraction(rng.randint(-30, 30), rng.randint(1, 5)) for _ in range(3))
        x, y = Fraction(rng.randint(0, 40), rng.randint(1, 4)), Fraction(rng.randint(0, 40), rng.randint(1, 4))
        if rng.random() < 0.3:  # force exact cancellations such as 2 sqrt(2) - sqrt(8)
            y = x * 4
            c = -b / 2
            a = Fraction(0)
        dec = lambda f: Decimal(f.numerator) / Decimal(f.denominator)
        v = dec(a) + dec(b) * dec(x).sqrt() + dec(c) * dec(y).sqrt()
        want = 0 if abs(v) < Decimal(10) ** -60 else (1 if v > 0 else -1)
        assert sign_two_roots(a, b, x, c, y) == want


def test_against_refined_discrete_frechet():
    rng = random.Random(3)
    for _ in range(500):
        P, Q = rand_curve(rng, 8), rand_curve(rng, 8)
        d = math.sqrt(frechet_distance2(P, Q))
        assert d >= math.dist(P[0], Q[0]) - 1e-9 and d >= math.dist(P[-1], Q[-1]) - 1e-9
        k = 6
        dd = discrete_dp(refine(P, k), refine(Q, k))
        # d_F <= discrete distance of any sampling, and the gap is at most the longest sampled piece
        assert d <= dd + 1e-9
        assert dd <= d + max(max_seg(P), max_seg(Q)) / k + 1e-9


def test_decision_is_consistent_with_the_value():
    rng = random.Random(4)
    for _ in range(300):
        P, Q = rand_curve(rng, 6, 2, 5), rand_curve(rng, 6, 2, 5)
        d2 = frechet_distance2(P, Q)
        assert frechet_decide(P, Q, d2)
        for c in critical_values(P, Q):
            assert frechet_decide(P, Q, c) == (c >= d2)
        if d2 > 0:
            assert not frechet_decide(P, Q, d2 - Fraction(1, 10**9))


def test_invariances_exact():
    rng = random.Random(5)
    for _ in range(300):
        P, Q = rand_curve(rng, 7, 2, 5), rand_curve(rng, 7, 2, 5)
        d2 = frechet_distance2(P, Q)
        assert frechet_distance2(Q, P) == d2
        assert frechet_distance2(P[::-1], Q[::-1]) == d2
        assert frechet_distance2(P, P) == 0
        i = rng.randrange(len(P) - 1)  # insert a point inside a segment: the curve is the same
        t = Fraction(rng.randint(1, 4), 5)
        mid = (P[i][0] + t * (P[i + 1][0] - P[i][0]), P[i][1] + t * (P[i + 1][1] - P[i][1]))
        assert frechet_distance2(P[: i + 1] + [mid] + P[i + 1 :], Q) == d2
        shift = (rng.randint(-5, 5), rng.randint(-5, 5))  # translate both curves
        move = lambda C: [(x + shift[0], y + shift[1]) for x, y in C]
        assert frechet_distance2(move(P), move(Q)) == d2


def test_small_cases():
    assert frechet_distance2([(0, 0), (4, 0)], [(0, 0), (4, 0), (0, 0), (4, 0)]) == 4  # back and forth: d_F = 2
    assert frechet_distance2([(0, 0), (2, 0), (4, 0)], [(0, 0), (4, 0)]) == 0
    assert frechet_distance2([(0, 0), (1, 1), (2, 0)], [(0, 0), (2, 0)]) == 1
    assert frechet_distance2([(0, 0)], [(0, 0), (5, 0), (1, 0)]) == 25
    assert frechet_distance2([(3, 4)], [(0, 0)]) == 25
    assert frechet_distance2([(0, 0), (0, 0), (3, 0)], [(0, 1), (3, 1), (3, 1)]) == 1  # repeated vertices
    # two parallel unit-spaced segments in opposite directions
    assert frechet_distance2([(0, 0), (6, 0)], [(6, 1), (0, 1)]) == 37
    # the float trap: these squared distances differ by 1 but their roots round to the same double
    a, b, c = (0, 0), (10**8, 1), (-(10**8), 0)
    assert frechet_distance2([a], [b]) == 10**16 + 1 and frechet_distance2([a], [c]) == 10**16
    assert compare((Fraction(0), Fraction(1), Fraction(8)), (Fraction(0), Fraction(2), Fraction(2))) == 0
