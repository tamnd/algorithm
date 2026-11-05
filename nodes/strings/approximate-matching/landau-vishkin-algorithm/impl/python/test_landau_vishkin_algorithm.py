# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/landau-vishkin-algorithm/. The authors are listed in prov/2PT2TT.jsonl.

import random

import pytest
from landau_vishkin_algorithm import LCE, diagonal_table, landau_vishkin


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


def sellers_table(p: str, t: str) -> list[list[int]]:
    c = [[i if j == 0 else 0 for j in range(len(t) + 1)] for i in range(len(p) + 1)]
    for i in range(1, len(p) + 1):
        for j in range(1, len(t) + 1):
            c[i][j] = min(c[i - 1][j] + 1, c[i][j - 1] + 1, c[i - 1][j - 1] + (p[i - 1] != t[j - 1]))
    return c


def test_example() -> None:
    assert landau_vishkin("GATAA", "CAGATAAGAGAA", 1) == [6, 7, 8, 12]
    assert landau_vishkin("GATAA", "CAGATAAGAGAA", 0) == [7]
    assert landau_vishkin("survey", "surgery", 2) == [5, 6, 7]


def test_edges() -> None:
    assert landau_vishkin("", "", 0) == [0]
    assert landau_vishkin("", "ab", 0) == [0, 1, 2]
    assert landau_vishkin("ab", "", 1) == []
    assert landau_vishkin("ab", "", 2) == [0]
    assert landau_vishkin("ab", "xyz", 5) == [0, 1, 2, 3]
    with pytest.raises(ValueError):
        landau_vishkin("a", "a", -1)


def test_lce() -> None:
    rng = random.Random(7)
    for _ in range(200):
        a = "".join(rng.choice("ab") for _ in range(rng.randint(1, 10)))
        b = "".join(rng.choice("ab") for _ in range(rng.randint(1, 10)))
        s = LCE(a, b)
        for i in range(len(a)):
            for j in range(len(b)):
                q = 0
                while i + q < len(a) and j + q < len(b) and a[i + q] == b[j + q]:
                    q += 1
                assert s.query(i, j) == q


def test_table_is_furthest_row() -> None:
    rng = random.Random(1989)
    for alphabet in ("ab", "acgt"):
        for _ in range(150):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 10)))
            k = rng.randint(0, 4)
            c = sellers_table(p, t)
            table = diagonal_table(p, t, k)
            for e in range(k + 1):
                for d in range(-len(p), len(t) + 1):
                    rows = [i for i in range(len(p) + 1) if 0 <= i + d <= len(t) and c[i][i + d] <= e]
                    assert table.get((d, e)) == (max(rows) if rows else None)


def test_random_against_brute_force() -> None:
    rng = random.Random(1986)
    for alphabet in ("ab", "acgt"):
        for _ in range(400):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            k = rng.randint(0, 4)
            assert landau_vishkin(p, t, k) == brute(p, t, k)
