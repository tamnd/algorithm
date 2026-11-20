# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coded-aperture-imaging/. The authors are listed in prov/RBP3GB.jsonl.

import random
from fractions import Fraction

from coded_aperture_imaging import (
    adjoint_encode,
    decode,
    decode_scaled,
    decoding_array,
    encode,
    is_prime,
    legendre,
    periodic_correlation,
    quadratic_residue_ura,
    twin_prime_ura,
)


def shape(a):
    return len(a), len(a[0])


def delta_plus_constant(peak, side, n1, n2):
    return [[peak if (d1, d2) == (0, 0) else side for d2 in range(n2)] for d1 in range(n1)]


def all_uras():
    out = [quadratic_residue_ura(p) for p in (3, 7, 11, 19, 23, 31, 43)]
    out += [twin_prime_ura(r) for r in (3, 5, 11)]
    return out


def test_legendre_matches_squares():
    for p in range(3, 60):
        if not is_prime(p):
            continue
        squares = {(x * x) % p for x in range(1, p)}
        for a in range(p):
            want = 0 if a == 0 else (1 if a in squares else -1)
            assert legendre(a, p) == want


def test_quadratic_residue_sets():
    assert quadratic_residue_ura(7) == [[0, 1, 1, 0, 1, 0, 0]]
    assert [j for j, x in enumerate(quadratic_residue_ura(11)[0]) if x] == [1, 3, 4, 5, 9]


def test_autocorrelation_is_delta_plus_constant():
    # A corr A = (k - lam) delta + lam, exact integers, with 2 lam = k - 1.
    for a in all_uras():
        n1, n2 = shape(a)
        v = n1 * n2
        k = sum(map(sum, a))
        assert 2 * k == v - 1
        lam = (k - 1) // 2
        assert periodic_correlation(a, a) == delta_plus_constant(k, lam, n1, n2)


def test_balanced_correlation_is_delta():
    # A corr G = (k + 1) delta - 1 for G = 2A - 1: the peak is k, the sidelobes are -1.
    for a in all_uras():
        n1, n2 = shape(a)
        k = sum(map(sum, a))
        g = decoding_array(a)
        assert periodic_correlation(a, g) == delta_plus_constant(k, -1, n1, n2)


def test_twin_prime_parameters():
    a = twin_prime_ura(5)
    assert shape(a) == (5, 7)
    assert sum(map(sum, a)) == 17
    side = {x for row in periodic_correlation(a, a) for x in row[1:]}
    assert side == {8}


def test_exact_decoding_of_integer_objects():
    rng = random.Random(20261120)
    for a in all_uras():
        n1, n2 = shape(a)
        k = sum(map(sum, a))
        for _ in range(3):
            o = [[rng.randint(0, 50) for _ in range(n2)] for _ in range(n1)]
            p = encode(o, a)
            assert sum(map(sum, p)) == k * sum(map(sum, o))
            assert decode_scaled(p, a) == [[k * (k + 1) * x for x in row] for row in o]
            assert decode(p, a) == [[Fraction(x) for x in row] for row in o]


def test_point_source():
    a = quadratic_residue_ura(11)
    o = [[0] * 11]
    o[0][4] = 7
    p = encode(o, a)
    # the shadow is the mask shifted by 4 and scaled by 7
    assert p == [[7 * a[0][(j - 4) % 11] for j in range(11)]]
    assert decode(p, a) == [[Fraction(x) for x in o[0]]]


def test_adjoint():
    rng = random.Random(7)
    for a in (quadratic_residue_ura(19), twin_prime_ura(3)):
        n1, n2 = shape(a)
        o = [[rng.randint(-9, 9) for _ in range(n2)] for _ in range(n1)]
        q = [[rng.randint(-9, 9) for _ in range(n2)] for _ in range(n1)]
        lhs = sum(x * y for r1, r2 in zip(encode(o, a), q) for x, y in zip(r1, r2))
        rhs = sum(x * y for r1, r2 in zip(o, adjoint_encode(q, a)) for x, y in zip(r1, r2))
        assert lhs == rhs


def test_random_mask_is_not_a_ura():
    rng = random.Random(3)
    a = [[rng.randint(0, 1) for _ in range(11)]]
    while sum(a[0]) != 5:
        a = [[rng.randint(0, 1) for _ in range(11)]]
    side = {x for x in periodic_correlation(a, a)[0][1:]}
    assert len(side) > 1
    o = [[rng.randint(0, 50) for _ in range(11)]]
    assert decode(encode(o, a), a) != [[Fraction(x) for x in o[0]]]


def test_bad_sizes_raise():
    for bad in (13, 9, 2):
        try:
            quadratic_residue_ura(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(bad)
    try:
        twin_prime_ura(7)
    except ValueError:
        pass
    else:
        raise AssertionError(7)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("ok")
