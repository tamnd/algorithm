# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mrg32k3a/. The authors are listed in prov/3EWTJP.jsonl.

from math import gcd

import pytest

from mrg32k3a import (
    A13N,
    NORM,
    A1,
    A2,
    M1,
    M2,
    mat_pow2,
    mrg32k3a_jump,
    mrg32k3a_next,
    mrg32k3a_stream,
)


def test_reference_outputs() -> None:
    # L'Ecuyer's 1999 code with all six seeds 12345 (the RngStreams default seed).
    assert mrg32k3a_stream(5) == [
        0.12701112204657714,
        0.3185275653967945,
        0.30918601558327008,
        0.82584686292711362,
        0.2216299157820229,
    ]


def test_jump_matrices_of_rngstreams() -> None:
    # The matrices A1p76, A2p76, A1p127, A2p127 printed in RngStream.c.
    assert mat_pow2(A1, 76, M1) == [
        [82758667, 1871391091, 4127413238],
        [3672831523, 69195019, 1871391091],
        [3672091415, 3528743235, 69195019],
    ]
    assert mat_pow2(A2, 76, M2) == [
        [1511326704, 3759209742, 1610795712],
        [4292754251, 1511326704, 3889917532],
        [3859662829, 4292754251, 3708466080],
    ]
    assert mat_pow2(A1, 127, M1) == [
        [2427906178, 3580155704, 949770784],
        [226153695, 1230515664, 3580155704],
        [1988835001, 986791581, 1230515664],
    ]
    assert mat_pow2(A2, 127, M2) == [
        [1464411153, 277697599, 1610723613],
        [32183930, 1464411153, 1022607788],
        [2824425944, 32183930, 2093834863],
    ]


def test_second_stream_and_substream() -> None:
    # RngStream.c compiled and run: the second stream starts 2^127 steps ahead,
    # the second substream of the first stream 2^76 steps ahead.
    x1, x2 = mrg32k3a_jump([12345] * 3, [12345] * 3, 127)
    assert mrg32k3a_stream(3, x1, x2) == [0.7595818622487196, 0.97831057326137083, 0.68513580819318265]
    y1, y2 = mrg32k3a_jump([12345] * 3, [12345] * 3, 76)
    assert mrg32k3a_stream(2, y1, y2) == [0.079398989797334632, 0.48033950475757409]


def test_small_jump_equals_stepping() -> None:
    x1, x2 = [1, 2, 3], [4, 5, 6]
    a, b = list(x1), list(x2)
    for _ in range(8):
        mrg32k3a_next(a, b)
    assert mrg32k3a_jump(x1, x2, 3) == (a, b)


def test_period_of_the_combination() -> None:
    m1c, m2c = M1**3 - 1, M2**3 - 1
    assert gcd(m1c, m2c) == 2
    period = m1c * m2c // 2
    assert 2**190 < period < 2**191


def test_combined_period_is_lcm_on_small_components() -> None:
    # Two small MRGs of order 2 with primitive polynomials: periods 48 (mod 7) and 120 (mod 11).
    def step(x, a, m):
        v = (a[0] * x[0] + a[1] * x[1]) % m
        return (v, x[0])

    def per(x, a, m):
        y, n = step(x, a, m), 1
        while y != x:
            y, n = step(y, a, m), n + 1
        return n

    p1, p2 = per((1, 0), (1, 4), 7), per((1, 0), (1, 3), 11)
    assert (p1, p2) == (48, 120)
    s, t, n = (1, 0), (1, 0), 0
    while True:
        s, t, n = step(s, (1, 4), 7), step(t, (1, 3), 11), n + 1
        if s == (1, 0) and t == (1, 0):
            break
    assert n == 240 == p1 * p2 // gcd(p1, p2)


def test_output_range_and_uniformity() -> None:
    out = mrg32k3a_stream(20000)
    assert all(0.0 < u < 1.0 for u in out)
    counts = [0] * 10
    for u in out:
        counts[int(u * 10)] += 1
    chi2 = sum((c - 2000) ** 2 / 2000 for c in counts)
    assert chi2 < 27.88  # the 0.999 quantile of chi-square with 9 degrees of freedom


