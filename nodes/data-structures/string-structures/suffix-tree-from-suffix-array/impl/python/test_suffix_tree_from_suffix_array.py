# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-tree-from-suffix-array/. The authors are listed in prov/Q1HEHJ.jsonl.

import random

import pytest

from suffix_tree_from_suffix_array import Node, build, check_invariant, edge_label, lcp_array, suffix_array


def internal_labels(t: str, root: Node) -> set[str]:
    out: set[str] = set()
    stack: list[tuple[Node, str]] = [(root, "")]
    while stack:
        x, path = stack.pop()
        if x.leaf < 0:
            out.add(path)
            for c in x.children:
                stack.append((c, path + edge_label(t, x, c)))
    return out


def branching_substrings(t: str) -> set[str]:
    """The right-branching substrings of t, plus the empty string: the internal nodes of the suffix tree."""
    follow: dict[str, set[str]] = {}
    for i in range(len(t)):
        for j in range(i, len(t)):
            follow.setdefault(t[i:j], set()).add(t[j])
    return {w for w, f in follow.items() if len(f) >= 2} | {""}


def test_example() -> None:
    t = "banana\0"
    sa = suffix_array(t)
    lcp = lcp_array(t, sa)
    assert sa == [6, 5, 3, 1, 0, 4, 2] and lcp == [0, 0, 1, 3, 0, 0, 2]
    t, root = build("banana")
    check_invariant(t, root)
    assert sorted(internal_labels(t, root)) == ["", "a", "ana", "na"]
    assert [edge_label(t, root, c) for c in root.children] == ["\0", "a", "banana\0", "na"]


def test_edges() -> None:
    for s in ["", "a", "aaaa", "abab", "abcd"]:
        t, root = build(s)
        check_invariant(t, root)
        assert internal_labels(t, root) == branching_substrings(t)
    t, root = build("aaaa")
    assert sorted(internal_labels(t, root)) == ["", "a", "aa", "aaa"]
    with pytest.raises(ValueError):
        build("a\0b")


def test_random_against_naive() -> None:
    rng = random.Random(2004)
    for case in range(600):
        s = "".join(rng.choice("ab" if case % 2 else "abc") for _ in range(rng.randint(0, 25)))
        t, root = build(s)
        check_invariant(t, root)
        assert internal_labels(t, root) == branching_substrings(t)
