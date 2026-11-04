# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz-index/. The authors are listed in prov/TGNZ8J.jsonl.

import random

import pytest

from lz_index import LZIndex


def occurrences(t: str, p: str) -> list[int]:
    return [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)]


def test_example() -> None:
    z = LZIndex("abababab")
    z.check_invariant()
    assert [z.phrase(j) for j in range(1, z.phrases + 1)] == ["a", "b", "ab", "aba", "b\0"]
    assert z.start[1:] == [0, 1, 2, 4, 7]
    assert z.ending_with("aba") == [4]
    assert sorted(z.ending_with("a")) == [1, 4] and z.starting_with("ba") == []
    assert sorted(z.starting_with("a")) == [1, 3, 4]
    assert z.search("aba") == [0, 2, 4]
    assert z.search("bab") == [1, 3, 5]
    assert z.search("abababab") == [0]
    assert z.search("bb") == []


def test_edges() -> None:
    z = LZIndex("")
    z.check_invariant()
    assert z.phrases == 1 and z.search("a") == []
    z = LZIndex("aaaaaaaaaaaaaaaaaaaa")
    z.check_invariant()
    assert z.search("aaa") == list(range(18))
    with pytest.raises(ValueError):
        z.search("")
    with pytest.raises(ValueError):
        LZIndex("a\0")


def test_random_against_scan() -> None:
    rng = random.Random(2004)
    for _ in range(600):
        alpha = rng.choice(["ab", "abc"])
        t = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 40)))
        z = LZIndex(t)
        z.check_invariant()
        assert "".join(z.phrase(j) for j in range(1, z.phrases + 1)) == t + "\0"
        for _ in range(4):
            if t and rng.random() < 0.7:
                i = rng.randrange(len(t))
                p = t[i: i + rng.randint(1, 8)]
            else:
                p = "".join(rng.choice(alpha) for _ in range(rng.randint(1, 5)))
            assert z.search(p) == occurrences(t, p)
