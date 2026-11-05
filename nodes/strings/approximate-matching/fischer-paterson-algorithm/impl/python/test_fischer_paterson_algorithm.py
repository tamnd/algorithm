# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fischer-paterson-algorithm/. The authors are listed in prov/PNQWEP.jsonl.

import random

import pytest
from fischer_paterson_algorithm import MOD, hamming_distances, k_mismatch_starts, ntt


def brute(pattern: str, text: str) -> list[int]:
    m = len(pattern)
    return [
        sum(a != b for a, b in zip(pattern, text[i:i + m]))
        for i in range(len(text) - m + 1)
    ]


def test_examples() -> None:
    assert hamming_distances("abc", "abxabcbc") == [1, 3, 3, 0, 3, 1]
    assert hamming_distances("ACGTA", "ACGAAACGTTACCTA") == [1, 4, 5, 4, 4, 1, 3, 5, 5, 5, 1]
    assert k_mismatch_starts("abc", "abxabcbc", 1) == [0, 3, 5]


def test_edges() -> None:
    assert hamming_distances("", "") == [0]
    assert hamming_distances("", "ab") == [0, 0, 0]
    assert hamming_distances("a", "") == []
    assert hamming_distances("abc", "ab") == []
    assert hamming_distances("ab", "ab") == [0]
    assert hamming_distances("ab", "xyzw") == [2, 2, 2]
    assert k_mismatch_starts("ab", "xyzw", 0) == []
    with pytest.raises(ValueError):
        k_mismatch_starts("a", "a", -1)


def test_ntt_round_trip_and_product() -> None:
    rng = random.Random(5)
    for size in (1, 2, 4, 8, 32):
        a = [rng.randrange(100) for _ in range(size // 2 or 1)] + [0] * (size - (size // 2 or 1))
        b = [rng.randrange(100) for _ in range(size // 2 or 1)] + [0] * (size - (size // 2 or 1))
        want = [0] * size
        for i, u in enumerate(a):
            for j, v in enumerate(b):
                if i + j < size:
                    want[i + j] += u * v
        fa, fb = a[:], b[:]
        ntt(fa, False)
        ntt(fb, False)
        prod = [u * v % MOD for u, v in zip(fa, fb)]
        ntt(prod, True)
        assert prod == want


def test_random_against_brute_force() -> None:
    rng = random.Random(1974)
    for alphabet in ("ab", "acgt"):
        for _ in range(700):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 9)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 30)))
            assert hamming_distances(p, t) == brute(p, t), (p, t)
            k = rng.randint(0, 5)
            assert k_mismatch_starts(p, t, k) == [i for i, d in enumerate(brute(p, t)) if d <= k]


def test_text_symbols_outside_the_pattern() -> None:
    rng = random.Random(8)
    for _ in range(300):
        p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
        t = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 25)))
        assert hamming_distances(p, t) == brute(p, t)
