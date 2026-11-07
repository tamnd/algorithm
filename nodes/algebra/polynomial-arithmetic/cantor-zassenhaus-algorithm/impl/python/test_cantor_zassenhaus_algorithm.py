# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cantor-zassenhaus-algorithm/. The authors are listed in prov/1P1SGK.jsonl.

import random

import pytest

from cantor_zassenhaus_algorithm import cantor_zassenhaus as cz, pth_root


# Independent oracle: plain mod-p list arithmetic and factorization by trial division.
# Independent oracle: plain mod-p list arithmetic and factorization by trial division.
def ref_trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def ref_mod(a, p):
    return ref_trim([x % p for x in a])


def ref_mul(a, b, p):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            out[i + j] += a[i] * b[j]
    return ref_mod(out, p)


def ref_divmod(a, b, p):
    """Long division by the nonzero b, coefficients modulo p."""
    a = ref_mod(a, p)
    inv = pow(b[-1], -1, p)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b):
        c = a[-1] * inv % p
        s = len(a) - len(b)
        q[s] = c
        a = ref_mod([a[i] - (c * b[i - s] if i >= s else 0) for i in range(len(a))], p)
    return ref_trim(q), a


def ref_product(polys, p):
    out = [1]
    for g in polys:
        out = ref_mul(out, g, p)
    return out


def monic_polys(deg, p):
    """All monic polynomials of the given degree over Z/pZ."""
    for k in range(p ** deg):
        coeffs = []
        for _ in range(deg):
            coeffs.append(k % p)
            k //= p
        yield coeffs + [1]


def brute_factor(f, p):
    """Monic irreducible factors of a monic f, with repetition, by trial division in degree order."""
    f = ref_mod(f, p)
    out = []
    d = 1
    while 2 * d <= len(f) - 1:
        for g in monic_polys(d, p):
            while True:
                q, r = ref_divmod(f, g, p)
                if r:
                    break
                out.append(g)
                f = q
            if 2 * d > len(f) - 1:
                break
        d += 1
    if len(f) > 1:
        out.append(f)
    return sorted(out, key=lambda g: (len(g), g))


def is_square_free_brute(f, p):
    fs = brute_factor(f, p)
    return len(set(map(tuple, fs))) == len(fs)


def random_monic(rng, deg, p):
    return [rng.randrange(p) for _ in range(deg)] + [1]


