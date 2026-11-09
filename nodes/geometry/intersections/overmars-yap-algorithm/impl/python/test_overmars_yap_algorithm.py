# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overmars-yap-algorithm/. The authors are listed in prov/6722KQ.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from overmars_yap_algorithm import klee_measure, union_length


def brute(boxes):
    """Volume of the union over the grid of compressed cells."""
    d = len(boxes[0])
    axes = [sorted({v for b in boxes for v in b[j]}) for j in range(d)]
    total = 0
    for idx in itertools.product(*[range(len(a) - 1) for a in axes]):
        cell = [(axes[j][i], axes[j][i + 1]) for j, i in enumerate(idx)]
        if any(all(b[j][0] <= cell[j][0] and cell[j][1] <= b[j][1] for j in range(d)) for b in boxes):
            v = 1
            for lo, hi in cell:
                v *= hi - lo
            total += v
    return total


def inclusion_exclusion(boxes):
    d = len(boxes[0])
    total = 0
    for r in range(1, len(boxes) + 1):
        for sub in itertools.combinations(boxes, r):
            v = 1
            for j in range(d):
                lo, hi = max(b[j][0] for b in sub), min(b[j][1] for b in sub)
                v *= max(0, hi - lo)
            total += (-1) ** (r + 1) * v
    return total


def test_example():
    r1 = ((0, 4), (0, 2))
    r2 = ((2, 6), (1, 3))
    vol, solver = klee_measure([r1, r2], keep_trace=True)
    assert vol == 14
    assert solver.trace == [
        (((0, 2), (0, 3)), "trellis", 4),
        (((2, 6), (0, 2)), "trellis", 6),
        (((2, 6), (2, 3)), "covered", 4),
    ]
    r3 = ((1, 3), (-1, 4))
    assert klee_measure([r1, r2, r3])[0] == 19 == brute([r1, r2, r3])
    assert union_length([(1, 3), (2, 5), (6, 7)]) == 5


def test_degenerate():
    assert klee_measure([])[0] == 0
    with pytest.raises(ValueError):
        klee_measure([((0, 1), (2, 1))])
    assert klee_measure([((0, 0), (0, 5))])[0] == 0  # flat box
    assert klee_measure([((0, 2), (0, 2))] * 4)[0] == 4  # equal boxes
    assert klee_measure([((0, 1),), ((1, 2),), ((5, 6),)])[0] == 3  # touching intervals
    assert klee_measure([((0, 2), (0, 2), (0, 2)), ((2, 4), (0, 2), (0, 2))])[0] == 16  # shared face
    cross = [((0, 3), (1, 2), (1, 2)), ((1, 2), (0, 3), (1, 2)), ((1, 2), (1, 2), (0, 3))]
    assert klee_measure(cross)[0] == 7 == brute(cross)  # three piles through a common cube
    half = [((Fraction(0), Fraction(1, 2)), (Fraction(0), Fraction(3))), ((Fraction(1, 3), Fraction(1)), (Fraction(1), Fraction(2)))]
    assert klee_measure(half)[0] == brute(half) == Fraction(3, 2) + Fraction(1, 2)


def test_random():
    rng = random.Random(11)
    for case in range(900):
        d = (1, 2, 3, 4)[case % 4]
        n = rng.randint(1, 9 if d <= 3 else 6)
        k = rng.choice([3, 6, 20])
        boxes = []
        for _ in range(n):
            b = []
            for _ in range(d):
                lo, hi = sorted((rng.randint(0, k), rng.randint(0, k)))
                if rng.random() < 0.3:
                    lo, hi = 0, k  # a full side makes piles common
                b.append((lo, hi))
            boxes.append(tuple(b))
        if rng.random() < 0.2:
            boxes.append(boxes[0])
        vol, solver = klee_measure(boxes)
        assert vol == brute(boxes)
        if n <= 7:
            assert vol == inclusion_exclusion(boxes)
        if solver is not None:
            assert solver.max_depth <= 2 * d * len(boxes)
