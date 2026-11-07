# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heuristic-gcd/. The authors are listed in prov/N1KXF6.jsonl.

import random
from fractions import Fraction
from math import gcd, lcm

from heuristic_gcd import (
    content,
    divides,
    evaluate,
    genpoly,
    heuristic_gcd,
    heuristic_gcd_trace,
    primitive_part,
    trim,
)


def mul(a, b):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def oracle_gcd(f, g):
    """gcd in Z[x] from the Euclidean algorithm over Q, then made primitive."""
    f, g = trim(f), trim(g)
    if not f or not g:
        h = f or g
        return [-a for a in h] if h and h[-1] < 0 else h
    a = [Fraction(x) for x in f]
    b = [Fraction(x) for x in g]
    while b:
        r = list(a)
        while len(r) >= len(b) and r:
            q = r[-1] / b[-1]
            s = len(r) - len(b)
            for i, y in enumerate(b):
                r[s + i] -= q * y
            while r and r[-1] == 0:
                r.pop()
        a, b = b, r
    den = 1
    for x in a:
        den = lcm(den, x.denominator)
    h = primitive_part([int(x * den) for x in a])
    c = gcd(content(f), content(g))
    return [c * x for x in h]


def rand_poly(rng, deg, size):
    p = [rng.randint(-size, size) for _ in range(deg + 1)]
    if p[-1] == 0:
        p[-1] = rng.choice([-1, 1]) * rng.randint(1, size)
    return p


def test_worked_example():
    f, g = [0, 2, 1], [-4, 0, 1]  # x^2 + 2x and x^2 - 4
    tr = heuristic_gcd_trace(f, g)
    assert tr == [(6, 16, [-2, 3], False), (16, 36, [2, 1], True)]
    assert heuristic_gcd(f, g) == [2, 1]


def test_coprime_example():
    tr = heuristic_gcd_trace([1, -1, 1], [1, 3])
    assert tr == [(4, 13, [1, -1, 1], False), (10, 1, [1], True)]
    assert heuristic_gcd([1, -1, 1], [1, 3]) == [1]


def test_genpoly_inverts_evaluation():
    rng = random.Random(11)
    for _ in range(500):
        xi = rng.randint(2, 50)
        h = [rng.randint(-((xi - 1) // 2), xi // 2) for _ in range(rng.randint(1, 6))]
        h = trim(h)
        assert genpoly(evaluate(h, xi), xi) == h


def test_random_against_euclid():
    rng = random.Random(2024)
    answered = 0
    for _ in range(600):
        h = rand_poly(rng, rng.randint(0, 3), 6)
        a = rand_poly(rng, rng.randint(0, 3), 6)
        b = rand_poly(rng, rng.randint(0, 3), 6)
        f, g = mul(h, a), mul(h, b)
        want = oracle_gcd(f, g)
        got = heuristic_gcd(f, g)
        if got is not None:
            answered += 1
            assert got == want
            assert divides(primitive_part(got), primitive_part(f))
    assert answered >= 590


def test_large_coefficients():
    rng = random.Random(7)
    for _ in range(100):
        h = rand_poly(rng, 4, 10 ** 6)
        f = mul(h, rand_poly(rng, 3, 10 ** 6))
        g = mul(h, rand_poly(rng, 5, 10 ** 6))
        got = heuristic_gcd(f, g)
        assert got is None or got == oracle_gcd(f, g)


def test_edge_cases():
    assert heuristic_gcd([], []) == []
    assert heuristic_gcd([], [0, -2]) == [0, 2]
    assert heuristic_gcd([3, 6], []) == [3, 6]
    assert heuristic_gcd([6], [4]) == [2]
    assert heuristic_gcd([6], [1, 1]) == [1]
    assert heuristic_gcd([-2, 0, -2], [0, 0, 4]) == [2]
    f = [-1, 0, 0, 0, 0, 0, 1]  # x^6 - 1
    assert heuristic_gcd(f, f) == f
    assert heuristic_gcd([1, -1, 0, 0, 1], [-1, 1, 0, 0, -1]) == [1, -1, 0, 0, 1]
    assert heuristic_gcd(mul([1, 1], [2, 3]), mul([1, 1], [5, -7])) == [1, 1]
