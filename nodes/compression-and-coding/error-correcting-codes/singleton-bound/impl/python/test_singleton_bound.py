# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/singleton-bound/. The authors are listed in prov/HQ6X1P.jsonl.

import random
from itertools import product

from singleton_bound import (
    binary_mds_parameters, hamming_rate, is_mds, min_distance, puncture_is_injective,
    reed_solomon_words, singleton_bound, singleton_rate,
)

# A_2(n, d) from A. E. Brouwer, Table of general binary codes, https://aeb.win.tue.nl/codes/binary-1.html
BROUWER = {(8, 4): 16, (10, 4): 40, (12, 4): 144, (12, 6): 24, (16, 6): 256, (16, 8): 32, (24, 8): 4096}


def test_formula() -> None:
    assert singleton_bound(2, 7, 3) == 32
    assert singleton_bound(7, 6, 3) == 7 ** 4
    assert singleton_bound(3, 5, 5) == 3


def test_known_binary_values() -> None:
    for (n, d), a in BROUWER.items():
        assert a <= singleton_bound(2, n, d)


def test_reed_solomon_is_mds() -> None:
    for p, kmax in ((5, 5), (7, 3)):
        for n in range(2, p + 1):
            for k in range(1, min(n, kmax) + 1):
                words = reed_solomon_words(p, list(range(n)), k)
                assert len(set(words)) == p ** k
                d = min_distance(words)
                assert d == n - k + 1
                assert is_mds(p, n, k, d)
                assert puncture_is_injective(words, d)


def test_doubly_extended_rs_has_length_q_plus_1() -> None:
    for p in (5, 7):
        for k in range(1, 4):
            words = reed_solomon_words(p, list(range(p)), k, infinity=True)
            n = p + 1
            assert min_distance(words) == n - k + 1  # an MDS code of length q + 1


def test_binary_mds_codes_are_trivial() -> None:
    for n in range(2, 7):
        params = binary_mds_parameters(n)
        assert params == {(1, n), (n - 1, 2), (n, 1)}


def test_random_codes_never_beat_singleton() -> None:
    rng = random.Random(1964)
    for _ in range(300):
        q = rng.choice([2, 3])
        n = rng.randint(2, 6)
        d = rng.randint(1, n)
        allw = list(product(range(q), repeat=n))
        rng.shuffle(allw)
        code: list[tuple[int, ...]] = []
        for x in allw:
            if all(sum(a != b for a, b in zip(x, c)) >= d for c in code):
                code.append(x)
        assert len(code) <= singleton_bound(q, n, d)


def test_asymptotic_compare_with_hamming() -> None:
    # For q = 2 the Hamming bound is the stronger one; for large q the Singleton bound is.
    assert hamming_rate(0.2, 2) < singleton_rate(0.2)
    assert singleton_rate(0.4) < hamming_rate(0.4, 256)
    assert abs(singleton_rate(0.3) - 0.7) < 1e-12
