# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamming-bound/. The authors are listed in prov/39271D.jsonl.

import random
from itertools import combinations, product

from hamming_bound import (
    binary_syndromes_distinct, entropy_q, hamming_bound, hamming_code_words, hamming_rate_bound,
    meets_hamming_bound, min_distance_linear, perfect_parameter_sets, qary_linear_code,
    qary_min_distance, volume,
)

# A_2(n, d) from A. E. Brouwer, Table of general binary codes,
# https://aeb.win.tue.nl/codes/binary-1.html (columns d = 4, 6, 8; A_2(n - 1, d - 1) = A_2(n, d)).
BROUWER = {
    (6, 4): 4, (7, 4): 8, (8, 4): 16, (9, 4): 20, (10, 4): 40, (11, 4): 72, (12, 4): 144,
    (13, 4): 256, (14, 4): 512, (15, 4): 1024, (16, 4): 2048,
    (9, 6): 4, (10, 6): 6, (11, 6): 12, (12, 6): 24, (13, 6): 32, (14, 6): 64, (15, 6): 128,
    (16, 6): 256, (12, 8): 4, (14, 8): 8, (15, 8): 16, (16, 8): 32, (17, 8): 36, (24, 8): 4096,
}

# The binary Golay code: generator polynomial x^11 + x^10 + x^6 + x^5 + x^4 + x^2 + 1
# (MacWilliams and Sloane, Chapter 20).
GOLAY_G = (1 << 11) | (1 << 10) | (1 << 6) | (1 << 5) | (1 << 4) | (1 << 2) | 1


def test_volume_small() -> None:
    assert volume(2, 7, 1) == 8
    assert volume(2, 23, 3) == 2048
    assert volume(3, 11, 2) == 243
    assert volume(2, 90, 2) == 4096
    assert volume(5, 3, 0) == 1
    assert volume(2, 3, 10) == 8  # the radius is cut at n


def test_volume_brute_force() -> None:
    for q in (2, 3, 4):
        for n in range(1, 6):
            words = list(product(range(q), repeat=n))
            for r in range(n + 1):
                cnt = sum(1 for w in words if sum(1 for a in w if a) <= r)
                assert cnt == volume(q, n, r)


def test_bound_holds_on_known_values() -> None:
    for (n, d), a in BROUWER.items():
        assert a <= hamming_bound(2, n, d)
        assert a <= hamming_bound(2, n - 1, d - 1)  # same A, other parameters


def test_hamming_codes_are_perfect() -> None:
    for r in (2, 3, 4):
        n = 2 ** r - 1
        words = hamming_code_words(r)
        assert len(words) == 2 ** (n - r)
        assert min_distance_linear(words) == 3
        assert meets_hamming_bound(2, n, len(words), 3)
        ok, cnt = binary_syndromes_distinct([i + 1 for i in range(n)], 1)
        assert ok and cnt == 2 ** r


def test_ball_cover_direct_for_hamming_7() -> None:
    words = hamming_code_words(3)
    cover = [0] * 128
    for c in words:
        cover[c] += 1
        for i in range(7):
            cover[c ^ (1 << i)] += 1
    assert cover == [1] * 128  # every word is in exactly one ball


def _gf2_mulmod_cyclic_words(g: int, n: int) -> list[int]:
    k = n - (g.bit_length() - 1)
    words = []
    for m in range(2 ** k):
        c, i = 0, 0
        while m >> i:
            if (m >> i) & 1:
                c ^= g << i
            i += 1
        words.append(c)
    return words


def test_binary_golay_is_perfect() -> None:
    words = _gf2_mulmod_cyclic_words(GOLAY_G, 23)
    assert len(words) == 4096
    assert min_distance_linear(words) == 7
    assert meets_hamming_bound(2, 23, 4096, 7)
    # Syndrome of x^i is x^i mod g(x); distinct syndromes for weight <= 3 and 2^11 of them.
    cols = []
    for i in range(23):
        s = 1 << i
        while s.bit_length() > 11:
            s ^= GOLAY_G << (s.bit_length() - 12)
        cols.append(s)
    ok, cnt = binary_syndromes_distinct(cols, 3)
    assert ok and cnt == 2 ** 11
    ok4, _ = binary_syndromes_distinct(cols, 4)
    assert not ok4  # radius 4 balls overlap


def test_ternary_golay_and_hamming_are_perfect() -> None:
    # Ternary Golay: generator polynomial x^5 + x^4 - x^3 + x^2 - 1 over GF(3)
    # (MacWilliams and Sloane, Chapter 20). Coefficients from x^0 up.
    g = [2, 0, 1, 2, 1, 1]
    gen = [tuple(([0] * i + g + [0] * 11)[:11]) for i in range(6)]
    words = qary_linear_code(gen, 3)
    assert len(set(words)) == 729
    assert qary_min_distance(words) == 5
    assert meets_hamming_bound(3, 11, 729, 5)
    # A [4, 2, 3] ternary code: every such code has the parameters of the ternary Hamming code.
    gen_h = [(1, 0, 2, 2), (0, 1, 2, 1)]
    words = qary_linear_code(gen_h, 3)
    assert qary_min_distance(words) == 3
    assert meets_hamming_bound(3, 4, 9, 3)


def test_not_perfect_examples() -> None:
    assert not meets_hamming_bound(2, 24, 4096, 8)  # extended Golay: even d
    assert not meets_hamming_bound(2, 10, 40, 4)
    assert not meets_hamming_bound(2, 9, 40, 3)  # A_2(9, 3) = 40 < 51


def test_perfect_parameter_search() -> None:
    sets = perfect_parameter_sets(2, 1100, 8)
    ham = [(2 ** r - 1, 1, 2 ** r - 1 - r) for r in range(3, 11)]
    assert sorted(sets) == sorted(ham + [(23, 3, 12), (90, 2, 78)])
    sets3 = perfect_parameter_sets(3, 400, 6)
    assert (11, 2, 6) in sets3
    assert all(t == 1 or (n, t) == (11, 2) for n, t, _ in sets3)


def test_no_perfect_90_78_5_code_counting() -> None:
    # The words of weight 3 that start with 11 would be covered 3 at a time by codewords
    # of weight 5 that start with 11. There are 88 of them and 3 does not divide 88.
    assert len([c for c in combinations(range(2, 90), 1)]) == 88
    assert 88 % 3 != 0


def test_asymptotic_values() -> None:
    assert abs(hamming_rate_bound(0.0) - 1.0) < 1e-12
    assert abs(hamming_rate_bound(1.0)) < 1e-12
    assert abs(hamming_rate_bound(0.2) - 0.531) < 1e-3
    assert abs(entropy_q(2 / 3, 3) - 1.0) < 1e-12  # h_q(1 - 1/q) = 1
    prev = 2.0
    for i in range(101):
        v = hamming_rate_bound(i / 100)
        assert v <= prev + 1e-12
        prev = v


def test_finite_bound_converges_to_asymptotic() -> None:
    from math import log2
    for delta in (0.1, 0.2, 0.3):
        n = 2000
        d = int(delta * n)
        r = log2(hamming_bound(2, n, d)) / n
        assert abs(r - hamming_rate_bound(d / n)) < 0.01


def test_random_codes_satisfy_bound() -> None:
    rng = random.Random(1950)
    for _ in range(200):
        n = rng.randint(4, 10)
        d = rng.randint(2, n)
        code: list[int] = []
        order = list(range(2 ** n))
        rng.shuffle(order)
        for x in order:
            if all((x ^ c).bit_count() >= d for c in code):
                code.append(x)
        assert len(code) <= hamming_bound(2, n, d)
