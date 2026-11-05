# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weiner-algorithm/. The authors are listed in prov/7NCBQB.jsonl.

import random

from weiner_algorithm import END, WeinerTree


def naive_node_count(s: str) -> int:
    """Root, n + 1 leaves, and one inner node per right-branching substring of S$."""
    t = list(s) + [None]
    ext: dict[str, set] = {}
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            ext.setdefault(s[i:j], set()).add(t[j])
    return len(s) + 2 + sum(1 for x in ext.values() if len(x) >= 2)


def test_example() -> None:
    tr = WeinerTree("abaaa")
    tr.check_invariant()
    assert tr.node_count() == 9 and tr.suffix_array() == [4, 3, 2, 0, 1]
    assert tr.trace == [
        (4, "new symbol", 0), (3, "split, virtual node", 1), (2, "split", 2),
        (1, "new symbol", 0), (0, "link", 1)]
    assert tr.ind[0] == {END, "a", "b"}
    tr = WeinerTree("banana")
    tr.check_invariant()
    assert tr.suffix_array() == [5, 3, 1, 0, 4, 2] and tr.node_count() == 11
    assert tr.contains("ana") and not tr.contains("nab") and tr.contains("")


def test_edges() -> None:
    tr = WeinerTree("")
    tr.check_invariant()
    assert tr.suffix_array() == [] and tr.node_count() == 2
    for n in (1, 2, 7, 500):
        tr = WeinerTree("a" * n)
        if n < 30:
            tr.check_invariant()
        assert tr.node_count() == 2 * n + 1
        assert tr.suffix_array() == list(range(n - 1, -1, -1))
    s = "ab" * 300
    tr = WeinerTree(s)
    assert tr.suffix_array() == sorted(range(600), key=lambda i: s[i:])
    tr = WeinerTree([3, 1, 4, 1, 5, 9, 2, 6])
    tr.check_invariant()
    assert tr.suffix_array() == [1, 3, 6, 0, 2, 4, 7, 5]


def test_against_naive() -> None:
    rng = random.Random(1973)
    for trial in range(700):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 20)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 25 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        tr = WeinerTree(s)
        tr.check_invariant()
        assert tr.suffix_array() == sorted(range(len(s)), key=lambda i: s[i:])
        assert tr.node_count() == naive_node_count(s)
        assert sum(len(x) for x in tr.wlink) <= tr.node_count()
        for _ in range(8):
            p = "".join(rng.choice(sigma + "e") for _ in range(rng.randint(0, 4)))
            assert tr.contains(p) == (p in s)


def test_long_inputs() -> None:
    """Long random and periodic strings build without recursion and sort correctly."""
    rng = random.Random(5)
    for s in ["".join(rng.choice("acgt") for _ in range(4000)), "abc" * 1500, "a" * 3000 + "b"]:
        tr = WeinerTree(s)
        assert tr.node_count() <= 2 * len(s) + 1
        sa = tr.suffix_array()
        assert sorted(sa) == list(range(len(s)))
        assert all(s[sa[r - 1]:] < s[sa[r]:] for r in range(1, 300))