def nonresidues(p, count, start=2):
    """The first count quadratic non-residues modulo the odd prime p, by Euler's criterion."""
    out, c = [], start
    while len(out) < count:
        if pow(c, (p - 1) // 2, p) == p - 1:
            out.append(c)
        c += 1
    return out


def big_prime_irreducibles(p):
    """Distinct monic irreducibles over Z/pZ for p = 998244353 (p = 1 mod 8): x - a and x^(2^j) - c, c a non-residue."""
    c = nonresidues(p, 4)
    return [[p - 5, 1], [p - 12345, 1], [p - c[0], 0, 1], [p - c[1], 0, 1], [p - c[2], 0, 0, 0, 1], [p - c[3]] + [0] * 7 + [1]]


def expand(c, factors, p):
    out = [c % p]
    for q, e in factors:
        for _ in range(e):
            out = ref_mul(out, q, p)
    return out


def grouped(qs):
    out = {}
    for q in qs:
        out[tuple(q)] = out.get(tuple(q), 0) + 1
    return sorted(((list(q), e) for q, e in out.items()), key=lambda t: (len(t[0]), t[0]))


def check(f, p, rng=None):
    c, fac = cz(f, p, rng=rng)
    g = ref_mod(f, p)
    assert expand(c, fac, p) == g
    assert c == g[-1]
    return c, fac


def test_worked_example():
    p = 3
    f = [0, 1, 2, 2, 2, 0, 1, 1, 1, 2]  # 2 x (x + 2) (x + 1)^3 (x^2 + 1)^2
    st = {}
    c, fac = cz(f, p, stats=st)
    assert c == 2
    assert fac == [([0, 1], 1), ([1, 1], 3), ([2, 1], 1), ([1, 0, 1], 2)]
    assert st["square_free"] == [([0, 2, 1], 1), ([1, 0, 1], 2), ([1, 1], 3)]
    assert st["degree_parts"] == [([0, 2, 1], 1), ([1, 0, 1], 2), ([1, 1], 1)]


@pytest.mark.parametrize("p,maxdeg,count", [(2, 9, 120), (3, 8, 120), (7, 6, 80)])
def test_random_against_trial_division(p, maxdeg, count):
    rng = random.Random(1000 + p)
    for t in range(count):
        n = rng.randint(1, maxdeg)
        f = [rng.randrange(p) for _ in range(n)] + [rng.randrange(1, p)]
        c, fac = check(f, p, random.Random(t))
        assert fac == grouped(brute_factor(ref_mod([x * pow(c, -1, p) for x in f], p), p))


@pytest.mark.parametrize("p", [2, 3, 7])
def test_products_with_multiplicities(p):
    rng = random.Random(77 + p)
    for t in range(40):
        qs = []
        for _ in range(rng.randint(1, 4)):
            d = rng.randint(1, 3)
            irr = [g for g in monic_polys(d, p) if brute_factor(g, p) == [g]]
            q = rng.choice(irr)
            qs.extend([q] * rng.choice([1, 1, 2, p, p + 1, 2 * p]))
        c = rng.randrange(1, p)
        f = ref_product(qs, p)
        f = ref_mod([c * x for x in f], p)
        got_c, fac = cz(f, p, rng=random.Random(t))
        assert got_c == c
        assert fac == grouped(qs)


def test_large_prime():
    p = 998244353
    irr = big_prime_irreducibles(p)
    rng = random.Random(5)
    for t in range(6):
        qs = []
        for q in rng.sample(irr, rng.randint(2, 4)):
            qs.extend([q] * rng.randint(1, 2))
        f = ref_mod([3 * x for x in ref_product(qs, p)], p)
        c, fac = cz(f, p, rng=random.Random(t))
        assert c == 3
        assert fac == grouped(qs)
    # integer input with negative and large coefficients: x^2 - 1 = (x - 1)(x + 1)
    assert cz([-1, 0, 1 + p], p) == (1, [([1, 1], 1), ([p - 1, 1], 1)])


def test_pth_powers():
    for p in (2, 3, 7):
        # x^p - x factors into all linear factors
        f = [0, p - 1] + [0] * (p - 2) + [1]
        assert cz(f, p)[1] == [([a, 1], 1) for a in range(p)]
        # (x^2 + x + 1)^(p^2) has zero derivative twice over
        g = [1, 1, 1]
        h = [1]
        for _ in range(p * p):
            h = ref_mul(h, g, p)
        expected = grouped(brute_factor(g, p) * (p * p))
        assert cz(h, p)[1] == expected
    assert pth_root([1, 0, 0, 2, 0, 0, 1], 3) == [1, 2, 1]
    with pytest.raises(ValueError):
        pth_root([1, 1], 3)


def test_edge_cases():
    for p in (2, 3, 7, 998244353):
        with pytest.raises(ValueError):
            cz([], p)
        with pytest.raises(ValueError):
            cz([0, 0, 0], p)
        with pytest.raises(ValueError):
            cz([p, 2 * p], p)  # reduces to the zero polynomial
        assert cz([1], p) == (1, [])
        assert cz([1, 0, 0], p) == (1, [])  # leading zeros are stripped
        assert cz([-1 % p, 1], p) == (1, [([p - 1, 1], 1)])
        assert cz([0, 1, 0], p) == (1, [([0, 1], 1)])
    assert cz([5], 7) == (5, [])
    assert cz([4, 2], 7) == (2, [([2, 1], 1)])  # non-monic linear: 2 (x + 2)
    assert cz([1, 0, 1], 3) == (1, [([1, 0, 1], 1)])  # irreducible
    assert cz([1, 0, 1], 2) == (1, [([1, 1], 2)])  # (x + 1)^2 over F_2
    assert cz([0, 0, 0, 0, 1], 5) == (1, [([0, 1], 4)])
