# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-and-prune/. The authors are listed in prov/46M4XT.jsonl.

import random

from sweep_and_prune import SweepAndPrune, sort_and_sweep


def brute(boxes):
    out = set()
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]:
                out.add((i, j))
    return out


def inversions(sap, boxes):
    total = 0
    for a in range(2):
        e = [[boxes[x[2]][a + 2 * x[1]], x[1], x[2]] for x in sap.ends[a]]
        total += sum(1 for i in range(len(e)) for j in range(i + 1, len(e)) if e[i] > e[j])
    return total


def page_example():
    return [(0, 0, 4, 2), (3, 1, 6, 5), (5, 4, 8, 6), (9, 0, 10, 3)]


def test_page_example():
    boxes = page_example()
    sap = SweepAndPrune(boxes)
    assert sap.overlapping_pairs() == {(0, 1), (1, 2)}
    assert [(v, k, i) for v, k, i in sap.ends[0]] == [
        (0, 0, 0), (3, 0, 1), (4, 1, 0), (5, 0, 2), (6, 1, 1), (8, 1, 2), (9, 0, 3), (10, 1, 3)
    ]
    assert sap.count == {(0, 1): 2, (1, 2): 2, (0, 3): 1, (1, 3): 1}
    moved = [(0, 0, 4, 2), (3, 1, 6, 5), (5, 4, 8, 6), (5, 2, 6, 5)]  # box 3 moves 4 left and 2 up
    r = sap.update(moved)
    assert r == 6
    assert sap.overlapping_pairs() == brute(moved) == {(0, 1), (1, 2), (1, 3), (2, 3)}
    assert sap.count[(1, 3)] == 2 and sap.count[(2, 3)] == 2 and sap.count[(0, 3)] == 1
    sap.check_invariant()
    again = SweepAndPrune(boxes)
    assert again.update([(0, 0, 4, 2), (3, 1, 6, 5), (5, 4, 8, 6), (7, 0, 8, 3)]) == 1


def test_sort_and_sweep_example():
    assert sort_and_sweep(page_example()) == {(0, 1), (1, 2)}
    assert sort_and_sweep(page_example(), axis=1) == {(0, 1), (1, 2)}


def test_edge_cases():
    assert SweepAndPrune([]).overlapping_pairs() == set()
    assert SweepAndPrune([(0, 0, 1, 1)]).overlapping_pairs() == set()
    touching = [(0, 0, 1, 1), (1, 1, 2, 2)]  # closed boxes that share a corner
    assert SweepAndPrune(touching).overlapping_pairs() == {(0, 1)}
    same = [(0, 0, 1, 1)] * 3
    sap = SweepAndPrune(same)
    assert sap.overlapping_pairs() == {(0, 1), (0, 2), (1, 2)}
    assert sap.update(same) == 0
    points = [(2, 2, 2, 2), (2, 2, 2, 2), (3, 2, 3, 2)]  # degenerate boxes
    sap = SweepAndPrune(points)
    assert sap.overlapping_pairs() == {(0, 1)}


def random_boxes(rng, n, size):
    out = []
    for _ in range(n):
        x, y = rng.randint(0, size), rng.randint(0, size)
        w, h = rng.randint(0, 6), rng.randint(0, 6)
        out.append((x, y, x + w, y + h))
    return out


def test_random_moving_scenes_against_brute_force():
    rng = random.Random(46)
    for _ in range(60):
        n = rng.randint(0, 25)
        boxes = random_boxes(rng, n, 30)
        sap = SweepAndPrune(boxes)
        assert sap.overlapping_pairs() == brute(boxes)
        assert sort_and_sweep(boxes) == brute(boxes)
        vel = [(rng.randint(-2, 2), rng.randint(-2, 2)) for _ in range(n)]
        for _ in range(10):
            boxes = [(b[0] + v[0], b[1] + v[1], b[2] + v[0], b[3] + v[1]) for b, v in zip(boxes, vel)]
            if rng.random() < 0.2:  # sometimes one box jumps far
                k = rng.randrange(n) if n else None
                if k is not None:
                    b = random_boxes(rng, 1, 30)[0]
                    boxes[k] = b
            expected_r = inversions(sap, boxes)
            r = sap.update(boxes)
            assert r == expected_r
            assert sap.overlapping_pairs() == brute(boxes)
            assert sort_and_sweep(boxes, axis=rng.randrange(2)) == brute(boxes)
        sap.check_invariant()


def test_float_boxes():
    rng = random.Random(7)
    for _ in range(100):
        boxes = []
        for _ in range(12):
            x, y = rng.uniform(0, 10), rng.uniform(0, 10)
            boxes.append((x, y, x + rng.uniform(0, 3), y + rng.uniform(0, 3)))
        sap = SweepAndPrune(boxes)
        assert sap.overlapping_pairs() == brute(boxes)
        boxes = [(b[0] + 0.5, b[1], b[2] + 0.5, b[3]) if i % 2 else b for i, b in enumerate(boxes)]
        sap.update(boxes)
        assert sap.overlapping_pairs() == brute(boxes)
