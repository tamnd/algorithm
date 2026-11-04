# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rooted-tree-representation/. The authors are listed in prov/X6DGHS.jsonl.

import random

import pytest

from rooted_tree_representation import Node, RootedTree


def build_example() -> tuple[RootedTree[str], dict[str, Node[str]]]:
    t: RootedTree[str] = RootedTree()
    n = {k: t.new_node(k) for k in "ABCDEFG"}
    for par, ch in [("A", "D"), ("A", "C"), ("A", "B"), ("B", "F"), ("B", "E"), ("D", "G")]:
        t.add_child(n[par], n[ch])
    return t, n


def test_example() -> None:
    t, n = build_example()
    assert [c.key for c in t.children(n["A"])] == ["B", "C", "D"]
    assert n["B"].left_child is n["E"] and n["B"].right_sibling is n["C"]
    assert t.parent(n["G"]) is n["D"] and t.parent(n["A"]) is None
    assert t.preorder(n["A"]) == list("ABEFCDG")
    assert t.postorder(n["A"]) == list("EFBCGDA")
    assert t.preorder(n["B"]) == list("BEF")  # a subtree stops at its root
    assert t.check_invariant(n["A"]) == 7


def test_detach_and_edges() -> None:
    t, n = build_example()
    t.detach(n["C"])  # a middle child
    assert [c.key for c in t.children(n["A"])] == ["B", "D"]
    t.detach(n["B"])  # the leftmost child
    assert [c.key for c in t.children(n["A"])] == ["D"]
    assert t.preorder(n["B"]) == list("BEF")
    t.add_child(n["G"], n["B"])
    assert t.preorder(n["A"]) == list("ADGBEF")
    t.detach(n["A"])  # a root: no change
    leaf = t.new_node("z")
    assert t.preorder(leaf) == ["z"] and t.postorder(leaf) == ["z"]
    assert list(t.children(leaf)) == []
    with pytest.raises(ValueError):
        t.add_child(leaf, n["D"])


def test_deep_and_wide() -> None:
    t: RootedTree[int] = RootedTree()
    root = t.new_node(0)
    x = root
    for i in range(1, 100_000):  # a path: no recursion limit is hit
        y = t.new_node(i)
        t.add_child(x, y)
        x = y
    assert t.preorder(root) == list(range(100_000))
    assert t.postorder(root) == list(range(99_999, -1, -1))
    wide = t.new_node(-1)
    for i in range(1000):
        t.add_child(wide, t.new_node(i))
    assert [c.key for c in t.children(wide)] == list(range(999, -1, -1))


def oracle_pre(kids: dict[int, list[int]], r: int) -> list[int]:
    out, stack = [], [r]
    while stack:
        x = stack.pop()
        out.append(x)
        stack.extend(reversed(kids[x]))
    return out


def oracle_post(kids: dict[int, list[int]], r: int) -> list[int]:
    return list(reversed(_mirror_pre(kids, r)))


def _mirror_pre(kids: dict[int, list[int]], r: int) -> list[int]:
    out, stack = [], [r]
    while stack:
        x = stack.pop()
        out.append(x)
        stack.extend(kids[x])
    return out


def test_random_against_child_lists() -> None:
    rng = random.Random(3141)
    for _ in range(500):
        t: RootedTree[int] = RootedTree()
        nodes = {0: t.new_node(0)}
        kids: dict[int, list[int]] = {0: []}
        par: dict[int, int | None] = {0: None}
        in_tree = {0}
        for step in range(rng.randint(0, 40)):
            if rng.random() < 0.7 or len(in_tree) == 1:
                k = len(nodes)
                nodes[k] = t.new_node(k)
                kids[k] = []
                x = rng.choice(sorted(in_tree))
                t.add_child(nodes[x], nodes[k])
                kids[x].insert(0, k)
                par[k] = x
                in_tree.add(k)
            else:
                y = rng.choice(sorted(in_tree - {0}))
                x = par[y]
                assert x is not None
                t.detach(nodes[y])
                kids[x].remove(y)
                sub = set(oracle_pre(kids, y))
                in_tree -= sub
                z = rng.choice(sorted(in_tree))  # re-attach the subtree elsewhere
                t.add_child(nodes[z], nodes[y])
                kids[z].insert(0, y)
                par[y] = z
                in_tree |= sub
            for v in in_tree:
                assert [c.key for c in t.children(nodes[v])] == kids[v]
                assert (t.parent(nodes[v]) or Node(None)).key == par[v]
        assert t.preorder(nodes[0]) == oracle_pre(kids, 0)
        assert t.postorder(nodes[0]) == oracle_post(kids, 0)
        assert t.check_invariant(nodes[0]) == len(in_tree)
