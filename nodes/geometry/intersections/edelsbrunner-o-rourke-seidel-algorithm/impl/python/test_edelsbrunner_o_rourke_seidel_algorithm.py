# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edelsbrunner-o-rourke-seidel-algorithm/. The authors are listed in prov/SQSS70.jsonl.

import random
from fractions import Fraction

import pytest

from edelsbrunner_o_rourke_seidel_algorithm import cross, eos_arrangement, meet, same_line, side


def model_counts(lines):
    """Vertices, edges and faces from the crossing points alone."""
    verts, faces = set(), 1
    for i, l in enumerate(lines):
        here = {meet(l, lines[j]) for j in range(i)} - {None}
        faces += len(here) + 1
        verts |= here
    edges = sum(len({meet(l, k) for k in lines if k is not l} - {None}) + 1 for l in lines)
    return len(verts), edges, faces


def random_lines(rng, n, r):
    out = []
    while len(out) < n:
        a, b, c = rng.randint(-r, r), rng.randint(-r, r), rng.randint(-r, r)
        if (a, b) == (0, 0) or any(same_line((a, b, c), k) for k in out):
            continue
        out.append((a, b, c))
    return out


def check(lines):
    arr = eos_arrangement(lines)
    arr.check_invariant()
    assert arr.counts() == model_counts(lines)
    seen, area = set(), Fraction(0)
    for f in range(1, len(arr.face_edge)):
        pts = arr.face_boundary(f)
        area += sum(cross(pts[i - 1], pts[i]) for i in range(len(pts))) / 2
        c = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
        sv = tuple(side(l, c) for l in lines)
        assert 0 not in sv and sv not in seen
        seen.add(sv)
    assert area == (2 * arr.m) ** 2  # the faces tile the box
    return arr


def test_example():
    # y = 0, x = 0, y = x, x + y = 2 and y = 2, inserted in this order.
    lines = [(0, 1, 0), (1, 0, 0), (-1, 1, 0), (1, 1, 2), (0, 1, 2)]
    arr = check(lines)
    assert arr.m == 3
    assert arr.counts() == (5, 17, 13)
    assert len(arr.points) == 17 and len(arr.origin) // 2 == 29


def test_degenerate():
    check([])
    check([(1, 0, 0)])
    check([(0, 1, 0), (0, 1, 1), (0, 1, -1)])  # parallel
    check([(1, 1, 0), (1, -1, 0), (1, 0, 0), (0, 1, 0), (1, 2, 0)])  # concurrent
    check([(1, -1, 0), (1, 1, 0)])  # both lines through box corners
    check([(1, 0, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1), (1, 0, -1), (0, 1, -1)])
    with pytest.raises(ValueError):
        eos_arrangement([(1, 1, 1), (-2, -2, -2)])


def test_random():
    rng = random.Random(1986)
    for case in range(900):
        n = rng.randint(0, 8)
        r = (1, 2, 4, 9)[case % 4]
        check(random_lines(rng, n, r))


def test_linear_work_per_line():
    # The zone theorem: inserting the i-th line costs O(i) steps.
    rng = random.Random(7)
    for n in (10, 20, 30):
        lines = random_lines(rng, n, 1000)
        arr = eos_arrangement(lines)
        assert arr.steps <= 12 * n * n + 40 * n
