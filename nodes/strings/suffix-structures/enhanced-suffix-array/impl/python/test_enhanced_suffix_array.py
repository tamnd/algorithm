# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/enhanced-suffix-array/. The authors are listed in prov/VFC544.jsonl.

import random

from enhanced_suffix_array import NIL, EnhancedSuffixArray


def naive(text: str) -> tuple[list[int], list[int]]:
    """SA of T$ by sorting all suffixes, and L with L[0] = 0 and L[N] = -1 by brute force."""
    t = [ord(c) for c in text] + [0]
    sa = sorted(range(len(t)), key=lambda p: t[p:])

    def lcp(a: int, b: int) -> int:
        k = 0
        while t[a + k] == t[b + k]:
            k += 1
        return k

    return sa, [0] + [lcp(sa[i - 1], sa[i]) for i in range(1, len(t))] + [-1]


def by_definition(L: list[int]) -> tuple[list[int], list[int], list[int]]:
    """up, down and next from their definitions."""
    N = len(L) - 1
    up, down, nxt = [NIL] * (N + 1), [NIL] * (N + 1), [NIL] * (N + 1)
    for q in range(N + 1):
        for k in range(q):
            if L[k] > L[q] and all(L[r] >= L[k] for r in range(k + 1, q)):
                up[q] = k
                break
        for k in range(N, q, -1):
            if L[k] > L[q] and all(L[r] > L[k] for r in range(q + 1, k)):
                down[q] = k
                break
        for k in range(q + 1, N + 1):
            if L[k] == L[q] and all(L[r] > L[q] for r in range(q + 1, k)):
                nxt[q] = k
                break
    return up, down, nxt


def naive_tree(text: str) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """Internal nodes of the suffix tree of T$ as rank ranges, with their children."""
    t = text + "\0"
    sa = sorted(range(len(t)), key=lambda p: t[p:])
    nexts: dict[str, set[str]] = {}
    for i in range(len(text)):
        for j in range(i, len(text) + 1):
            nexts.setdefault(text[i:j], set()).add(t[j])
    labels = {u for u, s in nexts.items() if len(s) >= 2}
    labels = labels | {""} if text else set()
    rng = {u: (min(r for r, p in enumerate(sa) if t.startswith(u, p)), max(r for r, p in enumerate(sa) if t.startswith(u, p))) for u in labels}
    tree = {}
    for u, (a, b) in rng.items():
        kids, r = [], a
        while r <= b:
            best = (r, r)
            for w, (c, d) in rng.items():
                if c == r and len(w) > len(u) and w.startswith(u) and d - c > best[1] - best[0] and d <= b:
                    best = (c, d)
            kids.append(best)
            r = best[1] + 1
        tree[(a, b)] = kids
    return tree


def check(text: str) -> None:
    esa = EnhancedSuffixArray(text)
    sa, L = naive(text)
    assert esa.sa == sa and esa.lcp == L
    up, down, nxt = by_definition(L)
    assert esa.up[: len(L)] == up and esa.down[: len(L)] == down and esa.next[: len(L)] == nxt
    tree = naive_tree(text)
    for (a, b), kids in tree.items():
        assert esa.children(a, b) == kids, (text, a, b)
        assert esa.lcp_value(a, b) == min(L[a + 1 : b + 1])
    got = {(i, j) for _, i, j in esa.intervals()}
    assert got == set(tree) or (not text and got == {(0, 0)})
    t = text + "\0"
    pats = {text[i:j] for i in range(len(text)) for j in range(i, min(len(text), i + 6) + 1)} | {"x", "ba", "aaa", "gg"}
    for pat in pats:
        lo, hi = esa.find(pat)
        expect = [r for r, p in enumerate(sa) if t.startswith(pat, p)]
        assert list(range(lo, hi)) == expect, (text, pat)


def test_mississippi() -> None:
    esa = EnhancedSuffixArray("mississippi")
    assert esa.sa == [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert esa.lcp == [0, 0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3, -1]
    assert esa.children(0, 11) == [(0, 0), (1, 4), (5, 5), (6, 7), (8, 11)]
    assert esa.children(8, 11) == [(8, 9), (10, 11)]
    assert esa.find("ssi") == (10, 12)
    check("mississippi")


def test_special() -> None:
    check("")
    for n in range(1, 22):
        check("a" * n)
        check("ab" * n)
        check("ab" * n + "a")


def test_random() -> None:
    rng = random.Random(11)
    for trial in range(600):
        sigma = (1, 2, 4)[trial % 3]
        text = "".join(rng.choice("acgt"[:sigma]) for _ in range(rng.randrange(0, 24)))
        check(text)
