# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farach-algorithm/. The authors are listed in prov/5GVP55.jsonl.

import random

from farach_algorithm import Merged, farach, suffix_array_lcp, suffix_tree, tree_from_sa


def naive(text: str) -> tuple[list[int], list[int]]:
    t = [ord(c) for c in text] + [0]
    sa = sorted(range(len(t)), key=lambda p: t[p:])

    def lcp(a: int, b: int) -> int:
        k = 0
        while t[a + k] == t[b + k]:
            k += 1
        return k

    return sa, [0] + [lcp(sa[k - 1], sa[k]) for k in range(1, len(t))]


def check(text: str) -> None:
    assert suffix_array_lcp(text) == naive(text), text
    tree = suffix_tree(text)
    t = text + "\0"
    nodes = {t[:0]}
    for v in range(len(tree.depth)):
        p = tree.pos[v]
        nodes.add(t[p:p + tree.depth[v]])
    branching = {u for u in {text[i:j] for i in range(len(text)) for j in range(i, len(text) + 1)} if len({t[i + len(u)] for i in range(len(text)) if t.startswith(u, i)}) >= 2}
    assert nodes == branching | {t[p:] for p in range(len(t))} | {""}
    assert len(tree.depth) == len(nodes)


def check_merge(text: str) -> None:
    """The d-tree depths equal the true lcp of every odd-even pair at the top level."""
    code = {c: r + 1 for r, c in enumerate(sorted(set(text)))}
    t = [code[c] for c in text] + [0]
    N = len(t)
    sa, lcp = naive(text)
    odd = [p for p in sa if p % 2 == 1]
    even = [p for p in sa if p % 2 == 0]

    def adj(order: list[int]) -> list[int]:
        return [0] + [naive_lcp(t, order[k - 1], order[k]) for k in range(1, len(order))]

    m = Merged(t, tree_from_sa(odd, adj(odd), N), tree_from_sa(even, adj(even), N))
    for x in odd:
        for y in even:
            assert m.ell(x, y) == naive_lcp(t, x, y), (text, x, y)
            assert m.less(x, y) == (t[x:] < t[y:])


def naive_lcp(t: list[int], a: int, b: int) -> int:
    k = 0
    while t[a + k] == t[b + k]:
        k += 1
    return k


def test_examples() -> None:
    sa, lcp = suffix_array_lcp("mississippi")
    assert sa == [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert lcp == [0, 0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]
    assert farach([2, 1, 2, 1]) == ([4, 3, 1, 2, 0], [0, 0, 1, 0, 2])
    check("mississippi")
    check_merge("mississippi")


def test_special() -> None:
    check("")
    for n in range(1, 40):
        check("a" * n)
        check("ab" * n)
        check("aab" * n)
        check_merge("a" * n)
        check_merge("ab" * n + "a")


def test_random() -> None:
    rng = random.Random(41)
    for trial in range(900):
        sigma = (1, 2, 4)[trial % 3]
        text = "".join(rng.choice("acgt"[:sigma]) for _ in range(rng.randrange(0, 60)))
        check(text)
        if len(text) < 30:
            check_merge(text)


def test_long() -> None:
    rng = random.Random(7)
    for sigma in (1, 2, 4):
        text = "".join(rng.choice("acgt"[:sigma]) for _ in range(3000))
        assert suffix_array_lcp(text) == naive(text)
