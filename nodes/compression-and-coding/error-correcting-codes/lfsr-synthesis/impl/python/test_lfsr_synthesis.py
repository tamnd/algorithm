# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfsr-synthesis/. The authors are listed in prov/FQKAS9.jsonl.

import itertools
import random
from fractions import Fraction

from lfsr_synthesis import (generates, linear_complexity_profile, shortest_lfsr_brute_force,
                            shortest_lfsr_euclid, shortest_lfsr_linear_algebra)


def m_sequence(n: int) -> list[int]:
    """s_j = s_(j-3) + s_(j-4) over GF(2): C(x) = 1 + x^3 + x^4, the reciprocal of x^4 + x + 1."""
    s = [1, 0, 0, 0]
    while len(s) < n:
        s.append(s[-3] ^ s[-4])
    return s


def test_m_sequence_example() -> None:
    s = m_sequence(30)
    assert s[:15] == s[15:30]  # period 2^4 - 1
    assert len({tuple(s[i:i + 4]) for i in range(15)}) == 15  # every nonzero state appears
    for n in range(8, 31):  # 2L = 8 terms are enough
        assert shortest_lfsr_euclid(s[:n], 2) == (4, [1, 0, 0, 1, 1])
        assert shortest_lfsr_linear_algebra(s[:n], 2) == (4, [1, 0, 0, 1, 1])
    assert linear_complexity_profile(s[:8], 2) == [1, 1, 1, 1, 4, 4, 4, 4]


def test_edges() -> None:
    assert shortest_lfsr_euclid([], 5) == (0, [1])
    assert shortest_lfsr_euclid([0, 0, 0], 5) == (0, [1])
    assert shortest_lfsr_euclid([0, 0, 0, 2], 5)[0] == 4  # 0^(N-1) a needs L = N
    assert shortest_lfsr_linear_algebra([0, 0, 0, 2], 5)[0] == 4
    assert shortest_lfsr_euclid([3, 3, 3, 3], 5) == (1, [1, 4])  # s_j = s_(j-1)


def test_three_methods_agree_exhaustively() -> None:
    for p, nmax in ((2, 10), (3, 6)):
        for n in range(nmax + 1):
            for s in itertools.product(range(p), repeat=n):
                s = list(s)
                L, polys = shortest_lfsr_brute_force(s, p)
                L1, c1 = shortest_lfsr_linear_algebra(s, p)
                L2, c2 = shortest_lfsr_euclid(s, p)
                assert L1 == L2 == L
                assert c1 in polys and c2 in polys
                # uniqueness exactly when 2L <= N; otherwise p^(2L - N) shortest LFSRs
                assert len(polys) == (1 if 2 * L <= n else p ** (2 * L - n))


def test_random_gf7_agree() -> None:
    rng = random.Random(77)
    for _ in range(600):
        n = rng.randrange(1, 18)
        if rng.random() < 0.5:
            s = [rng.randrange(7) for _ in range(n)]
        else:  # a sequence of low linear complexity
            L = rng.randrange(1, 5)
            c = [1] + [rng.randrange(7) for _ in range(L)]
            s = [rng.randrange(7) for _ in range(L)]
            while len(s) < n:
                s.append(-sum(c[i] * s[-i] for i in range(1, L + 1)) % 7)
            s = s[:n]
        L1, c1 = shortest_lfsr_linear_algebra(s, 7)
        L2, c2 = shortest_lfsr_euclid(s, 7)
        assert L1 == L2 and generates(s, L1, c1, 7) and generates(s, L2, c2, 7)
        if 2 * L1 <= n:
            assert c1 == c2


def test_profile_rule() -> None:
    rng = random.Random(3)
    for _ in range(200):
        s = [rng.randrange(2) for _ in range(rng.randrange(1, 30))]
        prof = [0] + linear_complexity_profile(s, 2)
        for r in range(len(s)):
            assert prof[r + 1] in (prof[r], max(prof[r], r + 1 - prof[r]))


def test_counts_and_mean_over_gf2() -> None:
    # Number of binary sequences of length N with linear complexity L >= 1 is
    # 2^min(2N - 2L, 2L - 1), and the mean is
    # N/2 + (4 + (N mod 2))/18 - 2^(-N) (N/3 + 2/9)
    # (Rueppel, Analysis and Design of Stream Ciphers, 1986, the linear complexity of random sequences)
    for n in range(1, 11):
        count = {}
        total = 0
        for s in itertools.product(range(2), repeat=n):
            L = shortest_lfsr_euclid(list(s), 2)[0]
            count[L] = count.get(L, 0) + 1
            total += L
        assert count[0] == 1
        for L in range(1, n + 1):
            assert count[L] == 2 ** min(2 * n - 2 * L, 2 * L - 1)
        mean = Fraction(n, 2) + Fraction(4 + n % 2, 18) - Fraction(1, 2 ** n) * (Fraction(n, 3) + Fraction(2, 9))
        assert Fraction(total, 2 ** n) == mean
