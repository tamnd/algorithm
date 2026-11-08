# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiply-with-carry/. The authors are listed in prov/D46KH3.jsonl.

from itertools import product
from math import gcd

from multiply_with_carry import (
    A64,
    B32,
    from_lcg,
    kiss99_mwc_pair,
    mwc64_next,
    mwc_jump,
    mwc_lag_next,
    mwc_next,
    mwc_stream,
    to_lcg,
)


def _is_prime(n: int) -> bool:
    # Miller-Rabin with the first 13 prime bases: exact for n < 3.3 * 10^24.
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


def _order(g: int, m: int) -> int:
    k, v = 1, g % m
    while v != 1:
        v, k = v * g % m, k + 1
    return k


def test_reference_values_64() -> None:
    # A direct C implementation with uint64_t: t = a*x + c; x = (uint32_t)t; c = t >> 32.
    assert mwc_stream(5, 123456789, 362436, A64, B32) == [
        693968569, 3776248345, 1429218845, 44760066, 4136716891
    ]
    s = (362436 << 32) | 123456789
    s = mwc64_next(s)
    assert s == (123456512 << 32) | 693968569


def test_reference_values_kiss99() -> None:
    # Marsaglia's 1999 KISS components from z = 362436069, w = 521288629, run in C.
    z, w = 362436069, 521288629
    got = []
    for _ in range(5):
        z, w, v = kiss99_mwc_pair(z, w)
        got.append((z, w, v))
    assert got == [
        (812916871, 275137954, 820856226),
        (307853267, 320872198, 2331188998),
        (1134028772, 142960896, 4033440000),
        (2194645019, 483842181, 3169966213),
        (1515281890, 997729382, 2572821606),
    ]


def test_lcg_equivalence_exhaustive_small() -> None:
    # Every state of every lag-1 MWC with b = 16 and 2 <= a < 16.
    b = 16
    for a in range(2, b):
        m = a * b - 1
        for x in range(b):
            for c in range(a):
                z = to_lcg(x, c, a)
                assert from_lcg(z, a) == (x, c)
                x2, c2 = mwc_next(x, c, a, b)
                z2 = to_lcg(x2, c2, a)
                if z in (0, m):
                    assert z2 == z  # the two fixed points
                else:
                    assert 0 < z2 < m and z2 == a * z % m


def test_period_is_order_of_b_small() -> None:
    # Brute force: from a state with 0 < z < m the period is the order of a modulo m / gcd(z, m);
    # in particular it is the order of b (= order of a, since a b = 1 mod m) when gcd(z, m) = 1.
    for b in (8, 16, 32):
        for a in range(2, b):
            m = a * b - 1
            o = _order(b, m)
            assert o == _order(a, m)
            for x in range(b):
                for c in range(a):
                    z = to_lcg(x, c, a)
                    if z in (0, m):
                        continue
                    y, d, n = *mwc_next(x, c, a, b), 1
                    while (y, d) != (x, c):
                        y, d = mwc_next(y, d, a, b)
                        n += 1
                    assert n == _order(a, m // gcd(z, m))
                    if gcd(z, m) == 1:
                        assert n == o


def test_safe_prime_multipliers_give_period() -> None:
    # b = 2^32 is a square mod m, so its order divides (m - 1)/2; if that is a prime q
    # and b is not 1 mod m, the order is exactly q.
    for a, bits in ((A64, 62), (698769069, 60)):
        m = a * B32 - 1
        q = (m - 1) // 2
        assert _is_prime(m) and _is_prime(q)
        assert pow(B32, q, m) == 1 and B32 % m != 1
        assert 2**bits < q < 2 ** (bits + 1)
    for a in (36969, 18000):  # the KISS99 components, base 2^16
        m = a * (1 << 16) - 1
        q = (m - 1) // 2
        assert _is_prime(m) and _is_prime(q) and pow(1 << 16, q, m) == 1


def test_jump_matches_stepping() -> None:
    x, c = 123456789, 362436
    y, d = x, c
    for _ in range(1000):
        y, d = mwc_next(y, d, A64, B32)
    assert mwc_jump(x, c, A64, B32, 1000) == (y, d)
    m = A64 * B32 - 1
    q = (m - 1) // 2
    assert mwc_jump(x, c, A64, B32, q) == (x, c)


def test_lag_r_cycle_lengths_divide_order() -> None:
    for b, r in ((4, 2), (8, 2), (4, 3)):
        for a in range(2, b):
            m = a * b**r - 1
            if gcd(b, m) != 1:
                continue
            o = _order(b, m)
            lengths = set()
            for xs in product(range(b), repeat=r):
                for c in range(a):
                    s, seen = (xs, c), {}
                    while s not in seen:
                        seen[s] = len(seen)
                        s = mwc_lag_next(*s, a, b)
                    lengths.add(len(seen) - seen[s])
            assert all(o % L == 0 for L in lengths)
            assert max(lengths) == o


def test_output_uniformity() -> None:
    out = mwc_stream(20000, 123456789, 362436, A64, B32)
    counts = [0] * 16
    for v in out:
        counts[v >> 28] += 1
    e = len(out) / 16
    chi2 = sum((k - e) ** 2 / e for k in counts)
    assert chi2 < 37.70  # the 0.999 quantile of chi-square with 15 degrees of freedom
