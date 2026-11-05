# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcp-interval-tree/. The authors are listed in prov/GAWS4P.jsonl.

import random

from lcp_interval_tree import LcpIntervalTree


def naive_intervals(text: str) -> list[tuple[int, int, int]]:
    """lcp-intervals by the definition, with LCP[0] = LCP[n] = -1 and the root as a 0-interval."""
    n = len(text)
    sa = sorted(range(n), key=lambda i: text[i:])
    assert [text[p:] for p in sa] == sorted(text[p:] for p in range(n))

    def lcp(a: str, b: str) -> int:
        k = 0
        while k < min(len(a), len(b)) and a[k] == b[k]:
            k += 1
        return k

    h = [-1] + [lcp(text[sa[i - 1]:], text[sa[i]:]) for i in range(1, n)] + [-1]
    out = {(0, 0, n - 1)}
    for i in range(n):
        for j in range(i + 1, n):
            inner = h[i + 1:j + 1]
            ell = min(inner)
            if ell > 0 and h[i] < ell and h[j + 1] < ell:
                out.add((ell, i, j))
    return sorted(out, key=lambda x: (x[1], -x[2], x[0]))


def branching(text: str) -> set[str]:
    """Substrings followed by two different symbols, where the end counts as a symbol."""
    t = text + "\0"
    nexts: dict[str, set[str]] = {}
    for i in range(len(text)):
        for j in range(i, len(text) + 1):
            nexts.setdefault(text[i:j], set()).add(t[j])
    return {u for u, s in nexts.items() if len(s) >= 2 and u}


def check(text: str) -> None:
    tree = LcpIntervalTree(text)
    assert tree.intervals() == naive_intervals(text)
    labels = {tree.label(v) for v in range(len(tree.value)) if v != tree.root}
    assert labels == branching(text)
    for v in range(len(tree.value) if text else 0):
        kids = tree.children(v)
        assert kids[0][0] == tree.lb[v] and kids[-1][1] == tree.rb[v]
        assert all(kids[t][1] + 1 == kids[t + 1][0] for t in range(len(kids) - 1))
        assert len(kids) >= 2 or v == tree.root
    pats = {text[i:j] for i in range(len(text)) for j in range(i + 1, min(len(text), i + 6) + 1)} | {"x", "ba", "aaa"}
    for pat in pats:
        lo, hi = tree.find(pat)
        expect = sorted(r for r, p in enumerate(tree.sa) if text.startswith(pat, p))
        assert list(range(lo, hi)) == expect, (text, pat)


def test_mississippi() -> None:
    tree = LcpIntervalTree("mississippi")
    assert tree.lcp == [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]
    assert tree.intervals() == [(0, 0, 10), (1, 0, 3), (4, 2, 3), (1, 5, 6), (1, 7, 10), (2, 7, 8), (3, 9, 10)]
    assert tree.children(tree.root) == [(0, 3), (4, 4), (5, 6), (7, 10)]
    check("mississippi")


def test_special() -> None:
    check("")
    for n in range(1, 25):
        check("a" * n)
        check("ab" * n)
        check("ab" * n + "a")


def test_random() -> None:
    rng = random.Random(5)
    for trial in range(600):
        sigma = (1, 2, 4)[trial % 3]
        text = "".join(rng.choice("acgt"[:sigma]) for _ in range(rng.randrange(0, 26)))
        check(text)
