# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-longest-substring/. The authors are listed in prov/H69540.jsonl.

import random

from sliding_window_longest_substring import length_of_longest_substring, longest_distinct_substring


def brute(s: str) -> tuple[int, int]:
    best = (0, 0)
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i : j + 1])) == j - i + 1 and j - i + 1 > best[0]:
                best = (j - i + 1, i)
    return best


def test_example() -> None:
    assert longest_distinct_substring("abcabcbb") == (3, 0)
    assert longest_distinct_substring("bbbbb") == (1, 0)
    assert longest_distinct_substring("pwwkew") == (3, 2)


def test_edges() -> None:
    assert longest_distinct_substring("") == (0, 0)
    assert longest_distinct_substring(" ") == (1, 0)
    assert longest_distinct_substring("abba") == (2, 0)
    assert longest_distinct_substring("dvdf") == (3, 1)
    assert longest_distinct_substring("abcdef") == (6, 0)
    assert longest_distinct_substring([1, 2, 1, 3, 4]) == (4, 1)
    assert length_of_longest_substring("tmmzuxt") == 5


def test_against_brute_force() -> None:
    rng = random.Random(20261104)
    for _ in range(2000):
        n = rng.randrange(0, 16)
        s = "".join(rng.choice("abcde"[: rng.randrange(1, 6)]) for _ in range(n))
        assert longest_distinct_substring(s) == brute(s)
