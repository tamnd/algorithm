# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/myers-bit-parallel-algorithm/. The authors are listed in prov/MXPHKN.jsonl.

import random

import pytest
from myers_bit_parallel_algorithm import edit_distance, myers, myers_columns


def lev(a: str, b: str) -> int:
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
        if min(lev(pattern, text[h:j]) for h in range(j + 1)) <= k
    ]


def test_example() -> None:
    assert myers("GATAA", "CAGATAAGAGAA", 1) == [6, 7, 8, 12]
    assert myers("GATAA", "CAGATAAGAGAA", 0) == [7]
    assert myers("survey", "surgery", 2) == [5, 6, 7]
    assert [s for _, s, _, _ in myers_columns("survey", "surgery")] == [6, 5, 4, 3, 3, 2, 2, 2]
    assert edit_distance("kitten", "sitting") == 3


def test_edges() -> None:
    assert myers("", "", 0) == [0]
    assert myers("", "ab", 0) == [0, 1, 2]
    assert myers("ab", "", 1) == []
    assert myers("ab", "", 2) == [0]
    assert myers("ab", "xyz", 5) == [0, 1, 2, 3]
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "") == 3


def test_vectors_are_the_column_differences() -> None:
    rng = random.Random(1999)
    for alphabet in ("ab", "acgt"):
        for _ in range(200):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 8)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 10)))
            c = sellers_table(p, t)
            for j, score, pv, mv in myers_columns(p, t):
                assert score == c[len(p)][j]
                for i in range(1, len(p) + 1):
                    v = c[i][j] - c[i - 1][j]
                    assert (pv >> (i - 1)) & 1 == (v == 1)
                    assert (mv >> (i - 1)) & 1 == (v == -1)


def test_random_against_brute_force() -> None:
    rng = random.Random(2001)
    for alphabet in ("ab", "acgt"):
        for _ in range(400):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            k = rng.randint(0, 4)
            assert myers(p, t, k) == brute(p, t, k)
            assert edit_distance(p, t) == lev(p, t)
