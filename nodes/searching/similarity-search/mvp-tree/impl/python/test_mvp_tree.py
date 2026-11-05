# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mvp-tree/. The authors are listed in prov/WR0RGE.jsonl.

import math
import random

from mvp_tree import Internal, Leaf, MVPTree

P = [(1, 1), (2, 6), (4, 4), (5, 1), (6, 7), (8, 3), (9, 8), (3, 9), (7, 5), (0, 4), (10, 2), (6, 2)]
N = dict(zip("abcdefghijkl", P))


def depth(node) -> int:
    if isinstance(node, Leaf):
        return 1
    return 1 + max(depth(c) for row in node.children for c in row)


def edit(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def test_example() -> None:
    t = MVPTree(P, math.dist, m=2, k=2, p=2, choose=lambda n: 0)
    assert t.evaluations == 29
    root = t.root
    assert isinstance(root, Internal) and root.v1 == N["a"] and root.v2 == N["g"]
    leaf = root.children[0][1]
    assert {leaf.v1, leaf.v2} == {N["b"], N["d"]}
    (j,) = leaf.entries
    assert j.obj == N["j"] and [round(x, 4) for x in j.path] == [3.1623, 9.8489]
    t.evaluations = 0
    assert sorted(t.range((5, 5), 2)) == sorted([N["c"], N["i"]])
    assert t.evaluations == 8


def test_edges() -> None:
    assert MVPTree([], math.dist).range((0, 0), 1) == []
    assert MVPTree([(1, 1)], math.dist).range((0, 0), 2) == [(1, 1)]
    same = MVPTree([(2, 2)] * 20, math.dist, k=1, p=3)
    assert len(same.range((2, 2), 0)) == 20


def test_height() -> None:
    for n in [1, 5, 16, 64, 300]:
        for m in [2, 3]:
            t = MVPTree([(i, 0) for i in range(n)], math.dist, m=m, k=1, p=2, seed=n)
            assert depth(t.root) <= math.ceil(math.log(max(n, 2), m * m)) + 1
            assert t.evaluations <= 2 * n * depth(t.root)


def test_random_against_scan() -> None:
    rng = random.Random(1997)
    for trial in range(500):
        m, k, p = rng.choice([2, 3]), rng.randint(1, 5), rng.randint(0, 6)
        if trial % 2:
            dim = rng.choice([1, 2, 3])
            pts = [tuple(rng.randint(0, 9) for _ in range(dim)) for _ in range(rng.randint(0, 60))]
            d = math.dist
            q = tuple(rng.uniform(-1, 10) for _ in range(dim))
            r = rng.uniform(0, 5)
        else:
            pts = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(0, 40))]
            d = edit
            q = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
            r = rng.randint(0, 3)
        t = MVPTree(pts, d, m=m, k=k, p=p, seed=trial)
        assert sorted(t.range(q, r)) == sorted(x for x in pts if d(q, x) <= r)
