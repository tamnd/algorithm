# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/well-rng/. The authors are listed in prov/RZPYG3.jsonl.

from math import gcd

import pytest

from well_rng import Well512a, well512a_next

# Prime factors of 2^512 - 1 = F0 F1 ... F8 (Fermat numbers 2^(2^i) + 1).
F8_SMALL = 1238926361552897
F8_BIG = 93461639715357977769163558199606896584051237541638188580280321
FACTORS_512 = [3, 5, 17, 257, 65537, 641, 6700417, 274177, 67280421310721,
               59649589127497217, 5704689200685129054721, F8_SMALL, F8_BIG]


def test_reference_outputs() -> None:
    # WELL512a.c of Panneton, L'Ecuyer and Matsumoto, compiled and run with init[j] = j + 1.
    g = Well512a([j + 1 for j in range(16)])
    assert [g.next_u32() for _ in range(5)] == [2692481146, 2447117626, 752362814, 4237304894, 3767796794]
    g = Well512a([j + 1 for j in range(16)])
    assert g.next_double() == 0.62689211824908853


def test_zero_state_and_linearity() -> None:
    s, i = [0] * 16, 0
    assert well512a_next(s, i) == (0, 15) and s == [0] * 16
    a = [(j * 2654435761) & 0xFFFFFFFF for j in range(16)]
    b = [(j * 40503 + 7) & 0xFFFFFFFF for j in range(16)]
    c = [x ^ y for x, y in zip(a, b)]
    ia = ib = ic = 0
    for _ in range(50):
        oa, ia = well512a_next(a, ia)
        ob, ib = well512a_next(b, ib)
        oc, ic = well512a_next(c, ic)
        assert oc == oa ^ ob


def _is_prime_small(n: int) -> bool:
    """Miller-Rabin with the first 13 prime bases: exact for n < 3.3 * 10^24."""
    assert n < 3 * 10**24
    if n < 2:
        return False
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for p in bases:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _pocklington(n: int, factors: dict[int, int]) -> bool:
    """n is prime if F = prod q^e divides n - 1, F^2 > n, and each q has a witness base."""
    f = 1
    for q, e in factors.items():
        f *= q**e
    assert (n - 1) % f == 0 and f * f > n
    for q in factors:
        for a in range(2, 200):
            if pow(a, n - 1, n) != 1:
                return False
            if gcd(pow(a, (n - 1) // q, n) - 1, n) == 1:
                break
        else:
            return False
    return True


def test_factorization_of_2_to_512_minus_1() -> None:
    prod = 1
    for f in FACTORS_512:
        prod *= f
    assert prod == 2**512 - 1
    for f in FACTORS_512[:-1]:
        assert _is_prime_small(f)
    # The 43-digit prime factor of F8_BIG - 1, proved by Pocklington with a full factorization.
    q43 = 1057372046781162536274034354686893329625329
    small = {2: 4, 3: 1, 8861: 1, 10608557: 1, 25353082741699: 1, 9243081088796207: 1}
    assert all(_is_prime_small(p) for p in small)
    assert _pocklington(q43, small)
    # F8_BIG - 1 = 2^11 3 5 7 13 31618624099079 q43, and this part already exceeds its square root.
    part = {2: 11, 3: 1, 5: 1, 7: 1, 13: 1, 31618624099079: 1, q43: 1}
    assert _is_prime_small(31618624099079)
    assert _pocklington(F8_BIG, part)


# Polynomials over GF(2) as ints: bit k is the coefficient of x^k.

def _reduce(a: int, p: int, deg: int) -> int:
    while a.bit_length() > deg:
        a ^= p << (a.bit_length() - 1 - deg)
    return a


_SPREAD = [int(bin(b)[2:], 4) for b in range(256)]  # interleave zeros: the square of a byte


def _square(a: int, p: int, deg: int) -> int:
    r, k = 0, 0
    while a:
        r |= _SPREAD[a & 0xFF] << k
        a >>= 8
        k += 16
    return _reduce(r, p, deg)


def _x_power(e: int, p: int) -> int:
    """x^e mod p, left to right: squarings and multiplications by x."""
    deg = p.bit_length() - 1
    r = 1
    for bit in bin(e)[2:]:
        r = _square(r, p, deg)
        if bit == "1":
            r = _reduce(r << 1, p, deg)
    return r


def _berlekamp_massey(bits: list[int]) -> tuple[int, int]:
    c, b, ell, m = 1, 1, 0, 1
    for n, bit in enumerate(bits):
        d = bit
        for i in range(1, ell + 1):
            d ^= ((c >> i) & 1) & bits[n - i]
        if d == 0:
            m += 1
            continue
        t = c
        c ^= b << m
        if 2 * ell <= n:
            ell, b, m = n + 1 - ell, t, 1
        else:
            m += 1
    return c, ell


def _charpoly_from_output() -> int:
    g = Well512a([j + 1 for j in range(16)])
    bits = [g.next_u32() & 1 for _ in range(1024)]
    c, ell = _berlekamp_massey(bits)
    assert ell == 512
    return sum(1 << (ell - i) for i in range(ell + 1) if (c >> i) & 1)  # reverse the connection polynomial


def test_characteristic_polynomial_is_primitive() -> None:
    p = _charpoly_from_output()
    n = 2**512 - 1
    assert _x_power(n, p) == 1
    for q in FACTORS_512:
        assert _x_power(n // q, p) != 1
    assert bin(p).count("1") == 225  # N1, the number of non-zero coefficients


def test_small_primitivity_check_agrees_with_brute_force() -> None:
    # Degree 6 over GF(2): 2^6 - 1 = 3^2 * 7. Brute force the order of x.
    for p in range(1 << 6, 1 << 7):
        if not p & 1:
            continue
        r, k = _reduce(2, p, 6), 1
        while r != 1 and k < 64:
            r, k = _reduce(r << 1, p, 6), k + 1
        brute = k == 63
        check = _x_power(63, p) == 1 and all(_x_power(63 // q, p) != 1 for q in (3, 7))
        assert brute == check


def _rank(vectors: list[int]) -> int:
    basis: dict[int, int] = {}
    for v in vectors:
        while v:
            h = v.bit_length() - 1
            if h not in basis:
                basis[h] = v
                break
            v ^= basis[h]
    return len(basis)


def test_maximally_equidistributed() -> None:
    # For every l = 1..32, the top l bits of floor(512/l) consecutive outputs are a surjective
    # linear function of the 512-bit state: the dimension defects are all 0.
    outs = []
    for j in range(512):
        s = [0] * 16
        s[j // 32] = 1 << (j % 32)
        i, row = 0, []
        for _ in range(512):
            o, i = well512a_next(s, i)
            row.append(o)
        outs.append(row)
    for ell in range(1, 33):
        k = 512 // ell
        vecs = []
        for row in outs:
            v = 0
            for o in row[:k]:
                v = (v << ell) | (o >> (32 - ell))
            vecs.append(v)
        assert _rank(vecs) == ell * k


def test_escape_from_almost_zero_state() -> None:
    s, i = [0] * 16, 0
    s[0] = 1
    for _ in range(200):
        _, i = well512a_next(s, i)
    ones = sum(bin(w).count("1") for w in s)
    assert 0.4 < ones / 512 < 0.6


def test_bad_seed_rejected() -> None:
    with pytest.raises(ValueError):
        Well512a([0] * 16)
    with pytest.raises(ValueError):
        Well512a([1] * 15)
