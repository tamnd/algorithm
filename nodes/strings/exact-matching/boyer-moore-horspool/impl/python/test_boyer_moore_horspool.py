# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-moore-horspool/. The authors are listed in prov/RFB4V2.jsonl.

import random

from boyer_moore_horspool import boyer_moore_horspool, horspool_shift


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def test_example() -> None:
    assert horspool_shift("gcagagag") == {"g": 2, "c": 6, "a": 1}
    assert boyer_moore_horspool("gcatcgcagagagtatacagtacg", "gcagagag") == [5]


def test_last_character_excluded() -> None:
    # The last pattern character must not set its own shift to 0.
    assert horspool_shift("ab") == {"a": 1}
    assert boyer_moore_horspool("abab", "ab") == [0, 2]


def test_edges() -> None:
    assert boyer_moore_horspool("abc", "") == [0, 1, 2, 3]
    assert boyer_moore_horspool("", "") == [0]
    assert boyer_moore_horspool("", "a") == []
    assert boyer_moore_horspool("ab", "abc") == []
    assert boyer_moore_horspool("a" * 10, "a" * 4) == list(range(7))
    assert boyer_moore_horspool("a" * 10, "baaa") == []


def test_random_against_oracle() -> None:
    rng = random.Random(1980)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert boyer_moore_horspool(t, p) == oracle(t, p)
