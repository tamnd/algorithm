# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/galil-park-algorithm/. The authors are listed in prov/0F6W2E.jsonl.

import random

import pytest
from galil_park_algorithm import galil_park, pattern_extensions


def edit_distance(a: str, b: str) -> int:
    d = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d[len(a)][len(b)]


def brute(pattern: str, text: str, k: int) -> list[int]:
    return [
        j for j in range(len(text) + 1)
        if min(edit_distance(pattern, text[h:j]) for h in range(j + 1)) <= k
    ]


def test_example() -> None:
    assert galil_park("GATAA", "CAGATAAGAGAA", 1) == [6, 7, 8, 12]
    assert galil_park("GATAA", "CAGATAAGAGAA", 0) == [7]
    assert galil_park("survey", "surgery", 2) == [5, 6, 7]


def test_edges() -> None:
    assert galil_park("", "", 0) == [0]
    assert galil_park("", "ab", 0) == [0, 1, 2]
    assert galil_park("ab", "", 1) == []
    assert galil_park("ab", "", 2) == [0]
    assert galil_park("ab", "xyz", 5) == [0, 1, 2, 3]
    with pytest.raises(ValueError):
        galil_park("a", "a", -1)


def test_pattern_extensions() -> None:
    rng = random.Random(5)
    for _ in range(200):
        p = "".join(rng.choice("ab") for _ in range(rng.randint(0, 9)))
        pp = pattern_extensions(p)
        for a in range(len(p) + 1):
            for b in range(len(p) + 1):
                q = 0
                while a + q < len(p) and b + q < len(p) and p[a + q] == p[b + q]:
                    q += 1
                assert pp[a][b] == q


def test_random_against_brute_force() -> None:
    rng = random.Random(1990)
    for alphabet in ("ab", "acgt"):
        for _ in range(500):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            k = rng.randint(0, 4)
            assert galil_park(p, t, k) == brute(p, t, k)


def test_long_random_against_brute_force() -> None:
    rng = random.Random(89)
    for alphabet in ("ab", "acgt"):
        for _ in range(60):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(5, 12)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(20, 40)))
            k = rng.randint(0, 3)
            assert galil_park(p, t, k) == brute(p, t, k)
