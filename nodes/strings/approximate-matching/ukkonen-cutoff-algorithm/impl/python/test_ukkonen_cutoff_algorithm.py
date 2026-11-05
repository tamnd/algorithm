# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ukkonen-cutoff-algorithm/. The authors are listed in prov/V58QHM.jsonl.

import random

import pytest
from ukkonen_cutoff_algorithm import ukkonen_cutoff, ukkonen_cutoff_trace


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
    ends, lact, cells = ukkonen_cutoff_trace("survey", "surgery", 2)
    assert ends == [5, 6, 7]
    assert lact == [2, 3, 4, 5, 5, 6, 6, 6]
    assert ukkonen_cutoff("survey", "surgery", 1) == []


def test_edges() -> None:
    assert ukkonen_cutoff("", "", 0) == [0]
    assert ukkonen_cutoff("", "ab", 0) == [0, 1, 2]
    assert ukkonen_cutoff("ab", "", 1) == []
    assert ukkonen_cutoff("ab", "", 2) == [0]
    assert ukkonen_cutoff("ab", "xyz", 5) == [0, 1, 2, 3]
    assert ukkonen_cutoff("abc", "xxabcxx", 0) == [5]
    with pytest.raises(ValueError):
        ukkonen_cutoff("a", "a", -1)


def test_last_active_row() -> None:
    rng = random.Random(1985)
    for alphabet in ("ab", "acgt"):
        for _ in range(300):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            k = rng.randint(0, 4)
            c = sellers_table(p, t)
            _, lact, _ = ukkonen_cutoff_trace(p, t, k)
            for j in range(len(t) + 1):
                assert lact[j] == max(i for i in range(len(p) + 1) if c[i][j] <= k)


def test_random_against_brute_force() -> None:
    rng = random.Random(132)
    for alphabet in ("ab", "acgt"):
        for _ in range(400):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            k = rng.randint(0, 4)
            assert ukkonen_cutoff(p, t, k) == brute(p, t, k)
