# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paes/. The authors are listed in prov/J8DPVZ.jsonl.

import itertools
import random

from paes import Grid, archive_add, dominates, paes


def front(images):
    return {y for y in images if not any(dominates(z, y) for z in images)}


def test_grid_cells() -> None:
    g = Grid([(0, 8), (8, 0)], 1)
    assert g.cell((0, 8)) == (0, 1)
    assert g.cell((3, 5)) == (0, 1)
    assert g.cell((4, 4)) == (1, 1)
    assert g.cell((8, 0)) == (1, 0)
    g2 = Grid([(0, 8), (8, 0)], 2)
    assert g2.cell((3, 5)) == (1, 2)


def test_example() -> None:
    for seed in range(10):
        a = [("a", (0, 8)), ("b", (2, 6)), ("c", (3, 5)), ("d", (8, 0))]
        assert archive_add(a, ("m", (6, 1)), 4, 1, random.Random(seed))
        names = {x for x, _ in a}
        assert len(a) == 4 and {"d", "m"} <= names
        assert len(names & {"a", "b", "c"}) == 2
    # a point in the most crowded cell is not added to a full archive
    a = [("a", (0, 8)), ("b", (2, 6)), ("c", (3, 5)), ("d", (8, 0))]
    assert not archive_add(a, ("m", (1, 7)), 4, 1, random.Random(0))
    # a dominated point is never added; a dominating point removes what it dominates
    assert not archive_add(a, ("m", (3, 6)), 4, 1, random.Random(0))
    assert archive_add(a, ("m", (1, 5)), 4, 1, random.Random(0))
    assert sorted(z for _, z in a) == [(0, 8), (1, 5), (8, 0)]


def bits(n):
    return lambda r: tuple(r.randint(0, 1) for _ in range(n))


def flip(x, r):
    y = tuple(b ^ 1 if r.random() < 1 / len(x) else b for b in x)
    return y


def two_knapsacks(x):
    w1 = [3, 1, 4, 1, 5, 9, 2]
    w2 = [2, 7, 1, 8, 2, 8, 1]
    return (-sum(a * b for a, b in zip(x, w1)), -sum((1 - a) * b for a, b in zip(x, w2)))


def test_unbounded_archive_is_front_of_seen() -> None:
    for seed in range(4):
        rng = random.Random(seed)
        start = bits(7)(random.Random(seed))
        seen = {two_knapsacks(start)}

        def hook(c, m, archive):
            seen.add(m[1])
            imgs = [z for _, z in archive]
            assert len(set(imgs)) == len(imgs)
            assert set(imgs) == front(seen)

        paes(bits(7), two_knapsacks, flip, 10**6, 2, 300, rng, hook)


def test_bounded_invariants() -> None:
    for seed, cap, l in [(1, 3, 1), (2, 5, 2), (3, 1, 3), (4, 4, 0)]:
        rng = random.Random(seed)
        prev = {}

        def hook(c, m, archive):
            assert 1 <= len(archive) <= cap
            assert all(len(x) == 7 and set(x) <= {0, 1} for x, _ in archive)
            assert all(z == two_knapsacks(x) for x, z in archive)
            assert c[1] == two_knapsacks(c[0])
            for (_, a), (_, b) in itertools.permutations(archive, 2):
                assert a != b and not dominates(a, b)
            # the current solution never moves to a point it dominates
            if "c" in prev:
                assert not dominates(prev["c"], c[1])
            prev["c"] = c[1]

        paes(bits(7), two_knapsacks, flip, cap, l, 300, rng, hook)
