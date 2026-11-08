# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-feedback-shift-register/. The authors are listed in prov/C3FG9T.jsonl.

import pytest

from linear_feedback_shift_register import (
    FibonacciLFSR,
    GaloisLFSR,
    gf2_mulmod,
    is_primitive,
    state_period,
)

P4 = 0b11001  # x^4 + x^3 + 1


def test_fibonacci_trace() -> None:
    g = FibonacciLFSR(P4, 4, 0b0001)
    bits = [g.step() for _ in range(19)]
    assert "".join(map(str, bits)) == "1000111101011001000"
    assert sum(bits[:15]) == 8
    windows = {tuple(bits[i:i + 4]) for i in range(15)}
    assert len(windows) == 15 and (0, 0, 0, 0) not in windows


def test_galois_trace() -> None:
    g = GaloisLFSR(P4, 4, 0b0001)
    bits = [g.step() for _ in range(15)]
    assert bits == [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]
    assert g.s == 0b0001
    # the Galois output obeys the same recurrence s_(i+4) = s_(i+3) xor s_i
    more = bits + [g.step() for _ in range(15)]
    assert all(more[i + 4] == more[i + 3] ^ more[i] for i in range(26))


def test_sixteen_bit_reference() -> None:
    # Taps 16, 14, 13, 11 of the classic example: bit = s0 ^ s2 ^ s3 ^ s5, seed 0xACE1.
    poly = (1 << 16) | (1 << 5) | (1 << 3) | (1 << 2) | 1
    g = FibonacciLFSR(poly, 16, 0xACE1)
    seen = []
    for _ in range(3):
        g.step()
        seen.append(g.s)
    assert seen == [0x5670, 0xAB38, 0x559C]

    def gal_right(x: int) -> int:  # the right-shift Galois form with toggle mask 0xB400
        lsb = x & 1
        x >>= 1
        return x ^ 0xB400 if lsb else x

    assert state_period(gal_right, 0xACE1) == 65535


def _fib_state_map(poly: int, k: int):
    def f(s: int) -> int:
        g = FibonacciLFSR(poly, k, s)
        g.step()
        return g.s
    return f


def test_primitive_iff_maximal_period() -> None:
    for k in range(2, 9):
        count = 0
        for low in range(1 << k):
            poly = (1 << k) | low
            if not poly & 1:
                assert not is_primitive(poly, k)
                continue
            prim = is_primitive(poly, k)
            count += prim
            gal = state_period(lambda t: gf2_mulmod(t, 2, poly, k), 1)
            assert (gal == (1 << k) - 1) == prim
            if k <= 6:
                assert (state_period(_fib_state_map(poly, k), 1) == (1 << k) - 1) == prim
        # phi(2^k - 1) / k primitive polynomials of degree k
        n = (1 << k) - 1
        phi = sum(1 for j in range(1, n + 1) if __import__("math").gcd(j, n) == 1)
        assert count == phi // k


def test_irreducible_not_primitive() -> None:
    p = 0b11111  # x^4 + x^3 + x^2 + x + 1 divides x^5 - 1
    assert not is_primitive(p, 4)
    lengths = set()
    for s in range(1, 16):
        lengths.add(state_period(lambda t: gf2_mulmod(t, 2, p, 4), s))
    assert lengths == {5}


def test_known_primitive_polynomials() -> None:
    assert is_primitive((1 << 16) | (1 << 5) | (1 << 3) | (1 << 2) | 1, 16)
    assert is_primitive((1 << 32) | (1 << 22) | (1 << 2) | (1 << 1) | 1, 32)
    assert is_primitive((1 << 64) | (1 << 4) | (1 << 3) | (1 << 1) | 1, 64)
    assert not is_primitive((1 << 16) | 1, 16)


def test_zero_state_and_bad_degree() -> None:
    with pytest.raises(ValueError):
        FibonacciLFSR(P4, 4, 0)
    with pytest.raises(ValueError):
        GaloisLFSR(P4, 4, 16)  # masks to 0
    with pytest.raises(ValueError):
        GaloisLFSR(0b111, 4, 1)


def test_largest_state() -> None:
    k = 64
    poly = (1 << 64) | (1 << 4) | (1 << 3) | (1 << 1) | 1
    g = GaloisLFSR(poly, k, (1 << 64) - 1)
    assert g.step() == 1 and 0 < g.s < (1 << 64)
    f = FibonacciLFSR(poly, k, (1 << 64) - 1)
    f.step()
    assert 0 < f.s < (1 << 64)
