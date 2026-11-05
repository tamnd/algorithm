# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/manacher/. The authors are listed in prov/25Z40B.jsonl.

import random

from manacher import is_palindrome_query, longest_palindrome, manacher


def brute_radii(s: str) -> list[int]:
    """For each center c, the length of the longest palindrome s[i..j] with i + j + 1 = c."""
    n = len(s)
    out = [0] * (2 * n + 1)
    for i in range(n):
        for j in range(i, n):
            t = s[i : j + 1]
            if t == t[::-1]:
                c = i + j + 1
                out[c] = max(out[c], j - i + 1)
    return out


def brute_longest(s: str) -> tuple[int, int]:
    best = (0, 0)
    for i in range(len(s)):
        for j in range(i, len(s)):
            t = s[i : j + 1]
            if t == t[::-1] and j - i + 1 > best[1]:
                best = (i, j - i + 1)
    return best


def test_example() -> None:
    assert manacher("abaabaab") == [0, 1, 0, 3, 0, 1, 6, 1, 0, 7, 0, 1, 4, 1, 0, 1, 0]
    assert manacher("abacaba") == [0, 1, 0, 3, 0, 1, 0, 7, 0, 1, 0, 3, 0, 1, 0]
    assert longest_palindrome("banana") == (1, 5)


def test_edges() -> None:
    assert manacher("") == [0]
    assert longest_palindrome("") == (0, 0)
    assert manacher("a") == [0, 1, 0]
    for n in range(1, 30):
        p = manacher("a" * n)
        assert p == [min(c, 2 * n - c) for c in range(2 * n + 1)]
        assert longest_palindrome("a" * n) == (0, n)
    s = "abc" * 10
    assert max(manacher(s)) == 1
    assert longest_palindrome(s) == (0, 1)
    assert manacher([1, 2, 1]) == [0, 1, 0, 3, 0, 1, 0]


def test_random_against_brute_force() -> None:
    rng = random.Random(20251105)
    for trial in range(1500):
        k = (1, 2, 3)[trial % 3]
        n = rng.randrange(0, 16)
        s = "".join(rng.choice("abc"[:k]) for _ in range(n))
        p = manacher(s)
        assert p == brute_radii(s), s
        assert longest_palindrome(s) == brute_longest(s), s
        for i in range(n):
            for j in range(i, n):
                t = s[i : j + 1]
                assert is_palindrome_query(p, i, j) == (t == t[::-1])


def test_long_input_is_linear() -> None:
    s = "ab" * 50000 + "a"
    p = manacher(s)
    assert p[len(s)] == len(s)
