# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-suffix-tree/. The authors are listed in prov/Q61TVH.jsonl.

import random

from compressed_suffix_tree import CompressedSuffixTree


def naive_tree(text: str) -> tuple[list[int], dict[str, tuple[int, int]]]:
    """SA of T$ by sorting the suffixes, and every node label of the suffix tree of T$ with its rank range."""
    t = text + "\0"
    sa = sorted(range(len(t)), key=lambda p: t[p:])
    nexts: dict[str, set[str]] = {}
    for i in range(len(text)):
        for j in range(i, len(text) + 1):
            nexts.setdefault(text[i:j], set()).add(t[j])
    labels = {u for u, s in nexts.items() if len(s) >= 2} | ({""} if text else set())
    labels |= {t[p:] for p in range(len(t))}
    nodes = {}
    for u in labels:
        ranks = [r for r, p in enumerate(sa) if t.startswith(u, p)]
        nodes[u] = (ranks[0], ranks[-1])
    return sa, nodes


def check(text: str, step: int = 4, block: int = 8) -> None:
    cst = CompressedSuffixTree(text, step, block)
    sa, nodes = naive_tree(text)
    t = text + "\0"
    n = len(text)
    assert [cst.sa(i) for i in range(n + 1)] == sa
    by_range = {rng: u for u, rng in nodes.items()}
    assert len(by_range) == len(nodes)
    seen, todo = [], [cst.root()]
    while todo:
        v = todo.pop()
        seen.append(v)
        todo.extend(cst.children(v))
    assert sorted(seen) == sorted(by_range), text
    for v in seen:
        u = by_range[v]
        assert cst.depth(v) == len(u)
        assert cst.is_leaf(v) == (u.endswith("\0") or (n == 0))
        anc = [w for w in nodes if len(w) < len(u) and u.startswith(w)]
        par = cst.parent(v)
        if anc:
            assert par == nodes[max(anc, key=len)], (text, v)
        else:
            assert par is None and v == cst.root()
        kids = sorted((w for w in nodes if w != u and w.startswith(u) and nodes[max((x for x in nodes if len(x) < len(w) and w.startswith(x)), key=len)] == v), key=lambda w: nodes[w])
        assert cst.children(v) == [nodes[w] for w in kids]
        if v != cst.root():
            assert cst.suffix_link(v) == nodes[u[1:]] if u != "\0" else cst.suffix_link(v) == cst.root()
        assert "".join(cst.label(v)) == u.rstrip("\0")
        for d in range(len(u)):
            assert cst.letter(v, d) == (0 if u[d] == "\0" else sorted(set(text)).index(u[d]) + 1)
        for c in sorted(set(text)) + ["z"]:
            w = cst.child(v, c)
            expect = [x for x in kids if len(x) > len(u) and x[len(u)] == c]
            assert w == (nodes[expect[0]] if expect else None)
    rng = random.Random(len(text))
    for _ in range(20):
        a, b = rng.choice(seen), rng.choice(seen)
        ua, ub = by_range[a], by_range[b]
        k = 0
        while k < min(len(ua), len(ub)) and ua[k] == ub[k]:
            k += 1
        common = max((w for w in nodes if ua.startswith(w) and ub.startswith(w)), key=len)
        assert cst.lca(a, b) == nodes[common]
    pats = {text[i:j] for i in range(n) for j in range(i, min(n, i + 5) + 1)} | {"z", "ba", "aaa"}
    for pat in pats:
        lo, hi = cst.find(pat)
        expect = [r for r, p in enumerate(sa) if t.startswith(pat, p)]
        assert list(range(lo, hi)) == expect, (text, pat)


def test_mississippi() -> None:
    cst = CompressedSuffixTree("mississippi")
    assert [cst.lcp(r) for r in range(13)] == [-1, 0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3, -1]
    assert cst.children(cst.root()) == [(0, 0), (1, 4), (5, 5), (6, 7), (8, 11)]
    assert cst.parent((10, 11)) == (8, 11)
    assert cst.suffix_link((10, 11)) == (8, 9)
    assert cst.depth((3, 4)) == 4
    check("mississippi")
    check("mississippi", 2, 2)
    check("mississippi", 3, 1)


def test_special() -> None:
    check("")
    for n in range(1, 16):
        check("a" * n)
        check("ab" * n)
        check("ab" * n + "a", 3, 2)


def test_random() -> None:
    rng = random.Random(23)
    for trial in range(500):
        sigma = (1, 2, 4)[trial % 3]
        text = "".join(rng.choice("acgt"[:sigma]) for _ in range(rng.randrange(0, 17)))
        check(text, rng.choice((1, 2, 3, 4)), rng.choice((1, 2, 3, 8)))
