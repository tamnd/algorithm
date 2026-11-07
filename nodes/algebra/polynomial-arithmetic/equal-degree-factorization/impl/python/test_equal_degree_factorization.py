# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equal-degree-factorization/. The authors are listed in prov/H77D0W.jsonl.

import random

import pytest

from equal_degree_factorization import equal_degree_factorization as edf, gcd_p, powmod, sub


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


def irreducibles(d, p):
    """All monic irreducibles of degree d over Z/pZ, by trial division (small p and d only)."""
    return [g for g in monic_polys(d, p) if brute_factor(g, p) == [g]]


def test_worked_example():
    p = 7
    f = ref_product([[1, 0, 1], [4, 0, 1], [3, 1, 1]], p)
    assert f == [5, 4, 5, 5, 1, 1, 1]
    # a = x^2 is a square modulo every factor, so b = 1 and nothing splits
    assert powmod([0, 0, 1], 24, f, p) == [1]
    # a = x gives b = 1, 1, -1 modulo the three factors
    b = powmod([0, 1], 24, f, p)
    assert b == [4, 0, 2, 0, 6]
    assert gcd_p(sub(b, [1], p), f, p) == [4, 0, 5, 0, 1]
    h = [4, 0, 5, 0, 1]
    b = powmod([1, 1], 24, h, p)
    assert b == [4, 0, 3]
    assert gcd_p(sub(b, [1], p), h, p) == [1, 0, 1]
    assert edf(f, 2, p) == [[1, 0, 1], [3, 1, 1], [4, 0, 1]]


@pytest.mark.parametrize("p,d", [(2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (7, 1), (7, 2)])
def test_random_products_of_irreducibles(p, d):
    irr = irreducibles(d, p)
    rng = random.Random(100 * p + d)
    for trial in range(15):
        k = rng.randint(1, min(len(irr), 6))
        pick = rng.sample(irr, k)
        f = ref_product(pick, p)
        stats = {}
        got = edf(f, d, p, random.Random(trial), stats)
        assert got == sorted(pick, key=lambda g: (len(g), g))
        assert stats["attempts"] <= 12 * k + 10


def test_large_prime():
    p = 998244353
    c = nonresidues(p, 8)
    cases = [
        ([[p - a, 1] for a in (1, 2, 3, 10 ** 6, 123456789)], 1),
        ([[p - x, 0, 1] for x in c[:4]], 2),
        ([[p - x, 0, 0, 0, 1] for x in c[4:7]], 4),
    ]
    for pick, d in cases:
        f = ref_product(pick, p)
        assert edf(f, d, p, random.Random(d)) == sorted(pick, key=lambda g: (len(g), g))


def test_success_rate_is_about_one_half():
    # with two factors, one attempt succeeds with probability about 1/2
    p, d = 3, 2
    irr = irreducibles(d, p)
    f = ref_product(irr[:2], p)
    total = 0
    for seed in range(200):
        stats = {}
        edf(f, d, p, random.Random(seed), stats)
        total += stats["attempts"]
    assert 1.4 < total / 200 < 2.8


def test_edge_cases():
    assert edf([1], 3, 5) == []
    assert edf([1, 1, 1], 2, 2) == [[1, 1, 1]]
    assert edf([3, 0, 1, 0, 0], 2, 7) == [[3, 0, 1]]
    # unreduced coefficients are reduced first
    assert edf([-1, 0, 1], 1, 5) == [[1, 1], [4, 1]]
    with pytest.raises(ValueError):
        edf([1, 0, 1, 1], 2, 2)  # degree 3 is not a multiple of 2
    with pytest.raises(ValueError):
        edf([1, 2], 1, 5)  # not monic
    with pytest.raises(ValueError):
        edf([1, 1], 0, 5)
