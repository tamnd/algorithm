# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfsr/. The authors are listed in prov/5N3GKG.jsonl.

import random

from lfsr import (
    berlekamp_massey,
    correlation_attack,
    fibonacci_lfsr,
    galois_lfsr,
    geffe,
    period,
)

# Primitive connection polynomials 1 + ... + x^L (their reciprocals are the
# primitive trinomials and pentanomials x^4+x^3+1, x^5+x^3+1, x^7+x^6+1,
# x^8+x^6+x^5+x^4+1 and x^9+x^5+1).
P4 = [1, 1, 0, 0, 1]  # 1 + x + x^4
P5 = [1, 0, 1, 0, 0, 1]  # 1 + x^2 + x^5
P7 = [1, 1, 0, 0, 0, 0, 0, 1]  # 1 + x + x^7
P8 = [1, 0, 1, 1, 1, 0, 0, 0, 1]  # 1 + x^2 + x^3 + x^4 + x^8
P9 = [1, 0, 0, 0, 1, 0, 0, 0, 0, 1]  # 1 + x^4 + x^9


def test_small_example() -> None:
    # s[t] = s[t-1] + s[t-4], from the state 1 0 0 0, computed by hand.
    assert fibonacci_lfsr(P4, [1, 0, 0, 0], 15) == [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0]
    # The Galois form from a(x) = 1 gives the same sequence shifted by one place.
    assert galois_lfsr(P4, 1, 14) == [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0]


def test_primitive_period() -> None:
    rng = random.Random(1)
    for c in (P4, P5, P7, P8, P9):
        big_l = len(c) - 1
        for _ in range(3):
            st = [0] * big_l
            while not any(st):
                st = [rng.randrange(2) for _ in range(big_l)]
            assert period(c, st) == 2**big_l - 1


def test_non_primitive_period_is_shorter() -> None:
    # 1 + x^2 + x^4 = (1 + x + x^2)^2 is not irreducible: period 6, not 15.
    assert period([1, 0, 1, 0, 1], [1, 0, 0, 0]) == 6


def test_galois_is_a_shift_of_fibonacci() -> None:
    rng = random.Random(2)
    for c in (P4, P5, P7, P8):
        big_l = len(c) - 1
        n = 2**big_l - 1
        fib = fibonacci_lfsr(c, [1] + [0] * (big_l - 1), n)
        gal = galois_lfsr(c, rng.randrange(1, 2**big_l), 3 * n)
        # The Galois output satisfies the same recurrence.
        for t in range(big_l, len(gal)):
            assert gal[t] == sum(c[i] & gal[t - i] for i in range(1, big_l + 1)) % 2
        # And one period of it is a cyclic shift of one Fibonacci period.
        assert any(gal[k:k + n] == fib for k in range(n))


def test_berlekamp_massey_known() -> None:
    s = fibonacci_lfsr(P5, [1, 0, 0, 1, 1], 10)
    assert berlekamp_massey(s) == (5, P5)


def test_berlekamp_massey_recovers_random_lfsr() -> None:
    rng = random.Random(3)
    for _ in range(50):
        big_l = rng.randrange(1, 20)
        c = [1] + [rng.randrange(2) for _ in range(big_l - 1)] + [1]
        st = [rng.randrange(2) for _ in range(big_l)]
        s = fibonacci_lfsr(c, st, 2 * big_l + 100)
        found_l, found_c = berlekamp_massey(s[: 2 * big_l])
        assert found_l <= big_l
        # The found LFSR, loaded with the first bits, predicts the next 100 bits.
        pred = fibonacci_lfsr(found_c, s[:found_l], 2 * big_l + 100) if found_l else [0] * (2 * big_l + 100)
        assert pred == s


def test_linear_complexity_of_m_sequence() -> None:
    s = fibonacci_lfsr(P9, [1] * 9, 600)
    assert berlekamp_massey(s)[0] == 9


def test_geffe_correlation() -> None:
    rng = random.Random(4)
    n = 4000
    x = [[rng.randrange(2) for _ in range(n)] for _ in range(3)]
    z = geffe(*x)
    agree2 = sum(a == b for a, b in zip(z, x[1])) / n
    agree3 = sum(a == b for a, b in zip(z, x[2])) / n
    agree1 = sum(a == b for a, b in zip(z, x[0])) / n
    assert abs(agree2 - 0.75) < 0.03 and abs(agree3 - 0.75) < 0.03
    assert abs(agree1 - 0.5) < 0.03


def test_siegenthaler_attack_on_toy_geffe() -> None:
    # Toy Geffe generator with LFSRs of lengths 7, 8 and 9 (key: 24 bits).
    rng = random.Random(5)

    def rand_state(big_l: int) -> list[int]:
        st = [0] * big_l
        while not any(st):
            st = [rng.randrange(2) for _ in range(big_l)]
        return st

    k1, k2, k3 = rand_state(7), rand_state(8), rand_state(9)
    n = 200
    x1 = fibonacci_lfsr(P7, k1, n)
    x2 = fibonacci_lfsr(P8, k2, n)
    x3 = fibonacci_lfsr(P9, k3, n)
    z = geffe(x1, x2, x3)
    # Attack registers 2 and 3 one at a time: 2^8 + 2^9 trials, not 2^24.
    g2 = correlation_attack(P8, z)
    g3 = correlation_attack(P9, z)
    assert (g2, g3) == (k2, k3)
    # With x2 and x3 known, try the 2^7 states of register 1.
    y2, y3 = fibonacci_lfsr(P8, g2, n), fibonacci_lfsr(P9, g3, n)
    hits = []
    for v in range(1, 128):
        st = [(v >> i) & 1 for i in range(7)]
        if geffe(fibonacci_lfsr(P7, st, n), y2, y3) == z:
            hits.append(st)
    assert hits == [k1]
