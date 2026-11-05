# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mccreight-algorithm/. The authors are listed in prov/1S27ZF.jsonl.

import random

from mccreight_algorithm import McCreightTree


def naive_node_count(s: str) -> int:
    """Root, n + 1 leaves, and one inner node per right-branching substring of S$."""
    t = list(s) + [None]
    ext: dict[str, set] = {}
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            ext.setdefault(s[i:j], set()).add(t[j])
    return len(s) + 2 + sum(1 for x in ext.values() if len(x) >= 2)


def test_example() -> None:
    tr = McCreightTree("aaabaaa")
    tr.check_invariant()
    assert tr.node_count() == 12
    assert tr.suffix_array() == [6, 5, 4, 0, 1, 2, 3]
    assert [(i, d) for i, _, d in tr.trace] == [(1, 2), (2, 1), (3, 0), (4, 3), (5, 2), (6, 1), (7, 0)]
    assert [c for _, c, _ in tr.trace] == [
        "scan from root", "rescan, new node", "rescan", "scan from root", "rescan", "link", "link"]
    tr = McCreightTree("banana")
    tr.check_invariant()
    assert tr.suffix_array() == [5, 3, 1, 0, 4, 2] and tr.node_count() == 11
    assert tr.contains("nan") and not tr.contains("nab") and tr.contains("")


def test_edges() -> None:
    tr = McCreightTree("")
    tr.check_invariant()
    assert tr.suffix_array() == [] and tr.node_count() == 2
    for n in (1, 2, 7, 500):
        tr = McCreightTree("a" * n)
        if n < 50:
            tr.check_invariant()
        assert tr.node_count() == 2 * n + 1
        assert tr.suffix_array() == list(range(n - 1, -1, -1))
    s = "ab" * 300
    tr = McCreightTree(s)
    assert tr.suffix_array() == sorted(range(600), key=lambda i: s[i:])
    tr = McCreightTree([3, 1, 4, 1, 5, 9, 2, 6])
    tr.check_invariant()
    assert tr.suffix_array() == [1, 3, 6, 0, 2, 4, 7, 5]


def test_against_naive() -> None:
    rng = random.Random(1976)
    for trial in range(800):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 24)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 25 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        tr = McCreightTree(s)
        tr.check_invariant()
        assert tr.suffix_array() == sorted(range(len(s)), key=lambda i: s[i:])
        assert tr.node_count() == naive_node_count(s)
        for _ in range(8):
            p = "".join(rng.choice(sigma + "e") for _ in range(rng.randint(0, 4)))
            assert tr.contains(p) == (p in s)


def test_linear_work() -> None:
    """Long random and periodic strings build without recursion and sort correctly."""
    rng = random.Random(7)
    for s in ["".join(rng.choice("ab") for _ in range(4000)), "abc" * 1500, "a" * 3000 + "b"]:
        tr = McCreightTree(s)
        assert tr.node_count() <= 2 * len(s) + 1
        sa = tr.suffix_array()
        assert len(sa) == len(s) and all(s[sa[r - 1]:] < s[sa[r]:] for r in range(1, min(len(s), 300)))
