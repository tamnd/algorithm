# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/palindrome-partition-dp/. The authors are listed in prov/3EX5K9.jsonl.

import itertools
import random

from palindrome_partition_dp import (
    min_cuts,
    min_palindrome_partition,
    palindromic_length_linear_space,
)


def brute_min(s: str) -> int:
    """Least number of pieces over all 2^(n-1) sets of cuts with only palindromic pieces."""
    n = len(s)
    if n == 0:
        return 0
    best = n
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i + 1 for i in range(n - 1) if mask >> i & 1] + [n]
        if all(s[a:b] == s[a:b][::-1] for a, b in itertools.pairwise(cuts)):
            best = min(best, len(cuts) - 1)
    return best


def check(s: str, k: int, pieces: list[tuple[int, int]]) -> None:
    assert len(pieces) == k
    pos = 0
    for j, i in pieces:
        assert j == pos and i >= j
        assert s[j : i + 1] == s[j : i + 1][::-1]
        pos = i + 1
    assert pos == len(s)


def test_example() -> None:
    assert min_palindrome_partition("banana") == (2, [(0, 0), (1, 5)])
    assert min_palindrome_partition("abaab") == (2, [(0, 0), (1, 4)])
    assert min_cuts("abaab") == 1
    assert min_palindrome_partition("aaba") == (2, [(0, 0), (1, 3)])


def test_edges() -> None:
    assert min_palindrome_partition("") == (0, [])
    assert min_cuts("") == 0
    assert palindromic_length_linear_space("") == 0
    assert min_palindrome_partition("a") == (1, [(0, 0)])
    for n in range(1, 30):
        assert min_palindrome_partition("a" * n) == (1, [(0, n - 1)])
        assert palindromic_length_linear_space("a" * n) == 1
    s = "abc" * 7
    assert min_palindrome_partition(s)[0] == len(s)
    assert palindromic_length_linear_space(s) == len(s)
    assert min_palindrome_partition([1, 2, 1])[0] == 1


def test_random_against_brute_force() -> None:
    rng = random.Random(3509)
    for trial in range(900):
        k = (1, 2, 3)[trial % 3]
        n = rng.randrange(0, 13)
        s = "".join(rng.choice("abc"[:k]) for _ in range(n))
        want = brute_min(s)
        got, pieces = min_palindrome_partition(s)
        assert got == want, s
        check(s, got, pieces)
        assert palindromic_length_linear_space(s) == want
        assert min_cuts(s) == max(want - 1, 0)


def test_longer_inputs_agree() -> None:
    rng = random.Random(77)
    for k in (2, 3):
        s = "".join(rng.choice("abc"[:k]) for _ in range(400))
        got, pieces = min_palindrome_partition(s)
        check(s, got, pieces)
        assert got == palindromic_length_linear_space(s)
