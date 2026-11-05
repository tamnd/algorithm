# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shift-or/. The authors are listed in prov/D9WFTK.jsonl.

import random

from shift_or import shift_or, shift_or_masks


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def test_example() -> None:
    masks, ones = shift_or_masks("abab")
    assert ones == 0b1111
    assert masks == {"a": 0b1010, "b": 0b0101}
    assert shift_or("aababab", "abab") == [1, 3]


def test_long_pattern() -> None:
    # Longer than a 64-bit word: Python integers grow as needed.
    p = "ab" * 50 + "c"
    t = "ab" * 120 + "c" + "ab" * 50 + "c"
    assert shift_or(t, p) == oracle(t, p)


def test_edges() -> None:
    assert shift_or("abc", "") == [0, 1, 2, 3]
    assert shift_or("", "") == [0]
    assert shift_or("", "a") == []
    assert shift_or("ab", "abc") == []
    assert shift_or("a" * 10, "a" * 4) == list(range(7))
    assert shift_or("a" * 10, "aaab") == []
    assert shift_or("xyz", "y") == [1]


def test_random_against_oracle() -> None:
    rng = random.Random(1992)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert shift_or(t, p) == oracle(t, p)
