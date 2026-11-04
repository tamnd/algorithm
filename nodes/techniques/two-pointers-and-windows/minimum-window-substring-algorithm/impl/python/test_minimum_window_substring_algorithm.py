# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-window-substring-algorithm/. The authors are listed in prov/380AMB.jsonl.

import random
from collections import Counter

from minimum_window_substring_algorithm import min_window


def brute(s: str, t: str) -> str:
    need = Counter(t)
    best = None
    for i in range(len(s)):
        for j in range(i, len(s)):
            have = Counter(s[i : j + 1])
            if all(have[c] >= k for c, k in need.items()):
                if best is None or j - i + 1 < best[0]:
                    best = (j - i + 1, i)
                break
    return "" if best is None else s[best[1] : best[1] + best[0]]


def test_example() -> None:
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"


def test_edges() -> None:
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
    assert min_window("aa", "aa") == "aa"
    assert min_window("", "a") == ""
    assert min_window("abc", "") == ""
    assert min_window("AAB", "AB") == "AB"
    assert min_window("abcab", "ab") == "ab"
    assert min_window("xyz", "q") == ""


def test_against_brute_force() -> None:
    rng = random.Random(20261104)
    for _ in range(2000):
        s = "".join(rng.choice("abcd") for _ in range(rng.randrange(0, 14)))
        t = "".join(rng.choice("abcd") for _ in range(rng.randrange(1, 5)))
        assert min_window(s, t) == brute(s, t)
