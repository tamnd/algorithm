# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-algorithm/. The authors are listed in prov/7JPXK4.jsonl.

import random

from z_algorithm import z_array, z_search


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def z_oracle(s: str) -> list[int]:
    out = []
    for k in range(len(s)):
        j = 0
        while k + j < len(s) and s[j] == s[k + j]:
            j += 1
        out.append(j)
    return out


def test_example() -> None:
    assert z_array("aabxaabxay") == [10, 1, 0, 0, 5, 1, 0, 0, 1, 0]
    assert z_array("aab$baabaaab") == [12, 1, 0, 0, 0, 3, 1, 0, 2, 3, 1, 0]
    assert z_search("baabaaab", "aab") == [1, 5]


def test_edges() -> None:
    assert z_array("") == []
    assert z_array("a") == [1]
    assert z_array("aaaa") == [4, 3, 2, 1]
    assert z_search("abc", "") == [0, 1, 2, 3]
    assert z_search("", "") == [0]
    assert z_search("", "a") == []
    assert z_search("ab", "abc") == []
    assert z_search("a" * 10, "a" * 4) == list(range(7))
    assert z_search("a" * 10, "aaab") == []


def test_separator_not_matched() -> None:
    # Without a separator the value at a text position could exceed m.
    assert z_search("aaaa", "aa") == [0, 1, 2]


def test_z_array_against_definition() -> None:
    rng = random.Random(7)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(400):
            s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 30)))
            assert z_array(s) == z_oracle(s)


def test_random_against_oracle() -> None:
    rng = random.Random(1997)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert z_search(t, p) == oracle(t, p)
