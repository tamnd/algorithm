# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-pratt/. The authors are listed in prov/SGQC43.jsonl.

import random

from morris_pratt import compute_prefix_function, morris_pratt


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def border_oracle(p: str) -> list[int]:
    return [max(k for k in range(q + 1) if p[:k] == p[q + 1 - k : q + 1]) for q in range(len(p))]


def test_example() -> None:
    assert compute_prefix_function("abacabab") == [0, 0, 1, 0, 1, 2, 3, 2]
    assert morris_pratt("abacabcabacababa", "abacabab") == [7]


def test_edges() -> None:
    assert morris_pratt("abc", "") == [0, 1, 2, 3]
    assert morris_pratt("", "") == [0]
    assert morris_pratt("", "a") == []
    assert morris_pratt("ab", "abc") == []
    assert morris_pratt("a" * 10, "a" * 4) == list(range(7))
    assert morris_pratt("a" * 10, "aaab") == []


def test_overlap_after_match() -> None:
    assert morris_pratt("abababab", "abab") == [0, 2, 4]
    assert morris_pratt("aaaaa", "aa") == [0, 1, 2, 3]


def test_prefix_function_against_definition() -> None:
    rng = random.Random(31)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(300):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 12)))
            assert compute_prefix_function(p) == border_oracle(p)


def test_random_against_oracle() -> None:
    rng = random.Random(1970)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert morris_pratt(t, p) == oracle(t, p)
