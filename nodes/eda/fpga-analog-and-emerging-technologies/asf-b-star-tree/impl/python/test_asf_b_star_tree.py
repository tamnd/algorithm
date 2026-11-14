# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asf-b-star-tree/. The authors are listed in prov/TQF55M.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from asf_b_star_tree import ASFBStarTree


def shapes(n: int):
    """Every binary tree with n nodes, as (left, right) nested tuples or None."""
    if n == 0:
        yield None
        return
    for k in range(n):
        for a in shapes(k):
            for b in shapes(n - 1 - k):
                yield (a, b)


def all_trees(cells: dict):
    names = list(cells)
    for shape in shapes(len(names)):
        for perm in itertools.permutations(names):
            it = iter(perm)
            left, right = {}, {}

            def label(s):
                if s is None:
                    return None
                b = next(it)
                left[b] = label(s[0])
                right[b] = label(s[1])
                return b

            root = label(shape)
            yield ASFBStarTree(cells, root, left, right)


def check_symmetric(t: ASFBStarTree, p: dict) -> None:
    rects = p["rects"]
    for (b, side), (x, y, w, h) in rects.items():
        assert x >= -p["width"] / 2 and x + w <= p["width"] / 2 and y >= 0 and y + h <= p["height"]
        if side == "R":
            xl, yl, wl, hl = rects[(b, "L")]
            assert (yl, wl, hl) == (y, w, h) and xl + wl / 2 == -(x + w / 2)
            assert x >= 0
        if side == "S":
            assert x + w / 2 == 0
    items = list(rects.values())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            x1, y1, w1, h1 = items[i]
            x2, y2, w2, h2 = items[j]
            assert x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1


def connected(rects: dict) -> bool:
    """True if the cells form one region, joining two cells that share a piece of boundary of positive length."""
    items = list(rects.values())

    def touch(a, b):
        x1, y1, w1, h1 = a
        x2, y2, w2, h2 = b
        if x1 + w1 == x2 or x2 + w2 == x1:
            return min(y1 + h1, y2 + h2) > max(y1, y2)
        if y1 + h1 == y2 or y2 + h2 == y1:
            return min(x1 + w1, x2 + w2) > max(x1, x2)
        return False

    seen, stack = {0}, [0]
    while stack:
        i = stack.pop()
        for j in range(len(items)):
            if j not in seen and touch(items[i], items[j]):
                seen.add(j)
                stack.append(j)
    return len(seen) == len(items)


GROUPS = [
    {"a": ("pair", 2, 1), "b": ("pair", 1, 2), "s": ("self", 2, 2)},
    {"a": ("pair", 1, 1), "s": ("self", 2, 1), "t": ("self", 4, 1)},
    {"a": ("pair", 2, 1), "b": ("pair", 1, 1), "c": ("pair", 1, 3)},
    {"a": ("pair", 1, 2), "b": ("pair", 2, 1), "s": ("self", 2, 1), "t": ("self", 2, 2)},
]


def test_every_asf_tree_packs_symmetric() -> None:
    for cells in GROUPS:
        n_asf = 0
        for t in all_trees(cells):
            if not t.is_asf():
                with pytest.raises(ValueError):
                    t.pack()
                continue
            n_asf += 1
            check_symmetric(t, t.pack())
        assert n_asf > 0


def test_self_symmetric_half_is_on_the_axis_only_on_the_rightmost_branch() -> None:
    # In a plain B*-tree packing, x = 0 holds exactly for the rightmost branch.
    cells = {"a": ("pair", 1, 1), "b": ("pair", 2, 1), "c": ("pair", 1, 2), "d": ("pair", 3, 1)}
    for t in all_trees(cells):
        p = t.pack()
        on = set(t.rightmost_branch())
        for b in cells:
            assert (p["rects"][(b, "R")][0] == 0) == (b in on)


