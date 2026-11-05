# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-trie/. The authors are listed in prov/J5APVR.jsonl.

import random

import pytest

from suffix_trie import SuffixTrie


def naive_occ(s: str, p: str) -> list[int]:
    return [i for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p]


def test_example() -> None:
    t = SuffixTrie("abab")
    t.check_invariant()
    assert t.node_count() == 8
    assert t.count("ab") == 2
    assert t.occurrences("ab") == [0, 2]
    assert t.occurrences("b") == [1, 3]
    assert t.occurrences("bab") == [1]
    assert not t.contains("aa")
    assert t.count("aa") == 0
    assert t.occurrences("abb") == []


def test_edges() -> None:
    t = SuffixTrie("")
    t.check_invariant()
    assert t.node_count() == 1
    assert t.contains("")
    assert not t.contains("a")
    t = SuffixTrie("a")
    t.check_invariant()
    assert t.occurrences("a") == [0]
    with pytest.raises(ValueError):
        t.count("")


def test_sizes() -> None:
    assert SuffixTrie("a" * 30).node_count() == 31
    k = 10
    assert SuffixTrie("a" * k + "b" * k).node_count() == (k + 1) ** 2
    assert SuffixTrie("abcdefgh").node_count() == 8 * 9 // 2 + 1
    assert SuffixTrie("ab" * 8).node_count() == 1 + 2 * 16 - 1
    assert SuffixTrie([3, 1, 4, 1, 5]).occurrences([1]) == [1, 3]


def test_random_against_naive() -> None:
    rng = random.Random(4417)
    for trial in range(600):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 14)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 50 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2)])
        t = SuffixTrie(s)
        t.check_invariant()
        for _ in range(8):
            p = "".join(rng.choice(sigma) for _ in range(rng.randint(1, 5)))
            if s and rng.random() < 0.5:
                i = rng.randrange(n)
                p = s[i:rng.randint(i + 1, n)]
            want = naive_occ(s, p)
            assert t.contains(p) == bool(want)
            assert t.count(p) == len(want)
            assert t.occurrences(p) == want
