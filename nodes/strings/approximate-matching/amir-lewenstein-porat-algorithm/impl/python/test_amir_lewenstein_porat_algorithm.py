# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amir-lewenstein-porat-algorithm/. The authors are listed in prov/EGHY1F.jsonl.

import random

import pytest
from amir_lewenstein_porat_algorithm import alp_k_mismatch, case_of, parameters


def brute(pattern: str, text: str, k: int) -> list[int]:
    m = len(pattern)
    return [
        i for i in range(len(text) - m + 1)
        if sum(pattern[q] != text[i + q] for q in range(m)) <= k
    ]


def test_example() -> None:
    assert alp_k_mismatch("ACGTA", "ACGAAACGTTACCTA", 1) == [0, 5, 10]
    assert alp_k_mismatch("abc", "abxabcbc", 1) == [0, 3, 5]
    assert alp_k_mismatch("abc", "abxabcbc", 0) == [3]


def test_edges() -> None:
    assert alp_k_mismatch("", "", 0) == [0]
    assert alp_k_mismatch("", "ab", 0) == [0, 1, 2]
    assert alp_k_mismatch("a", "", 0) == []
    assert alp_k_mismatch("ab", "ab", 5) == [0]
    assert alp_k_mismatch("aaaa", "aaaaaa", 0) == [0, 1, 2]
    with pytest.raises(ValueError):
        alp_k_mismatch("a", "a", -1)


def test_parameters() -> None:
    assert parameters(8, 1) == (2, 1)
    assert parameters(8, 4) == (4, 2)
    assert parameters(1, 0) == (1, 0)
    for m in range(1, 200):
        for k in range(0, m):
            f, g = parameters(m, k)
            assert f >= 1 and g * f >= 2 * k


@pytest.mark.parametrize("alphabet", ["ab", "acgt"])
def test_random_against_brute_force(alphabet: str) -> None:
    rng = random.Random(20241106 + len(alphabet))
    seen = {"A": 0, "B": 0}
    for _ in range(1500):
        n = rng.randint(0, 40)
        m = rng.randint(0, 14)
        text = "".join(rng.choice(alphabet) for _ in range(n))
        pattern = "".join(rng.choice(alphabet) for _ in range(m))
        k = rng.randint(0, m + 1)
        if m <= n and k < m:
            seen[case_of(pattern, k)] += 1
        assert alp_k_mismatch(pattern, text, k) == brute(pattern, text, k)
    assert seen["A"] > 50 and seen["B"] > 50


def test_case_b_long_patterns() -> None:
    rng = random.Random(7)
    for _ in range(300):
        m = rng.randint(10, 40)
        k = rng.randint(m // 2, m - 1)
        sigma = rng.choice(["ab", "acgt", "abcdefgh"])
        pattern = "".join(rng.choice(sigma) for _ in range(m))
        text = "".join(rng.choice(sigma) for _ in range(rng.randint(m, 3 * m + 5)))
        if rng.random() < 0.5:
            i = rng.randint(0, len(text) - m)
            text = text[:i] + pattern + text[i + m:]
        assert alp_k_mismatch(pattern, text, k) == brute(pattern, text, k)
