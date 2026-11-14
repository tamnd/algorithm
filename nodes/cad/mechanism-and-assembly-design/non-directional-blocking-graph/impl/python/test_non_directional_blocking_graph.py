# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-directional-blocking-graph/. The authors are listed in prov/RMGX71.jsonl.

import random
from fractions import Fraction

from assembly_boxes import (
    free_by_sampling, interiors_overlap, is_valid_assembly, random_boxes, translate)
from non_directional_blocking_graph import (
    CELLS, blocked, build, can_move, cell_of, removable, separate, tarjan_sccs)

# ---- independent reference: move the parts a small step and look ----


def step(d):
    """A step length for direction d that is small enough for integer corners:
    each coordinate moves by at most 1/2, so a gap of at least 1 stays open
    and an overlap of at least 1 stays closed."""
    return Fraction(1, 2 * max(abs(x) for x in d))


def moves_freely(boxes, s_mask, d):
    """Does the set s_mask move by a small step along d with no collision?"""
    t = step(d)
    n = len(boxes)
    moved = [translate(boxes[i], d, t) for i in range(n) if s_mask >> i & 1]
    rest = [boxes[j] for j in range(n) if not s_mask >> j & 1]
    return not any(interiors_overlap(a, b) for a in moved for b in rest)


def directions_in(rng, s, count):
    """Random integer direction vectors whose sign vector is s."""
    out = [s]
    for _ in range(count):
        out.append(tuple(x * rng.randint(1, 3) for x in s))
    return out


def scenes(rng, count, n_max):
    """Random products, some with parts that touch only at an edge or a corner."""
    out = []
    for _ in range(count):
        n = rng.randint(2, n_max)
        out.append(random_boxes(rng, n, size=3, max_side=2, connected=rng.random() < 0.7))
    out.append([(0, 0, 0, 1, 1, 1), (1, 1, 1, 2, 2, 2)])            # corner contact
    out.append([(0, 0, 0, 1, 1, 1), (1, 1, 0, 2, 2, 1)])            # edge contact
    out.append([(0, 0, 0, 1, 1, 1), (1, 0, 0, 2, 1, 1), (0, 1, 0, 2, 2, 1)])
    return out


# ---- tests ----


def test_blocking_matches_a_small_motion():
    rng = random.Random(31)
    for boxes in scenes(rng, 60, 4):
        assert is_valid_assembly(boxes)
        for s in CELLS:
            for d in directions_in(rng, s, 2):
                assert cell_of(d) == s
                for i, a in enumerate(boxes):
                    for j, b in enumerate(boxes):
                        if i != j:
                            moved = translate(a, d, step(d))
                            assert blocked(a, b, s) == interiors_overlap(moved, b)


def test_reverse_cell_is_reverse_graph():
    rng = random.Random(32)
    for boxes in scenes(rng, 30, 5):
        g = build(boxes)
        n = len(boxes)
        for s in CELLS:
            minus = tuple(-x for x in s)
            for i in range(n):
                for j in range(n):
                    assert (g[s][i] >> j & 1) == (g[minus][j] >> i & 1)


def test_can_move_and_scc_against_all_subsets():
    rng = random.Random(33)
    for boxes in scenes(rng, 40, 6):
        n = len(boxes)
        g = build(boxes)
        full = (1 << n) - 1
        for s in CELLS:
            out = g[s]
            movable = []
            for mask in range(1, full):
                ok = moves_freely(boxes, mask, s)
                assert can_move(out, mask, full) == ok
                if ok:
                    movable.append(mask)
            c = removable(out, full)
            if movable:
                assert c is not None and c in movable
            else:
                assert c is None
            # every movable set is a union of strongly connected components
            comps = tarjan_sccs(out, full)
            assert sum(comps) == full
            for m in movable:
                assert all(m & k in (0, k) for k in comps)


def test_subassemblies():
    rng = random.Random(34)
    for boxes in scenes(rng, 20, 6):
        n = len(boxes)
        g = build(boxes)
        for within in range(1, 1 << n):
            sub = [boxes[i] for i in range(n) if within >> i & 1]
            index = [i for i in range(n) if within >> i & 1]
            found = separate(g, within)
            any_free = any(
                moves_freely(sub, m, s) for s in CELLS for m in range(1, (1 << len(sub)) - 1))
            assert (found is not None) == any_free
            if found is not None:
                s, c = found
                local = sum(1 << index.index(i) for i in range(n) if c >> i & 1)
                assert moves_freely(sub, local, s)


def test_fraction_coordinates():
    rng = random.Random(35)
    for _ in range(20):
        boxes = random_boxes(rng, 4, size=3, max_side=2, connected=True)
        scaled = [tuple(Fraction(c, 7) for c in b) for b in boxes]
        assert build(scaled) == build(boxes)


def test_example_three_bars():
    bars = [
        (1, 1, 0, 2, 2, 2),   # 0 a: a column along z
        (0, 0, 0, 2, 1, 1),   # 1 b: a bar along x
        (0, 0, 1, 1, 2, 2),   # 2 c: a bar along y
    ]
    g = build(bars)
    assert len({tuple(out) for out in g.values()}) == 26
    # along (+, -, +): a is blocked by b, b by c and c by a
    assert g[(1, -1, 1)] == [1 << 1, 1 << 2, 1 << 0]
    locked = sorted(s for s in CELLS if removable(g[s], 7) is None)
    assert locked == [(-1, 1, -1), (1, -1, 1)]
    # along each axis cell the graph has no cycle, so a part can move
    for s in CELLS:
        if sum(map(abs, s)) == 1:
            assert all(bin(c).count("1") == 1 for c in tarjan_sccs(g[s], 7))


def test_example_frame():
    frame = [
        (0, 0, 0, 4, 2, 1),   # 0 base plate
        (0, 0, 1, 1, 2, 3),   # 1 left post
        (3, 0, 1, 4, 2, 3),   # 2 right post
        (1, 0, 1, 3, 2, 2),   # 3 block
        (0, 0, 3, 4, 2, 4),   # 4 top plate
    ]
    g = build(frame)
    full = 31
    assert len({tuple(out) for out in g.values()}) == 9
    # along +x the left post is blocked by the block, the block by the right post
    assert g[(1, 0, 0)][1] == 1 << 3 and g[(1, 0, 0)][3] == 1 << 2
    # a small step up is free for the block, because it does not touch the top
    # plate; a translation to infinity along +z is not
    assert can_move(g[(0, 0, 1)], 1 << 3, full)
    assert not moves_far(frame, 3, (0, 0, 1))
    assert separate(g, full) is not None


def moves_far(boxes, i, d):
    return free_by_sampling([boxes[i]], [b for j, b in enumerate(boxes) if j != i], d)
