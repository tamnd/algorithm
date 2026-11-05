# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/naive-string-matching/. The authors are listed in prov/NM14X8.jsonl.

import random

from naive_string_matching import naive_string_matching


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def test_example() -> None:
    assert naive_string_matching("abaababaab", "abab") == [3]
    assert naive_string_matching("abracadabra", "abra") == [0, 7]


def test_edges() -> None:
    assert naive_string_matching("abc", "") == [0, 1, 2, 3]
    assert naive_string_matching("", "") == [0]
    assert naive_string_matching("", "a") == []
    assert naive_string_matching("ab", "abc") == []
    assert naive_string_matching("abc", "abc") == [0]
    assert naive_string_matching("a" * 10, "a" * 4) == list(range(7))
    assert naive_string_matching("a" * 10, "aaab") == []


def test_last_shift() -> None:
    # the loop bound must include s = n - m
    assert naive_string_matching("xxab", "ab") == [2]


def test_lists() -> None:
    assert naive_string_matching([1, 2, 1, 2, 1], [1, 2, 1]) == [0, 2]


def test_random_against_oracle() -> None:
    rng = random.Random(4101)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 30)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            assert naive_string_matching(t, p) == oracle(t, p)


def test_periodic() -> None:
    for n in range(12):
        for m in range(n + 3):
            assert naive_string_matching("a" * n, "a" * m) == (list(range(n - m + 1)) if m <= n else [])
