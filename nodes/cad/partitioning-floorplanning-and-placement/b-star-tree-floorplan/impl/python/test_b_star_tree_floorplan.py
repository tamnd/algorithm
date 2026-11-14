# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-star-tree-floorplan/. The authors are listed in prov/WA1GJ6.jsonl.

import itertools
import random

from b_star_tree_floorplan import BStarTree


def overlap(a, b) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def shapes(n: int):
    """All binary tree shapes with n nodes, as nested (left, right) tuples; None is empty."""
    if n == 0:
        return [None]
    out = []
    for k in range(n):
        for a in shapes(k):
            for b in shapes(n - 1 - k):
                out.append((a, b))
    return out


def label(shape, names):
    """Turn a shape into a BStarTree, naming the nodes in preorder by names."""
    left, right = {}, {}
    it = iter(names)

    def rec(s):
        if s is None:
            return None
        b = next(it)
        left[b] = rec(s[0])
        right[b] = rec(s[1])
        return b

    root = rec(shape)
    return BStarTree(root, left, right)


def all_trees(n: int):
    for s in shapes(n):
        for p in itertools.permutations(range(n)):
            yield label(s, p)


def random_tree(n: int, rng: random.Random) -> BStarTree:
    t = BStarTree(None, {}, {})
    order = list(range(n))
    rng.shuffle(order)
    placed = []
    for b in order:
        if not placed:
            t.insert(b, None, "left")
        else:
            t.insert(b, rng.choice(placed), rng.choice(["left", "right"]))
        placed.append(b)
    return t


def best_packing_area(w: dict, h: dict) -> int:
    """Least bounding-box area of a packing, by brute force over positions (sums of other sizes)."""
    blocks = list(w)

    def sums(vals):
        s = {0}
        for v in vals:
            s |= {t + v for t in s}
        return sorted(s)

    cand = {b: [(px, py) for px in sums([w[c] for c in blocks if c != b]) for py in sums([h[c] for c in blocks if c != b])] for b in blocks}
    best = [sum(w.values()) * max(h.values())]
    placed: list = []

    def rec(k: int, wid: int, hei: int) -> None:
        if wid * hei >= best[0]:
            return
        if k == len(blocks):
            best[0] = wid * hei
            return
        b = blocks[k]
        for px, py in cand[b]:
            r = (px, py, px + w[b], py + h[b])
            if any(overlap(r, q) for q in placed):
                continue
            placed.append(r)
            rec(k + 1, max(wid, r[2]), max(hei, r[3]))
            placed.pop()

    rec(0, 0, 0)
    return best[0]


def check_packing(t: BStarTree, w: dict, h: dict) -> None:
    res = t.pack(w, h)
    assert res == t.pack_naive(w, h)
    width, height, pos = res
    r = {b: (x, y, x + w[b], y + h[b]) for b, (x, y) in pos.items()}
    for a, b in itertools.combinations(r, 2):
        assert not overlap(r[a], r[b])
    for b, (x, y) in pos.items():
        # down-compact: on the floor or resting on a block below it
        assert y == 0 or any(q[3] == y and q[0] < r[b][2] and r[b][0] < q[2] for a, q in r.items() if a != b)
        if t.left.get(b) is not None:
            assert pos[t.left[b]][0] == x + w[b]
        if t.right.get(b) is not None:
            assert pos[t.right[b]][0] == x
    assert width == max(q[2] for q in r.values()) and height == max(q[3] for q in r.values())


def test_example() -> None:
    # root 0; 0.left = 1, 1.left = 2, 0.right = 3, 3.left = 4
    t = BStarTree(0, {0: 1, 1: 2, 2: None, 3: 4, 4: None}, {0: 3, 1: None, 2: None, 3: None, 4: None})
    w = {0: 3, 1: 2, 2: 2, 3: 2, 4: 3}
    h = {0: 2, 1: 3, 2: 1, 3: 2, 4: 1}
    width, height, pos = t.pack(w, h)
    assert pos == {0: (0, 0), 1: (3, 0), 2: (5, 0), 3: (0, 2), 4: (2, 3)}
    assert (width, height) == (7, 4)
    assert t.blocks() == [0, 1, 2, 3, 4]
    check_packing(t, w, h)


def test_not_left_compact_and_not_injective() -> None:
    one = {0: 1, 1: 1, 2: 1}
    # 0.left = 1, 1.right = 2: block 2 sits at (1, 1) although (0, 1) is free
    t = BStarTree(0, {0: 1, 1: None, 2: None}, {0: None, 1: 2, 2: None})
    assert t.pack(one, one)[2] == {0: (0, 0), 1: (1, 0), 2: (1, 1)}
    # two different trees, one packing
    t1 = BStarTree(0, {0: None, 1: 2, 2: None}, {0: 1, 1: None, 2: None})
    t2 = BStarTree(0, {0: 2, 1: None, 2: None}, {0: 1, 1: None, 2: None})
    assert t1.pack(one, one)[2] == t2.pack(one, one)[2] == {0: (0, 0), 1: (0, 1), 2: (1, 0)}


def test_all_small_trees() -> None:
    rng = random.Random(21)
    counts = [len(shapes(n)) for n in range(7)]
    assert counts == [1, 1, 2, 5, 14, 42, 132]
    for n in range(1, 5):
        trees = list(all_trees(n))
        assert len(trees) == counts[n] * [1, 1, 2, 6, 24][n]
        for _ in range(6):
            w = {b: rng.randint(1, 4) for b in range(n)}
            h = {b: rng.randint(1, 4) for b in range(n)}
            for t in trees:
                t.check_invariant()
                check_packing(t, w, h)


def test_best_tree_is_best_packing() -> None:
    rng = random.Random(22)
    for trial in range(30):
        n = 3 if trial < 18 else 4
        w = {b: rng.randint(1, 5 if n == 3 else 3) for b in range(n)}
        h = {b: rng.randint(1, 5 if n == 3 else 3) for b in range(n)}
        best = min(wd * ht for wd, ht, _ in (t.pack(w, h) for t in all_trees(n)))
        assert best == best_packing_area(w, h)


def test_random_trees_and_moves() -> None:
    rng = random.Random(23)
    for _ in range(300):
        n = rng.randint(1, 30)
        t = random_tree(n, rng)
        t.check_invariant()
        w = {b: rng.randint(1, 9) for b in range(n)}
        h = {b: rng.randint(1, 9) for b in range(n)}
        check_packing(t, w, h)
        for _ in range(5):
            op = rng.randrange(3)
            if op == 0 and n >= 2:
                a, b = rng.sample(range(n), 2)
                t.swap(a, b)
            elif op == 1:
                b = rng.randrange(n)
                w[b], h[b] = h[b], w[b]  # rotate block b
            elif n >= 2:
                b = rng.randrange(n)
                t.delete(b)
                t.check_invariant()
                assert sorted(t.blocks()) == sorted(set(range(n)) - {b})
                p = rng.choice(t.blocks())
                t.insert(b, p, rng.choice(["left", "right"]))
            t.check_invariant()
            assert sorted(t.blocks()) == list(range(n))
            check_packing(t, w, h)


def test_empty() -> None:
    assert BStarTree(None, {}, {}).pack({}, {}) == (0, 0, {})