def test_equal_components_give_largest_output() -> None:
    # p1 == p2 gives m1 * norm, just below 1: the generator never returns 0 or 1.
    # Here both new values are 0: p1 depends on x1[0], x1[1] and p2 on x2[0], x2[2].
    u = mrg32k3a_next([0, 0, 5], [0, 5, 0])
    assert u == M1 * 2.328306549295728e-10 and u < 1.0
    # The smallest output: p1 = 1 and p2 = 0, so p1 - p2 = 1.
    w = mrg32k3a_next([(-pow(A13N, -1, M1)) % M1, 0, 5], [0, 5, 0])
    assert w == NORM and w > 0.0


def test_bad_seeds() -> None:
    with pytest.raises(ValueError):
        mrg32k3a_stream(1, [0, 0, 0], [1, 1, 1])
    with pytest.raises(ValueError):
        mrg32k3a_stream(1, [1, 1, 1], [M2, 0, 0])
    with pytest.raises(ValueError):
        mrg32k3a_stream(1, [M1, 1, 1], [1, 1, 1])


def _is_prime(n: int) -> bool:
    # Miller-Rabin with the first 13 prime bases: exact for n < 3.3 * 10^24.
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
    assert n < 3 * 10**24
    return True


def _prime_factors(n: int) -> list[int]:
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def _z_power_mod(e: int, c: list[int], m: int) -> list[int]:
    # z^e modulo z^3 - c[0] z^2 - c[1] z - c[2] over GF(m); returns [r0, r1, r2] for r0 + r1 z + r2 z^2.
    def mul(u, v):
        w = [0] * 5
        for i in range(3):
            for j in range(3):
                w[i + j] = (w[i + j] + u[i] * v[j]) % m
        for d in (4, 3):  # z^3 = c0 z^2 + c1 z + c2
            t, w[d] = w[d], 0
            w[d - 1] = (w[d - 1] + t * c[0]) % m
            w[d - 2] = (w[d - 2] + t * c[1]) % m
            w[d - 3] = (w[d - 3] + t * c[2]) % m
        return w[:3]

    r, b = [1, 0, 0], [0, 1, 0]
    while e:
        if e & 1:
            r = mul(r, b)
        b, e = mul(b, b), e >> 1
    return r


def _knuth_primitive(c: list[int], m: int) -> bool:
    # Knuth 3.2.2 for k = 3: a3 = c[2] is a primitive root mod m, z^r = a3 with
    # r = (m^3 - 1)/(m - 1), and z^(r/q) is not a constant for each prime q dividing r.
    a3 = c[2] % m
    if not all(pow(a3, (m - 1) // q, m) != 1 for q in _prime_factors(m - 1)):
        return False
    r = (m**3 - 1) // (m - 1)
    if _z_power_mod(r, c, m) != [a3, 0, 0]:
        return False
    assert _is_prime(r)  # so the only q is r itself, and z^1 = z is not a constant
    return True


def test_components_are_primitive() -> None:
    assert _is_prime(M1) and _is_prime(M2)
    assert _knuth_primitive([0, 1403580, -810728 % M1], M1)
    assert _knuth_primitive([527612, 0, -1370589 % M2], M2)


def test_primitivity_check_on_small_cases() -> None:
    # Brute force over all order-3 recurrences mod 5: the check agrees with the period.
    m = 5
    for a1 in range(m):
        for a2 in range(m):
            for a3 in range(1, m):
                s, n = (1, 0, 0), 0
                while True:
                    s, n = ((a1 * s[0] + a2 * s[1] + a3 * s[2]) % m, s[0], s[1]), n + 1
                    if s == (1, 0, 0):
                        break
                r = (m**3 - 1) // (m - 1)  # 31, prime
                assert _is_prime(r)
                full = n == m**3 - 1
                assert _knuth_primitive([a1, a2, a3], m) == full
