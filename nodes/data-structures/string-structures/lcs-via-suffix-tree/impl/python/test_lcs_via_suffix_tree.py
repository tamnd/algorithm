# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcs-via-suffix-tree/. The authors are listed in prov/2AY22B.jsonl.

import random

from lcs_via_suffix_tree import SuffixTree, longest_common_substring


def lcs_length_dp(a: str, b: str) -> int:
    best = 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


def check(a: str, b: str) -> None:
    k, i, j = longest_common_substring(a, b)
    assert k == lcs_length_dp(a, b)
    assert a[i : i + k] == b[j : j + k]


def leaf_suffixes(s: list[int]) -> list[int]:
    t = SuffixTree(s)
    n = len(s)
    out = []
    stack = [(0, 0)]
    while stack:
        v, d = stack.pop()
        if not t.children[v]:
            out.append(n - d)
        for w in t.children[v].values():
            stack.append((w, d + t.edge_len(w, n - 1)))
    return sorted(out)


def test_example() -> None:
    k, i, j = longest_common_substring("xabxac", "abcabxabcd")
    assert (k, "xabxac"[i : i + k]) == (4, "abxa")
    k, i, j = longest_common_substring("banana", "ananas")
    assert "banana"[i : i + k] == "anana"


def test_edges() -> None:
    assert longest_common_substring("", "") == (0, 0, 0)
    assert longest_common_substring("abc", "")[0] == 0
    assert longest_common_substring("abc", "xyz")[0] == 0
    assert longest_common_substring("aaaa", "aa")[0] == 2
    k, i, j = longest_common_substring("same", "same")
    assert (k, i, j) == (4, 0, 0)
    check("abab", "baba")


def test_tree_has_all_suffixes() -> None:
    rng = random.Random(77)
    for _ in range(200):
        s = [rng.randint(0, 2) for _ in range(rng.randint(0, 30))] + [-2]
        assert leaf_suffixes(s) == list(range(len(s)))


def test_random_against_dp() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        alpha = "ab" if rng.random() < 0.5 else "abcd"
        a = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 25)))
        b = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 25)))
        check(a, b)
