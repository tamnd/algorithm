# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/palindromic-tree/. The authors are listed in prov/6DMXQ2.jsonl.

import random
from collections import Counter

from palindromic_tree import EMPTY, IMAG, PalindromicTree


def brute_occurrences(s: str) -> Counter[str]:
    """Every palindromic occurrence s[a..b-1], counted by its string."""
    return Counter(s[a:b] for a in range(len(s)) for b in range(a + 1, len(s) + 1) if s[a:b] == s[a:b][::-1])


def test_example() -> None:
    t = PalindromicTree("eertree")
    rows = [("".join(t.palindrome(v)), t.length[v], t.link[v], t.end[v]) for v in range(2, len(t.length))]
    assert rows == [
        ("e", 1, EMPTY, 0),
        ("ee", 2, 2, 1),
        ("r", 1, EMPTY, 2),
        ("t", 1, EMPTY, 3),
        ("rtr", 3, 4, 4),
        ("ertre", 5, 2, 5),
        ("eertree", 7, 3, 6),
    ]
    assert t.size() == 7
    t.check_invariant()


def test_edges() -> None:
    t = PalindromicTree("")
    assert t.size() == 0 and t.last == EMPTY
    t.check_invariant()
    for n in range(1, 25):
        t = PalindromicTree("a" * n)
        assert t.size() == n
        assert t.depth[t.last] == n
        t.check_invariant()
    t = PalindromicTree("abc" * 8)
    assert t.size() == 3
    t.check_invariant()
    t = PalindromicTree([1, 2, 1, 1])
    assert t.size() == 4
    assert t.link[2] == EMPTY and t.link[IMAG] == IMAG


def test_random_against_brute_force() -> None:
    rng = random.Random(6202)
    for trial in range(900):
        k = (1, 2, 3)[trial % 3]
        n = rng.randrange(0, 16)
        s = "".join(rng.choice("abc"[:k]) for _ in range(n))
        t = PalindromicTree()
        total = 0
        for i, c in enumerate(s):
            before = t.size()
            new = t.add(c)
            assert new == (t.size() == before + 1)
            total += t.depth[t.last]
            want_new = len(brute_occurrences(s[: i + 1])) - len(brute_occurrences(s[:i]))
            assert int(new) == want_new
        t.check_invariant()
        want = brute_occurrences(s)
        assert t.size() == len(want)
        assert total == sum(want.values())
        occ = t.occurrences()
        for v in range(2, len(t.length)):
            assert occ[v] == want["".join(t.palindrome(v))]


def test_long_input() -> None:
    rng = random.Random(9)
    s = "".join(rng.choice("ab") for _ in range(20000))
    t = PalindromicTree(s)
    assert t.size() <= len(s)
    assert len(t.length) == t.size() + 2
    t2 = PalindromicTree("a" * 20000)
    assert t2.size() == 20000 and t2.depth[t2.last] == 20000
