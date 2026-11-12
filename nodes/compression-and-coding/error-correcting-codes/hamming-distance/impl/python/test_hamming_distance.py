# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamming-distance/. The authors are listed in prov/ZXVGP4.jsonl.

import itertools
import random

import pytest

from hamming_distance import ball_volume, hamming_distance, hamming_distance_bits, sphere_size


def test_page_examples() -> None:
    assert hamming_distance("karolin", "kathrin") == 3
    assert hamming_distance("1011101", "1001001") == 2
    assert hamming_distance_bits(0b1011101, 0b1001001) == 2
    assert hamming_distance([2, 1, 7, 3], [2, 2, 3, 3]) == 2
    assert hamming_distance("", "") == 0


def test_different_lengths_are_rejected() -> None:
    with pytest.raises(ValueError):
        hamming_distance("abc", "ab")
    with pytest.raises(ValueError):
        hamming_distance_bits(-1, 3)


def test_metric_axioms_exhaustive() -> None:
    # every triple of words of length 3 over a ternary alphabet: 27^3 triples
    words = list(itertools.product(range(3), repeat=3))
    for x in words:
        assert hamming_distance(x, x) == 0
        for y in words:
            dxy = hamming_distance(x, y)
            assert dxy == hamming_distance(y, x)
            assert (dxy == 0) == (x == y)
            for z in words:
                assert hamming_distance(x, z) <= dxy + hamming_distance(y, z)


def test_translation_invariance_mod_q() -> None:
    # over Z_q (and GF(q)) the distance is the weight of the difference
    q, n = 5, 4
    rng = random.Random(11)
    for _ in range(500):
        x = [rng.randrange(q) for _ in range(n)]
        y = [rng.randrange(q) for _ in range(n)]
        z = [rng.randrange(q) for _ in range(n)]
        diff = [(a - b) % q for a, b in zip(x, y)]
        assert hamming_distance(x, y) == sum(1 for v in diff if v)
        xz = [(a + c) % q for a, c in zip(x, z)]
        yz = [(b + c) % q for b, c in zip(y, z)]
        assert hamming_distance(xz, yz) == hamming_distance(x, y)


def test_bits_against_sequences_random() -> None:
    rng = random.Random(2024)
    for _ in range(1000):
        n = rng.randrange(0, 70)
        a, b = rng.getrandbits(n) if n else 0, rng.getrandbits(n) if n else 0
        xa = [(a >> i) & 1 for i in range(n)]
        xb = [(b >> i) & 1 for i in range(n)]
        assert hamming_distance_bits(a, b) == hamming_distance(xa, xb)


def test_ball_volume_brute_force() -> None:
    for q in (2, 3):
        for n in range(0, 6):
            center = (0,) * n
            counts = [0] * (n + 1)
            for w in itertools.product(range(q), repeat=n):
                counts[hamming_distance(center, w)] += 1
            for i in range(n + 1):
                assert counts[i] == sphere_size(n, i, q)
            for r in range(n + 2):
                assert ball_volume(n, r, q) == sum(counts[: r + 1])
    assert ball_volume(7, 1, 2) == 8 and ball_volume(23, 3, 2) == 2048
