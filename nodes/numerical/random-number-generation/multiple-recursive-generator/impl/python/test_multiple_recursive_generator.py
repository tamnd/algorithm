# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-recursive-generator/. The authors are listed in prov/S7DSDC.jsonl.

import pytest

from multiple_recursive_generator import (
    characteristic_polynomial,
    is_primitive_knuth,
    mrg_jump,
    mrg_next,
    mrg_stream,
    poly_x_power,
)


def prime_factors(n: int) -> list[int]:
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def is_prime(n: int) -> bool:
    """Miller-Rabin with the first 13 prime bases, exact for n < 3.3 * 10^24."""
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    if n < 2:
        return False
    for p in bases:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for b in bases:
        x = pow(b, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def period(seed: list[int], a: list[int], m: int) -> int:
    x = list(seed)
    start, n = tuple(x), 0
    while True:
        mrg_next(x, a, m)
        n += 1
        if tuple(x) == start:
            return n


def is_primitive_generic(a: list[int], p: int) -> bool:
    k = len(a)
    mod = characteristic_polynomial(a, p)
    if mod[0] == 0:
        return False
    n = p**k - 1
    one = [1] + [0] * (k - 1)
    if poly_x_power(n, mod, p) != one:
        return False
    return all(poly_x_power(n // q, mod, p) != one for q in prime_factors(n))


def test_trace_of_the_page() -> None:
    # x_n = x_{n-1} + 4 x_{n-2} mod 7 from x_0 = 1, x_{-1} = 0 (newest first).
    assert mrg_stream([1, 0], [1, 4], 7, 12) == [1, 5, 2, 1, 2, 6, 0, 3, 3, 1, 6, 3]
    assert period([1, 0], [1, 4], 7) == 48
    assert period([1, 0], [1, 3], 7) == 24


def test_brute_force_matches_primitivity() -> None:
    for p, k in [(7, 2), (5, 2), (3, 3), (5, 3), (2, 4), (3, 4)]:
        r = (p**k - 1) // (p - 1)
        fr, fp = prime_factors(r), prime_factors(p - 1) if p > 2 else []
        count = 0
        coeffs = [[]]
        for _ in range(k):
            coeffs = [c + [v] for c in coeffs for v in range(p)]
        for a in coeffs:
            if a[-1] == 0:
                continue
            seed = [1] + [0] * (k - 1)
            full = period(seed, a, p) == p**k - 1
            assert full == is_primitive_generic(a, p)
            if p > 2:
                assert full == is_primitive_knuth(a, p, fr, fp)
            count += full
        assert count > 0


def test_full_period_means_every_nonzero_state() -> None:
    a, p = [1, 4], 7
    x, seen = [1, 0], set()
    for _ in range(48):
        mrg_next(x, a, p)
        seen.add(tuple(x))
    assert len(seen) == 48 and (0, 0) not in seen


def test_mrg32k3a_components_are_primitive() -> None:
    # Each component has k = 3 and a prime modulus with r = m^2 + m + 1 prime,
    # so the only prime factor of r is r itself.
    for a, m in [([0, 1403580, -810728], 4294967087), ([527612, 0, -1370589], 4294944443)]:
        assert is_prime(m)
        r = m * m + m + 1
        assert is_prime(r)
        assert is_primitive_knuth([v % m for v in a], m, [r], prime_factors(m - 1))


def test_jump_equals_stepping() -> None:
    a, m = [0, 1403580, (-810728) % 4294967087], 4294967087
    seed = [12345, 12345, 12345]
    x = list(seed)
    for steps in range(1, 50):
        mrg_next(x, a, m)
        assert mrg_jump(seed, a, m, steps) == x
    assert mrg_jump([1, 0], [1, 4], 7, 48) == [1, 0]


def test_zero_seed_rejected() -> None:
    with pytest.raises(ValueError):
        mrg_stream([0, 0], [1, 4], 7, 1)
    with pytest.raises(ValueError):
        mrg_stream([7, 14], [1, 4], 7, 1)


def test_uniform_counts() -> None:
    # Over one full period of m^k - 1 values, each nonzero residue appears m^(k-1) times
    # and 0 appears m^(k-1) - 1 times.
    p, a = 7, [1, 4]
    out = mrg_stream([1, 0], a, p, 48)
    assert out.count(0) == 6 and all(out.count(v) == 7 for v in range(1, 7))
