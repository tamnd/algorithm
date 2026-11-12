# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-area-heuristic/. The authors are listed in prov/948WA8.jsonl.

import math
import random
from fractions import Fraction

from surface_area_heuristic import (
    area,
    best_sweep_split,
    line_hits_box,
    random_line,
    tree_cost,
    tree_cost_recursive_form,
    union,
)


def unit(c):
    return ((c, 0, 0), (c + 1, 1, 1))


def box_of(boxes, ids):
    b = None
    for i in ids:
        b = union(b, boxes[i])
    return b


def leaf(boxes, ids):
    return {"box": box_of(boxes, ids), "count": len(ids)}


def inner(*children):
    b = None
    for c in children:
        b = union(b, c["box"])
    return {"box": b, "children": list(children)}


def test_example() -> None:
    boxes = [unit(c) for c in (0, 1, 2, 3, 4, 18)]
    assert area(box_of(boxes, range(6))) == 78
    sah = inner(inner(leaf(boxes, [0, 1]), inner(leaf(boxes, [2]), leaf(boxes, [3, 4]))), leaf(boxes, [5]))
    assert tree_cost(sah) == Fraction(114 + 52, 78) == tree_cost_recursive_form(sah)
    median = inner(leaf(boxes, [0, 1, 2]), leaf(boxes, [3, 4, 5]))
    assert tree_cost(median) == Fraction(78 + 14 * 3 + 66 * 3, 78)
    cost, k, order = best_sweep_split(boxes)
    assert (cost, k, order) == (1 + Fraction(22 * 5 + 6, 78), 5, [0, 1, 2, 3, 4, 5])
    assert best_sweep_split([unit(0), unit(0)])[1] == 2  # two equal boxes: a leaf is cheaper


def direct_best(boxes, c_trav, c_isect):
    n = len(boxes)
    a_s = area(box_of(boxes, range(n)))
    best = Fraction(c_isect * n)
    for axis in range(3):
        order = sorted(range(n), key=lambda i: boxes[i][0][axis] + boxes[i][1][axis])
        for i in range(1, n):
            left, right = order[:i], order[i:]
            cost = c_trav + c_isect * Fraction(area(box_of(boxes, left)) * i + area(box_of(boxes, right)) * (n - i)) / a_s
            best = min(best, cost)
    return best


def test_sweep_against_direct() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 20)
        boxes = []
        for _ in range(n):
            lo = [rng.randint(0, 30) for _ in range(3)]
            boxes.append((tuple(lo), tuple(x + rng.randint(0, 6) for x in lo)))
        if area(box_of(boxes, range(n))) == 0:
            continue
        ct, ci = rng.choice([(1, 1), (Fraction(1, 2), 1), (1, 3)])
        cost, k, order = best_sweep_split(boxes, ct, ci)
        assert cost == direct_best(boxes, ct, ci)
        if k < n:  # the reported split has the reported cost
            left, right = order[:k], order[k:]
            a = Fraction(area(box_of(boxes, left)) * k + area(box_of(boxes, right)) * (n - k))
            assert cost == ct + ci * a / area(box_of(boxes, range(n)))


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        lo = [rng.randint(0, 20) for _ in range(3)]
        return {"box": (tuple(lo), tuple(x + rng.randint(1, 5) for x in lo)), "count": rng.randint(1, 4)}
    return inner(*[random_tree(rng, depth - 1) for _ in range(rng.choice([2, 2, 4]))])


def test_two_forms_of_the_cost() -> None:
    rng = random.Random(9)
    for _ in range(200):
        t = random_tree(rng, 5)
        ct, ci = rng.choice([(1, 1), (Fraction(1, 3), 2)])
        assert tree_cost(t, ct, ci) == tree_cost_recursive_form(t, ct, ci)


def test_area_ratio_is_the_hit_probability() -> None:
    a_box = ([0.0, 0.0, 0.0], [4.0, 2.0, 1.0])
    inner_boxes = [([1.0, 0.0, 0.0], [2.0, 1.0, 1.0]), ([0.0, 0.0, 0.5], [2.0, 2.0, 0.5]), ([3.0, 1.5, 0.2], [3.5, 1.7, 0.9])]
    rng = random.Random(2024)
    center = [2.0, 1.0, 0.5]
    radius = math.sqrt(4 + 1 + 0.25)  # half the diagonal: every line that meets A passes this close to the center
    hits_a = 0
    hits = [0] * len(inner_boxes)
    for _ in range(60000):
        p, u = random_line(rng, center, radius)
        if not line_hits_box(p, u, a_box):
            continue
        hits_a += 1
        for k, b in enumerate(inner_boxes):
            hits[k] += line_hits_box(p, u, b)
    sa = lambda b: 2 * sum((b[1][i] - b[0][i]) * (b[1][(i + 1) % 3] - b[0][(i + 1) % 3]) for i in range(3))
    assert hits_a > 20000
    for k, b in enumerate(inner_boxes):
        p = sa(b) / sa(a_box)
        se = math.sqrt(p * (1 - p) / hits_a)
        assert abs(hits[k] / hits_a - p) < 4 * se
