# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bk-tree/. The authors are listed in prov/WM7ED9.jsonl.

import random

from bk_tree import BKTree, levenshtein

WORDS = ["book", "books", "cake", "boo", "boon", "cook", "cape", "cart"]


def check_invariant(t) -> None:
    def items(u):
        yield u.item
        for c in u.children.values():
            yield from items(c)

    for i, c in t.children.items():
        assert all(levenshtein(x, t.item) == i for x in items(c))
        check_invariant(c)


def test_levenshtein() -> None:
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("", "abc") == 3
    assert levenshtein("flaw", "lawn") == 2


def test_example() -> None:
    tree = BKTree(items=WORDS)
    assert tree.root.item == "book"
    assert sorted(tree.root.children) == [1, 4]
    assert tree.root.children[1].item == "books"
    assert tree.root.children[4].item == "cake"
    check_invariant(tree.root)
    assert sorted(tree.range("bool", 1)) == ["boo", "book", "boon"]
    assert tree.nearest("cast") == (1, "cart")
    assert tree.insert("book") is False
    assert tree.size == len(WORDS)


def test_empty() -> None:
    tree = BKTree()
    assert tree.range("a", 3) == []
    assert tree.nearest("a") is None


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        alphabet = "ab" if rng.random() < 0.5 else "abcd"
        words = {"".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 30))}
        words = list(words)
        rng.shuffle(words)
        tree = BKTree(items=words)
        assert tree.size == len(words)
        if tree.root is not None:
            check_invariant(tree.root)
        q = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
        r = rng.randint(0, 4)
        assert sorted(tree.range(q, r)) == sorted(w for w in words if levenshtein(q, w) <= r)
        got = tree.nearest(q)
        if words:
            assert got[0] == min(levenshtein(q, w) for w in words)
            assert levenshtein(q, got[1]) == got[0]
        else:
            assert got is None


def test_other_metric() -> None:
    rng = random.Random(7)
    pts = rng.sample(range(1000), 200)
    tree = BKTree(dist=lambda a, b: abs(a - b), items=pts)
    for _ in range(200):
        q, r = rng.randrange(1000), rng.randrange(20)
        assert sorted(tree.range(q, r)) == sorted(p for p in pts if abs(p - q) <= r)
