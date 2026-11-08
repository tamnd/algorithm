# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mersenne-twister/. The authors are listed in prov/0AJ2E4.jsonl.

import random

from mersenne_twister import MASK, MT19937, temper, untemper


def test_reference_seed_5489() -> None:
    g = MT19937(5489)
    assert [g.next_u32() for _ in range(3)] == [3499211612, 581869302, 3890346734]
    g = MT19937(5489)
    for _ in range(9999):
        g.next_u32()
    assert g.next_u32() == 4123659995  # the C++ requirement for std::mt19937


def test_reference_init_by_array() -> None:
    # The first outputs in mt19937ar.out of Matsumoto and Nishimura.
    g = MT19937()
    g.init_by_array([0x123, 0x234, 0x345, 0x456])
    assert [g.next_u32() for _ in range(5)] == [
        1067595299, 955945823, 477289528, 4107218783, 4228976476]


def test_matches_python_random() -> None:
    for seed in (0, 1, 5489, 2**32 - 1):
        g = MT19937()
        g.init_by_array([seed])
        r = random.Random(seed)
        assert [g.next_u32() for _ in range(700)] == [r.getrandbits(32) for _ in range(700)]
        assert [g.random() for _ in range(10)] == [r.random() for _ in range(10)]


def test_seed_zero_and_largest_seed() -> None:
    a = MT19937(0)
    b = MT19937(2**32)  # masked to 0
    assert [a.next_u32() for _ in range(5)] == [b.next_u32() for _ in range(5)]
    c = MT19937(2**32 - 1)
    xs = [c.next_u32() for _ in range(2000)]
    assert all(0 <= x <= MASK for x in xs)
    assert len(set(xs)) > 1990


def test_tempering_is_invertible_and_state_recovery() -> None:
    rng = random.Random(3)
    for y in [0, 1, MASK, 0x80000000] + [rng.getrandbits(32) for _ in range(2000)]:
        assert untemper(temper(y)) == y
    g = MT19937(12345)
    outs = [g.next_u32() for _ in range(624)]
    clone = MT19937(0)
    clone.mt = [untemper(z) for z in outs]
    clone.index = 624
    assert [clone.next_u32() for _ in range(1000)] == [g.next_u32() for _ in range(1000)]


def _linear_complexity(bits: list[int]) -> int:
    """Berlekamp-Massey over GF(2) with Python ints as bit vectors."""
    c, b = 1, 1  # connection polynomials, bit i = coefficient of x^i
    length, m = 0, -1
    rev = 0  # bit i of rev is s_(n - i)
    for n, s in enumerate(bits):
        rev = (rev << 1) | s
        d = (c & rev).bit_count() & 1
        if d:
            t = c
            c ^= b << (n - m)
            if 2 * length <= n:
                length, m, b = n + 1 - length, n, t
    return length


def test_linear_complexity_is_19937() -> None:
    # The characteristic polynomial is irreducible of degree 19937, so every
    # nonzero output bit sequence has linear complexity exactly 19937.
    g = MT19937(5489)
    bits = [g.next_u32() & 1 for _ in range(2 * 19937 + 200)]
    assert _linear_complexity(bits) == 19937


def test_chi_square_bytes() -> None:
    g = MT19937(2024)
    counts = [0] * 256
    n = 51200
    for _ in range(n):
        counts[g.next_u32() >> 24] += 1
    e = n / 256
    chi2 = sum((x - e) ** 2 / e for x in counts)
    assert chi2 < 330.5  # 0.999 quantile of chi-square with 255 degrees of freedom
