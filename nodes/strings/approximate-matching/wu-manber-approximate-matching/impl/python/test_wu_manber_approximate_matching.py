# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wu-manber-approximate-matching/. The authors are listed in prov/QT4WGM.jsonl.

import random

import pytest
from wu_manber_approximate_matching import wu_manber, wu_manber_states


def edit_distance(a: str, b: str) -> int:
    d = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d[len(a)][len(b)]


def sellers_table(p: str, t: str) -> list[list[int]]:
    c = [[i if j == 0 else 0 for j in range(len(t) + 1)] for i in range(len(p) + 1)]
    for i in range(1, len(p) + 1):
        for j in range(1, len(t) + 1):
            c[i][j] = min(c[i - 1][j] + 1, c[i][j - 1] + 1, c[i - 1][j - 1] + (p[i - 1] != t[j - 1]))
    return c


def brute(pattern: str, text: str, k: int) -> list[int]:
    return [
        j for j in range(len(text) + 1)
        if min(edit_distance(pattern, text[h:j]) for h in range(j + 1)) <= k
    ]


def test_example() -> None:
    assert wu_manber("GATAA", "CAGATAAGAGAA", 1) == [6, 7, 8, 12]
    assert wu_manber("GATAA", "CAGATAAGAGAA", 0) == [7]
    assert wu_manber("survey", "surgery", 2) == [5, 6, 7]


def test_edges() -> None:
    assert wu_manber("", "", 0) == [0]
    assert wu_manber("", "ab", 0) == [0, 1, 2]
    assert wu_manber("ab", "", 1) == []
    assert wu_manber("ab", "", 2) == [0]
    assert wu_manber("ab", "xyz", 5) == [0, 1, 2, 3]
    with pytest.raises(ValueError):
        wu_manber("a", "a", -1)


def test_vectors_are_the_active_sets() -> None:
    rng = random.Random(1992)
    for alphabet in ("ab", "acgt"):
        for _ in range(200):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 10)))
            k = rng.randint(0, 4)
            c = sellers_table(p, t)
            for j, (_, r) in enumerate(wu_manber_states(p, t, k)):
                for e in range(k + 1):
                    want = sum(1 << (i - 1) for i in range(1, len(p) + 1) if c[i][j] <= e)
                    assert r[e] == want


def test_random_against_brute_force() -> None:
    rng = random.Random(35)
    for alphabet in ("ab", "acgt"):
        for _ in range(400):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            k = rng.randint(0, 4)
            assert wu_manber(p, t, k) == brute(p, t, k)
