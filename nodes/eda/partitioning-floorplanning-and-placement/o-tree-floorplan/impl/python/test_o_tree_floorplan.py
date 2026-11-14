# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/o-tree-floorplan/. The authors are listed in prov/GM5XEG.jsonl.

import itertools
import random

import pytest

from o_tree_floorplan import OTree, is_tree_string


def overlap(a, b) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def tree_strings(n: int) -> list[str]:
    """All strings with n zeros and n ones whose prefixes never have more ones than zeros."""
    out = []

    def rec(s: str, zeros: int, ones: int) -> None:
        if zeros == ones == n:
            out.append(s)
            return
        if zeros < n:
            rec(s + "0", zeros + 1, ones)
        if ones < zeros:
            rec(s + "1", zeros, ones + 1)

    rec("", 0, 0)
    return out


def b_star_pack(root, left, right, w, h):
    """Reference packing of a B*-tree by its rules, with a direct search for each y."""
    pos = {}
    if root is None:
        return pos
    stack = [(root, 0)]
    while stack:
        b, x = stack.pop()
        y = max([pos[a][1] + h[a] for a in pos if pos[a][0] < x + w[b] and x < pos[a][0] + w[a]], default=0)
        pos[b] = (x, y)
        if right.get(b) is not None:
            stack.append((right[b], x))
        if left.get(b) is not None:
            stack.append((left[b], x + w[b]))
    return pos


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


def check(t: OTree, w: dict, h: dict) -> None:
    res = t.pack(w, h)
    assert res == t.pack_naive(w, h)
    width, height, pos = res
    r = {b: (x, y, x + w[b], y + h[b]) for b, (x, y) in pos.items()}
    for a, b in itertools.combinations(r, 2):
        assert not overlap(r[a], r[b])
    par = t.parents()
    for b, (x, y) in pos.items():
        p = par[b]
        assert x == (0 if p is None else pos[p][0] + w[p])
        assert y == 0 or any(q[3] == y and q[0] < r[b][2] and r[b][0] < q[2] for a, q in r.items() if a != b)
    root, left, right = t.to_b_star()
    assert b_star_pack(root, left, right, w, h) == pos
    back = OTree.from_b_star(root, left, right)
    assert (back.bits, back.perm) == (t.bits, t.perm)


def test_example() -> None:
    a, b, c, d, e = range(5)
    t = OTree("0001110011", [a, b, c, d, e])
    w = {a: 3, b: 2, c: 2, d: 2, e: 3}
    h = {a: 2, b: 3, c: 1, d: 2, e: 1}
    width, height, pos = t.pack(w, h)
    assert pos == {a: (0, 0), b: (3, 0), c: (5, 0), d: (0, 2), e: (2, 3)}
    assert (width, height) == (7, 4)
    assert t.parents() == {a: None, b: a, c: b, d: None, e: d}
    assert t.to_b_star() == (a, {a: b, b: c, c: None, d: e, e: None}, {a: d, b: None, c: None, d: None, e: None})
    check(t, w, h)


def test_not_left_compact_and_not_injective() -> None:
    a, b, c, d, e = range(5)
    one = {v: 1 for v in range(5)}
    assert OTree("001011", [a, b, c]).pack(one, one)[2] == {a: (0, 0), b: (1, 0), c: (1, 1)}
    p1 = OTree("010011", [a, d, e]).pack(one, one)[2]
    p2 = OTree("001101", [a, e, d]).pack(one, one)[2]
    assert p1 == p2 == {a: (0, 0), d: (0, 1), e: (1, 0)}


def test_bad_input() -> None:
    for bits, perm in [("01", [1, 2]), ("10", [1]), ("0011", [1, 1]), ("0", [1]), ("0x", [1])]:
        with pytest.raises(ValueError):
            OTree(bits, perm)
    assert not is_tree_string("0110") and is_tree_string("0101") and is_tree_string("")
    assert OTree("", []).pack({}, {}) == (0, 0, {})


def test_all_small_trees() -> None:
    rng = random.Random(31)
    assert [len(tree_strings(n)) for n in range(7)] == [1, 1, 2, 5, 14, 42, 132]
    for n in range(1, 5):
        trees = [OTree(s, list(p)) for s in tree_strings(n) for p in itertools.permutations(range(n))]
        assert len(trees) == len(tree_strings(n)) * [1, 1, 2, 6, 24][n]
        for _ in range(6):
            w = {b: rng.randint(1, 4) for b in range(n)}
            h = {b: rng.randint(1, 4) for b in range(n)}
            for t in trees:
                check(t, w, h)


def test_best_tree_is_best_packing() -> None:
    rng = random.Random(32)
    for trial in range(30):
        n = 3 if trial < 18 else 4
        top = 5 if n == 3 else 3
        w = {b: rng.randint(1, top) for b in range(n)}
        h = {b: rng.randint(1, top) for b in range(n)}
        best = min(
            wd * ht
            for s in tree_strings(n)
            for p in itertools.permutations(range(n))
            for wd, ht, _ in [OTree(s, list(p)).pack(w, h)]
        )
        assert best == best_packing_area(w, h)


def random_tree_string(n: int, rng: random.Random) -> str:
    """A random tree string: a random walk that stays at depth 0 or more."""
    s, zeros, ones = [], 0, 0
    while ones < n:
        if zeros < n and (ones == zeros or rng.random() < 0.5):
            s.append("0")
            zeros += 1
        else:
            s.append("1")
            ones += 1
    return "".join(s)


def test_random_larger() -> None:
    rng = random.Random(33)
    for _ in range(300):
        n = rng.randint(1, 40)
        perm = list(range(n))
        rng.shuffle(perm)
        t = OTree(random_tree_string(n, rng), perm)
        w = {b: rng.randint(1, 9) for b in range(n)}
        h = {b: rng.randint(1, 9) for b in range(n)}
        check(t, w, h)
