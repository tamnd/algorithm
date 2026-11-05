# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quick-search/. The authors are listed in prov/GYWS8F.jsonl.

import random

from quick_search import quick_search, quick_search_shift


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def test_example() -> None:
    assert quick_search_shift("gcagagag") == {"g": 1, "c": 7, "a": 2}
    assert quick_search("gcatcgcagagagtatacagtacg", "gcagagag") == [5]


def test_window_at_the_end() -> None:
    # The last window has no character after it; reading T[n] would fail.
    assert quick_search("xxab", "ab") == [2]
    assert quick_search("ab", "ab") == [0]


def test_edges() -> None:
    assert quick_search("abc", "") == [0, 1, 2, 3]
    assert quick_search("", "") == [0]
    assert quick_search("", "a") == []
    assert quick_search("ab", "abc") == []
    assert quick_search("a" * 10, "a" * 4) == list(range(7))
    assert quick_search("a" * 10, "aaab") == []


def test_random_against_oracle() -> None:
    rng = random.Random(1990)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert quick_search(t, p) == oracle(t, p)
