# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/palindrome-partition-backtracking/. The authors are listed in prov/8C52F0.jsonl.

import itertools
import random

from palindrome_partition_backtracking import (
    count_palindrome_partitions,
    palindrome_ends,
    palindrome_partitions,
)


def brute_partitions(s: str) -> list[list[str]]:
    """All partitions from all 2^(n-1) sets of cuts, kept if every piece is a palindrome."""
    n = len(s)
    if n == 0:
        return [[]]
    out = []
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i + 1 for i in range(n - 1) if mask >> i & 1] + [n]
        pieces = [s[a:b] for a, b in itertools.pairwise(cuts)]
        if all(p == p[::-1] for p in pieces):
            out.append(pieces)
    return out


def test_example() -> None:
    assert list(palindrome_partitions("abaab")) == [
        ["a", "b", "a", "a", "b"],
        ["a", "b", "aa", "b"],
        ["a", "baab"],
        ["aba", "a", "b"],
    ]
    assert palindrome_ends("abaab") == [[0, 2], [1, 4], [2, 3], [3], [4]]


def test_edges() -> None:
    assert list(palindrome_partitions("")) == [[]]
    assert list(palindrome_partitions("a")) == [["a"]]
    assert list(palindrome_partitions("abcabc")) == [list("abcabc")]
    for n in range(1, 12):
        parts = list(palindrome_partitions("a" * n))
        assert len(parts) == 2 ** (n - 1)
        assert count_palindrome_partitions("a" * n) == 2 ** (n - 1)
    assert count_palindrome_partitions("") == 1


def test_random_against_brute_force() -> None:
    rng = random.Random(8052)
    for trial in range(900):
        k = (1, 2, 3)[trial % 3]
        n = rng.randrange(0, 12)
        s = "".join(rng.choice("abc"[:k]) for _ in range(n))
        got = list(palindrome_partitions(s))
        want = brute_partitions(s)
        assert len(got) == len(want)
        assert sorted(got) == sorted(want), s
        assert count_palindrome_partitions(s) == len(want)
        for p in got:
            assert "".join(p) == s


def test_long_input_no_deep_recursion() -> None:
    s = "ab" * 600
    first = next(palindrome_partitions(s))
    assert len(first) == len(s)