def brute_min_area(cells: dict, xmax: int, ymax: int, step: Fraction) -> Fraction:
    """The least area of a symmetric placement of the group, by trying every
    position of the right halves on a grid: a pair's right cell at x >= 0, a
    self-symmetric half at x = 0."""
    names = list(cells)
    xs = [k * step for k in range(int(xmax / step) + 1)]
    ys = list(range(ymax + 1))
    pairs_spots = list(itertools.product(xs, ys))
    best = None
    choices = [pairs_spots if cells[b][0] == "pair" else [(Fraction(0), y) for y in ys] for b in names]
    for choice in itertools.product(*choices):
        r = []
        for b, (x, y) in zip(names, choice):
            k, w, h = cells[b]
            r.append((x, y, Fraction(w, 2) if k == "self" else Fraction(w), Fraction(h)))
        if all(a[0] + a[2] <= c[0] or c[0] + c[2] <= a[0] or a[1] + a[3] <= c[1] or c[1] + c[3] <= a[1] for a, c in itertools.combinations(r, 2)):
            area = 2 * max(a[0] + a[2] for a in r) * max(a[1] + a[3] for a in r)
            best = area if best is None else min(best, area)
    return best


def best_tree_area(cells: dict) -> Fraction:
    best = None
    for t in all_trees(cells):
        if t.is_asf():
            p = t.pack()
            area = p["width"] * p["height"]
            best = area if best is None else min(best, area)
    return best


def test_least_area_over_trees_equals_grid_search() -> None:
    g1 = {"a": ("pair", 2, 1), "b": ("pair", 1, 2), "s": ("self", 2, 2)}
    assert best_tree_area(g1) == brute_min_area(g1, 4, 4, Fraction(1)) == 12
    g2 = {"a": ("pair", 1, 1), "s": ("self", 1, 1), "t": ("self", 3, 2)}
    assert best_tree_area(g2) == brute_min_area(g2, 3, 4, Fraction(1, 2))
    g3 = {"a": ("pair", 2, 1), "b": ("pair", 1, 1), "c": ("pair", 1, 3)}
    assert best_tree_area(g3) == brute_min_area(g3, 4, 4, Fraction(1))


def test_a_packing_need_not_be_connected() -> None:
    cells = {"r": ("self", 2, 3), "b": ("pair", 2, 1), "c": ("pair", 1, 1)}
    t = ASFBStarTree(cells, "r", {"r": None, "b": "c", "c": None}, {"r": "b", "b": None, "c": None})
    p = t.pack()
    check_symmetric(t, p)
    assert p["rects"][("c", "R")] == (2, 0, 1, 1)
    assert not connected(p["rects"])


def test_random_moves_keep_the_tree_asf() -> None:
    rng = random.Random(2009)
    cells = {"a": ("pair", 2, 1), "b": ("pair", 1, 2), "c": ("pair", 3, 1), "s": ("self", 2, 2), "t": ("self", 4, 1), "u": ("self", 1, 3)}
    t = ASFBStarTree(cells)
    assert t.is_asf()
    for _ in range(2000):
        op = rng.randrange(3)
        names = list(t.cells)
        if op == 0:
            t.rotate(rng.choice(names))
        elif op == 1:
            a, b = rng.sample(names, 2)
            try:
                t.swap(a, b)
            except ValueError:
                assert t.cells[a][0] == "self" or t.cells[b][0] == "self"
        else:
            b = rng.choice(names)
            t.delete(b)
            assert t.is_asf()
            rest = [u for u in t.left]
            if t.cells[b][0] == "self":
                spots = [(None, "right")] + [(u, "right") for u in t.rightmost_branch()]
            else:
                spots = [(None, "right")] + [(u, s) for u in rest for s in ("left", "right")]
            p, side = rng.choice(spots)
            t.insert(b, p, side)
        assert t.is_asf()
        assert sorted(t.preorder()) == sorted(cells)
        check_symmetric(t, t.pack())
