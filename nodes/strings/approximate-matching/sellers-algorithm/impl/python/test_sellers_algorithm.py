# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sellers-algorithm/. The authors are listed in prov/TZXPTF.jsonl.

import random

import pytest
from sellers_algorithm import last_row, sellers


def edit_distance(a: str, b: str) -> int:
    d = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d[len(a)][len(b)]


def brute(pattern: str, text: str, k: int) -> list[int]:
    return [
        j for j in range(len(text) + 1)
        if min(edit_distance(pattern, text[i:j]) for i in range(j + 1)) <= k
    ]


def test_example() -> None:
    assert last_row("survey", "surgery") == [6, 5, 4, 3, 3, 2, 2, 2]
    assert sellers("survey", "surgery", 2) == [5, 6, 7]
    assert sellers("survey", "surgery", 1) == []
    assert sellers("abc", "abxabcbc", 1) == [2, 3, 5, 6, 7, 8]


def test_edges() -> None:
    assert sellers("", "", 0) == [0]
    assert sellers("", "ab", 0) == [0, 1, 2]
    assert sellers("ab", "", 1) == []
    assert sellers("ab", "", 2) == [0]
    assert sellers("abc", "xxabcxx", 0) == [5]
    assert sellers("ab", "xyz", 5) == [0, 1, 2, 3]
    with pytest.raises(ValueError):
        sellers("a", "a", -1)


def test_random_against_brute_force() -> None:
    rng = random.Random(1980)
    for alphabet in ("ab", "acgt"):
        for _ in range(400):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            k = rng.randint(0, 4)
            assert sellers(p, t, k) == brute(p, t, k)
