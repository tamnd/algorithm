# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-irreducibility-test/. The authors are listed in prov/6CAYMS.jsonl.

import itertools
import random

import pytest

from rabin_irreducibility_test import is_irreducible


def strip(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def mul(a, b, p):
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = (c[i + j] + x * y) % p
    return strip(c)


def divides(g, f, p):
    """Trial division with a monic g."""
    r = list(f)
    n = len(g) - 1
    for k in range(len(r) - 1, n - 1, -1):
        t = r[k]
        for j in range(n + 1):
            r[k - n + j] = (r[k - n + j] - t * g[j]) % p
    return not any(r[:n])


def brute_irreducible(f, p):
    """Independent oracle: no monic factor of degree 1 .. n/2."""
    f = strip([c % p for c in f])
    n = len(f) - 1
    if n < 1:
        return False
    for d in range(1, n // 2 + 1):
        for low in itertools.product(range(p), repeat=d):
            if divides(list(low) + [1], f, p):
                return False
    return True


def mobius(n):
    m, d, r = n, 2, 1
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            r = -r
        d += 1
    return -r if m > 1 else r


def gauss_count(p, n):
    return sum(mobius(d) * p ** (n // d) for d in range(1, n + 1) if n % d == 0) // n


def test_worked_examples():
    assert is_irreducible([1, 1, 0, 0, 1], 2)          # x^4 + x + 1
    assert is_irreducible([1, 1, 1, 1, 1], 2)          # x^4 + x^3 + x^2 + x + 1
    assert not is_irreducible([1, 0, 1, 0, 1], 2)      # (x^2 + x + 1)^2
    assert not is_irreducible([1, 0, 0, 0, 1], 3)      # (x^2 + x + 2)(x^2 + 2x + 2)
    assert is_irreducible([1, 0, 1], 3)
    assert not is_irreducible([1, 0, 1], 2)


def test_edge_cases():
    assert not is_irreducible([], 7)
    assert not is_irreducible([5], 7)
    assert not is_irreducible([0, 0, 7], 7)            # the zero polynomial modulo 7
    assert is_irreducible([3, 5], 7)                   # degree 1
    assert is_irreducible([3, 5, 0, 0], 7)             # leading zeros
    assert is_irreducible([1, 1, 1], 2)                # non-monic is made monic below
    assert is_irreducible([3, 3, 3], 7) == is_irreducible([1, 1, 1], 7)
    assert not is_irreducible([0, 0, 1], 998244353)    # x^2
    assert not is_irreducible([0, 1, 1, 0, 0, 0, 1], 2)  # divisible by x


@pytest.mark.parametrize("p,maxdeg", [(2, 8), (3, 5), (7, 3)])
def test_exhaustive_counts_match_gauss_formula(p, maxdeg):
    for n in range(1, maxdeg + 1):
        count = sum(is_irreducible(list(low) + [1], p)
                    for low in itertools.product(range(p), repeat=n))
        assert count == gauss_count(p, n)


@pytest.mark.parametrize("p,maxdeg", [(2, 10), (3, 7), (7, 5)])
def test_random_against_trial_division(p, maxdeg):
    rng = random.Random(p * 31)
    for _ in range(200):
        n = rng.randint(1, maxdeg)
        f = [rng.randrange(p) for _ in range(n)] + [rng.randrange(1, p)]
        assert is_irreducible(f, p) == brute_irreducible(f, p)


P = 998244353


def order(a):
    e = P - 1
    for r in (2, 7, 17):
        while e % r == 0 and pow(a, e // r, P) == 1:
            e //= r
    return e


def binomial_irreducible(n, a):
    """x^n - a over F_P, by the theorem on irreducible binomials."""
    e = order(a)
    for r in (2, 3, 5, 7, 11, 13, 17):
        if n % r == 0 and (e % r != 0 or ((P - 1) // e) % r == 0):
            return False
    return not (n % 4 == 0 and (P - 1) % 4 != 0)


def test_large_prime():
    rng = random.Random(5)
    for _ in range(60):
        n = rng.choice([2, 4, 7, 8, 14, 16, 17])
        a = rng.randrange(1, P)
        f = [(-a) % P] + [0] * (n - 1) + [1]
        assert is_irreducible(f, P) == binomial_irreducible(n, a)
    for _ in range(100):
        b, c = rng.randrange(P), rng.randrange(P)
        disc = (b * b - 4 * c) % P
        euler = disc != 0 and pow(disc, (P - 1) // 2, P) == P - 1
        assert is_irreducible([c, b, 1], P) == euler
    for _ in range(40):
        g = [rng.randrange(P) for _ in range(rng.randint(1, 4))] + [1]
        h = [rng.randrange(P) for _ in range(rng.randint(1, 4))] + [1]
        assert not is_irreducible(mul(g, h, P), P)
