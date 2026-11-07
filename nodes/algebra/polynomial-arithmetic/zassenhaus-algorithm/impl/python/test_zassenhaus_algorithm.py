# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zassenhaus-algorithm/. The authors are listed in prov/0Y712F.jsonl.

import itertools
import random
from fractions import Fraction
from math import gcd

import pytest

import zassenhaus_algorithm as Z


# ---------------------------------------------------------------- reference helpers


def strip(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def mul(a, b):
    """Schoolbook product, the reference."""
    if not a or not b:
        return []
    c = [a[0] * 0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = c[i + j] + x * y
    return strip(c)


def product(fs):
    out = [1]
    for g in fs:
        out = mul(out, g)
    return out


def ev(f, x):
    s = 0
    for c in reversed(f):
        s = s * x + c
    return s


def key(fs):
    return sorted(tuple(g) for g in fs)


def divisors(n):
    n = abs(n)
    return [d for d in range(1, n + 1) if n % d == 0]


def rational_root_factors(f):
    """Oracle for degree <= 3: factor a primitive f with lc > 0 by the rational
    root test. A part of degree 2 or 3 without rational roots is irreducible."""
    f = list(f)
    out = []
    changed = True
    while changed and len(f) > 2:
        changed = False
        if f[0] == 0:
            out.append([0, 1])
            f = f[1:]
            changed = True
            continue
        for b in divisors(f[-1]):
            for a in divisors(f[0]):
                for sa in (a, -a):
                    if gcd(sa, b) == 1 and ev([Fraction(c) for c in f], Fraction(sa, b)) == 0:
                        q = exact_div(f, [-sa, b])
                        out.append([-sa, b])
                        f = q
                        changed = True
                        break
                if changed:
                    break
            if changed:
                break
    out.append(f)
    return out


def exact_div(f, g):
    r = [Fraction(c) for c in f]
    q = [Fraction(0)] * (len(f) - len(g) + 1)
    for k in range(len(r) - len(g), -1, -1):
        t = r[k + len(g) - 1] / g[-1]
        q[k] = t
        for j, y in enumerate(g):
            r[k + j] -= t * y
    assert not any(r)
    assert all(x.denominator == 1 for x in q)
    return [int(x) for x in q]


def is_primitive(f):
    c = 0
    for x in f:
        c = gcd(c, x)
    return c == 1


def squarefree_q(f):
    a = [Fraction(x) for x in f]
    b = strip([Fraction(i * x) for i, x in enumerate(f)][1:])
    while b:
        r = list(a)
        while len(r) >= len(b):
            t = r[-1] / b[-1]
            k = len(r) - len(b)
            for j, y in enumerate(b):
                r[k + j] -= t * y
            r = strip(r)
        a, b = b, r
    return len(a) == 1


def brute_factor_mod(f, p):
    """Oracle over F_p: trial division by all monic polynomials, by degree."""
    f = strip([x % p for x in f])
    inv = pow(f[-1], -1, p)
    f = [x * inv % p for x in f]
    out, d = [], 1
    while len(f) > 1:
        if 2 * d > len(f) - 1:
            out.append(f)
            break
        hit = False
        for tail in itertools.product(range(p), repeat=d):
            g = list(tail) + [1]
            q, r = Z._divmod_p(f, g, p)
            if not r:
                out.append(g)
                f = q
                hit = True
                break
        if not hit:
            d += 1
    return out


def irreducible_mod_some_prime(f):
    for p in (2, 3, 5, 7):
        if f[-1] % p and len(brute_factor_mod(f, p)) == 1:
            return True
    return False


# ---------------------------------------------------------------- the worked example


def test_worked_example():
    f = [-2, 0, -1, 0, 1]  # x^4 - x^2 - 2 = (x^2 - 2)(x^2 + 1)
    assert Z._choose_prime(f) == 5
    assert key(Z.factor_mod_p(f, 5)) == key([[2, 1], [3, 1], [3, 0, 1]])
    lifted = Z.hensel_lift(f, Z.factor_mod_p(f, 5), 5, 3)
    assert key(lifted) == key([[57, 1], [-57, 1], [-2, 0, 1]])
    assert (57 * 57) % 125 == 124
    assert Z.zassenhaus(f) == [[-2, 0, 1], [1, 0, 1]]


def test_page_examples():
    assert Z.zassenhaus([1, 0, 0, 0, 1]) == [[1, 0, 0, 0, 1]]
    assert Z.zassenhaus([1, 0, -10, 0, 1]) == [[1, 0, -10, 0, 1]]
    assert key(Z.zassenhaus([6, 5, 1])) == key([[2, 1], [3, 1]])


# ---------------------------------------------------------------- edge cases


def test_degree_one_and_nonmonic():
    assert Z.zassenhaus([3, 2]) == [[3, 2]]
    assert Z.zassenhaus([0, 1]) == [[0, 1]]
    assert key(Z.zassenhaus([-3, 1, 2])) == key([[-1, 1], [3, 2]])  # (x - 1)(2x + 3)
    assert key(Z.zassenhaus([0, -1, 0, 4])) == key([[0, 1], [-1, 2], [1, 2]])


@pytest.mark.parametrize("bad", [[], [5], [2, 4], [1, -2, 1], [-1, 0, -1], [0, 0, 1], [0, 0, 0]])
def test_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        Z.zassenhaus(bad)


def test_leading_zeros_are_ignored():
    assert key(Z.zassenhaus([6, 5, 1, 0, 0])) == key([[2, 1], [3, 1]])


# ---------------------------------------------------------------- exhaustive against the rational root oracle


def test_exhaustive_degree_at_most_three():
    count = 0
    for deg in (1, 2, 3):
        for lc in (1, 2, 3):
            for low in itertools.product(range(-3, 4), repeat=deg):
                f = list(low) + [lc]
                if not is_primitive(f) or not squarefree_q(f):
                    continue
                got = Z.zassenhaus(f)
                assert product(got) == f
                assert key(got) == key(rational_root_factors(f)), f
                count += 1
    assert count >= 500


# ---------------------------------------------------------------- constructed products of certified irreducibles


def random_irreducible(rng, deg):
    while True:
        g = [rng.randint(-5, 5) for _ in range(deg)] + [rng.randint(1, 3)]
        if is_primitive(g) and irreducible_mod_some_prime(g):
            return g


def test_random_products():
    rng = random.Random(20261107)
    for _ in range(60):
        fs = []
        while len(fs) < rng.randint(2, 4):
            g = random_irreducible(rng, rng.randint(1, 3))
            if g not in fs:
                fs.append(g)
        f = product(fs)
        assert key(Z.zassenhaus(f)) == key(fs)


def test_recombination_cases():
    # irreducible but split modulo every prime
    sd = [1, 0, -10, 0, 1]
    assert Z.zassenhaus(sd) == [sd]
    for g in ([1, 0, 1], [-2, 0, 1], [-3, 1, 1]):
        f = mul(sd, g)
        assert key(Z.zassenhaus(f)) == key([sd, g])
    f = mul([1, 0, 0, 0, 1], [1, 0, -10, 0, 1])
    assert key(Z.zassenhaus(f)) == key([[1, 0, 0, 0, 1], [1, 0, -10, 0, 1]])


def cyclotomic(n, cache={}):
    if n not in cache:
        f = [-1] + [0] * (n - 1) + [1]
        for d in range(1, n):
            if n % d == 0:
                f = exact_div(f, cyclotomic(d))
        cache[n] = f
    return cache[n]


@pytest.mark.parametrize("n", [1, 2, 6, 8, 12, 15, 16, 20, 24])
def test_cyclotomic(n):
    f = [-1] + [0] * (n - 1) + [1]
    want = [cyclotomic(d) for d in range(1, n + 1) if n % d == 0]
    assert key(Z.zassenhaus(f)) == key(want)


# ---------------------------------------------------------------- factoring modulo p


@pytest.mark.parametrize("p", [2, 3, 7])
def test_factor_mod_p_against_trial_division(p):
    rng = random.Random(p)
    done = 0
    while done < 60:
        n = rng.randint(1, 6)
        f = [rng.randrange(p) for _ in range(n)] + [rng.randrange(1, p)]
        g = Z._gcd_p(f, strip([i * x for i, x in enumerate(f)][1:]), p)
        if len(g) != 1:
            continue
        got = Z.factor_mod_p(f, p, seed=done)
        assert key(got) == key(brute_factor_mod(f, p))
        done += 1


def test_factor_mod_large_prime():
    p = 998244353
    rng = random.Random(5)
    for _ in range(8):
        roots = rng.sample(range(p), 5)
        f = product([[-r % p, 1] for r in roots])
        f = [x % p for x in f]
        got = Z.factor_mod_p(f, p)
        assert key(got) == key([[-r % p, 1] for r in roots])
    # x^2 - c with c a non-residue (Euler's criterion) stays irreducible
    c = 3
    assert pow(c, (p - 1) // 2, p) == p - 1
    f = mul([-c % p, 0, 1], [-1 % p, 1])
    got = Z.factor_mod_p([x % p for x in f], p)
    assert key(got) == key([[p - c, 0, 1], [p - 1, 1]])


def test_hensel_lift_invariants():
    rng = random.Random(11)
    for _ in range(20):
        fs = [random_irreducible(rng, rng.randint(1, 3)) for _ in range(3)]
        f = product(fs)
        if not squarefree_q(f) or not is_primitive(f):
            continue
        p = Z._choose_prime(f)
        us = Z.factor_mod_p(f, p)
        for k in (1, 2, 5):
            vs = Z.hensel_lift(f, us, p, k)
            m = p ** k
            assert all(v[-1] == 1 for v in vs)
            assert key([[x % p for x in v] for v in vs]) == key(us)
            diff = [a - b for a, b in zip(f, [f[-1] * x for x in product(vs)])]
            assert all(d % m == 0 for d in diff)
