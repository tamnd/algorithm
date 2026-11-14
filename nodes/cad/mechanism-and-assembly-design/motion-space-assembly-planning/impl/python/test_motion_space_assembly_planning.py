# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-space-assembly-planning/. The authors are listed in prov/TCQ1T4.jsonl.

import random
from fractions import Fraction

from assembly_boxes import AXES6, free_by_sampling, members, random_boxes
from motion_space_assembly_planning import (
    blocking_graph, closed_sets, removable_sets, separations, tarjan_sccs)

# ---- independent reference: try every subset and sweep it out ----


def brute_removable(boxes, within, d):
    out = []
    for s in range(1, within):
        if s & ~within or s == within:
            continue
        movers = [boxes[i] for i in members(s)]
        others = [boxes[i] for i in members(within & ~s)]
        if free_by_sampling(movers, others, d):
            out.append(s)
    return out


def brute_closed(out, within):
    return [s for s in range(1, within)
            if not s & ~within and s != within
            and all(out[i] & within & ~s == 0 for i in members(s))]


# ---- tests ----


def test_against_all_subsets_up_to_five_parts():
    rng = random.Random(41)
    for _ in range(8):
        n = rng.randint(2, 5)
        boxes = random_boxes(rng, n, size=3, max_side=2, connected=rng.random() < 0.8)
        for within in range(1, 1 << n):
            got = removable_sets(boxes, within)
            for d in AXES6:
                assert got[d] == brute_removable(boxes, within, d)


def test_against_all_subsets_six_parts():
    rng = random.Random(42)
    for _ in range(4):
        boxes = random_boxes(rng, 6, size=3, max_side=2, connected=True)
        full = 63
        got = removable_sets(boxes, full)
        for d in AXES6:
            assert got[d] == brute_removable(boxes, full, d)


def test_closed_sets_with_cycles():
    rng = random.Random(43)
    for _ in range(300):
        n = rng.randint(1, 7)
        out = [0] * n
        for i in range(n):
            for j in range(n):
                if i != j and rng.random() < 0.3:
                    out[i] |= 1 << j
        full = (1 << n) - 1
        got = closed_sets(out, full)
        assert len(got) == len(set(got))
        assert sorted(got) == brute_closed(out, full)
        within = rng.randint(1, full)
        assert sorted(closed_sets(out, within)) == brute_closed(out, within)


def test_axis_graphs_have_no_cycle():
    rng = random.Random(44)
    for _ in range(40):
        n = rng.randint(2, 6)
        boxes = random_boxes(rng, n, size=3, max_side=3, connected=True)
        full = (1 << n) - 1
        for d in AXES6:
            comps = tarjan_sccs(blocking_graph(boxes, d, full), full)
            assert all(bin(c).count("1") == 1 for c in comps)
            # so a single part can always leave along d
            assert any(bin(s).count("1") == 1 for s in removable_sets(boxes, full, [d])[d])


def test_separations():
    rng = random.Random(45)
    for _ in range(15):
        n = rng.randint(2, 5)
        boxes = random_boxes(rng, n, size=3, max_side=2, connected=True)
        full = (1 << n) - 1
        motions = tuple(rng.sample(AXES6, rng.randint(1, 3)))
        want = set()
        for s in range(1, full):
            if s & 1:
                a = [boxes[i] for i in members(s)]
                b = [boxes[i] for i in members(full & ~s)]
                if any(free_by_sampling(a, b, d) or free_by_sampling(b, a, d) for d in motions):
                    want.add((s, full & ~s))
        assert set(separations(boxes, full, motions)) == want


def test_fraction_coordinates():
    rng = random.Random(46)
    for _ in range(10):
        boxes = random_boxes(rng, 5, size=3, max_side=2, connected=True)
        scaled = [tuple(Fraction(c, 3) for c in b) for b in boxes]
        assert removable_sets(scaled, 31) == removable_sets(boxes, 31)


def test_example_frame():
    frame = [
        (0, 0, 0, 4, 2, 1),   # 0 base plate
        (0, 0, 1, 1, 2, 3),   # 1 left post
        (3, 0, 1, 4, 2, 3),   # 2 right post
        (1, 0, 1, 3, 2, 2),   # 3 block
        (0, 0, 3, 4, 2, 4),   # 4 top plate
    ]
    got = removable_sets(frame, 31)
    counts = {d: len(v) for d, v in got.items()}
    assert counts == EXAMPLE_COUNTS
    # along +z only sets that hold the top plate can leave
    assert all(s >> 4 & 1 for s in got[(0, 0, 1)])
    # in the plane of the frame, the block alone never leaves the closed frame
    plane = ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1))
    assert all(s != 1 << 3 for d in plane for s in got[d])
    assert 1 << 3 in got[(0, 1, 0)]
    # 13 of the 15 splits can be done in the plane, 11 with both sides connected
    splits = separations(frame, 31, plane)
    assert len(splits) == 13
    assert len(separations(frame, 31)) == 15
    disconnected = {(0b00111, 0b11000), (0b10001, 0b01110)}
    assert disconnected <= set(splits)


EXAMPLE_COUNTS = {(1, 0, 0): 14, (-1, 0, 0): 14, (0, 1, 0): 30, (0, -1, 0): 30,
                  (0, 0, 1): 8, (0, 0, -1): 8}
