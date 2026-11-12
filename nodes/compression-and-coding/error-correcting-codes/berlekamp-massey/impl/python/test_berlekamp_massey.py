# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berlekamp-massey/. The authors are listed in prov/VWBGTF.jsonl.

import itertools
import random

import pytest

from berlekamp_massey import (PrimeField, berlekamp_massey, error_locator_from_syndromes, generates,
                              linear_complexity_profile)
from gf import GF2m

F2 = PrimeField(2)
F3 = PrimeField(3)
F7 = PrimeField(7)
F16 = GF2m(4, 0b10011)  # alpha is a root of x^4 + x + 1


def brute_force_shortest(s: list[int], f, q: int) -> int:
    """The smallest L such that some connection polynomial of degree <= L generates s."""
    for L in range(len(s) + 1):
        for taps in itertools.product(range(q), repeat=L):
            if generates(s, L, [1, *taps], f):
                return L
    raise AssertionError("L = len(s) always works")


def test_worked_example() -> None:
    s = [1, 0, 1, 0, 0, 1, 1, 1, 0, 1]
    assert berlekamp_massey(s, F2) == (3, [1, 1, 0, 1])  # C(x) = 1 + x + x^3
    assert linear_complexity_profile(s, F2) == [1, 1, 2, 2, 3, 3, 3, 3, 3, 3]


def test_reed_solomon_example() -> None:
    # RS(15, 11) over GF(16), b = 1, errors alpha^5 at position 2 and alpha^11 at position 7
    a = F16.alpha
    syn = [a(4), a(13), a(9), a(10)]  # S_1 .. S_4
    for j in range(1, 5):
        assert syn[j - 1] == F16.mul(a(5), a(2 * j)) ^ F16.mul(a(11), a(7 * j))
    L, c = berlekamp_massey(syn, F16)
    assert L == 2 and c == [1, a(12), a(9)]
    assert c == F16.pmul([1, a(2)], [1, a(7)])  # (1 - X_1 x)(1 - X_2 x)


def test_edges() -> None:
    assert berlekamp_massey([], F2) == (0, [1])
    assert berlekamp_massey([0] * 9, F7) == (0, [1])
    for n in range(1, 10):
        s = [0] * (n - 1) + [3]
        L, c = berlekamp_massey(s, F7)
        assert L == n and generates(s, L, c, F7)
    assert berlekamp_massey([5], F7)[0] == 1
    L, c = berlekamp_massey([2, 2, 2, 2, 2], F7)  # constant: s_j = s_(j-1)
    assert (L, c) == (1, [1, 6])
    with pytest.raises(ValueError):
        PrimeField(9)


def test_brute_force_gf2_all_sequences() -> None:
    for n in range(0, 12):
        for s in itertools.product(range(2), repeat=n):
            s = list(s)
            L, c = berlekamp_massey(s, F2)
            assert len(c) == L + 1 and c[0] == 1
            assert generates(s, L, c, F2)
            assert L == brute_force_shortest(s, F2, 2)


def test_brute_force_gf3_all_sequences() -> None:
    for n in range(0, 7):
        for s in itertools.product(range(3), repeat=n):
            s = list(s)
            L, c = berlekamp_massey(s, F3)
            assert generates(s, L, c, F3)
            assert L == brute_force_shortest(s, F3, 3)


def test_profile_rule() -> None:
    # L_(r+1) is L_r or r + 1 - L_r, and a change always goes up to r + 1 - L_r
    rng = random.Random(11)
    for _ in range(300):
        s = [rng.randrange(7) for _ in range(rng.randrange(1, 25))]
        prof = [0] + linear_complexity_profile(s, F7)
        for r in range(len(s)):
            assert prof[r + 1] in (prof[r], r + 1 - prof[r])
            assert prof[r + 1] >= prof[r]


def test_recovers_lfsr_from_2l_terms() -> None:
    # A sequence of linear complexity L is fixed by its first 2L terms (unique shortest LFSR)
    rng = random.Random(2024)
    for f, q in ((F7, 7), (F16, 16)):
        for _ in range(300):
            L = rng.randrange(1, 9)
            c = [1] + [rng.randrange(q) for _ in range(L - 1)] + [rng.randrange(1, q)]
            s = [rng.randrange(q) for _ in range(L)]
            while len(s) < 2 * L + rng.randrange(0, 4):
                acc = f.zero
                for i in range(1, L + 1):
                    acc = f.sub(acc, f.mul(c[i], s[-i]))
                s.append(acc)
            L2, c2 = berlekamp_massey(s, f)
            assert generates(s, L2, c2, f) and L2 <= L
            if L2 == L:
                assert c2 == c


def test_error_locator_random_patterns() -> None:
    # S_j = sum_k Y_k X_k^j, j = 1 .. 2t, with nu <= t errors: BM returns prod (1 - X_k x)
    rng = random.Random(7)
    n, t = 15, 3
    for _ in range(600):
        nu = rng.randrange(0, t + 1)
        pos = rng.sample(range(n), nu)
        val = [rng.randrange(1, 16) for _ in pos]
        syn = []
        for j in range(1, 2 * t + 1):
            v = 0
            for p, y in zip(pos, val):
                v ^= F16.mul(y, F16.alpha(p * j))
            syn.append(v)
        want = [1]
        for p in pos:
            want = F16.pmul(want, [1, F16.alpha(p)])
        assert error_locator_from_syndromes(syn, F16) == want
