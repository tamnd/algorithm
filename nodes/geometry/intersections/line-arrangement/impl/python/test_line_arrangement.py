# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/line-arrangement/. The authors are listed in prov/FB22MJ.jsonl.

import random
from fractions import Fraction

import pytest

from line_arrangement import LineArrangement, meet, same_line, side


def model_counts(lines):
    """Vertices, edges and faces from the crossing points alone.

    Adding a line that meets the earlier lines in k distinct points cuts it
    into k + 1 edges, and each edge splits one face in two."""
    verts = set()
    faces = 1
    for i, l in enumerate(lines):
        here = {meet(l, lines[j]) for j in range(i)} - {None}
        faces += len(here) + 1
        verts |= here
    edges = 0
    for i, l in enumerate(lines):
        on = {meet(l, lines[j]) for j in range(len(lines)) if j != i} - {None}
        edges += len(on) + 1
    return len(verts), edges, faces


def sign_vector(lines, p):
    return tuple(side(l, p) for l in lines)


def random_lines(rng, n, r):
    out = []
    while len(out) < n:
        a, b = rng.randint(-r, r), rng.randint(-r, r)
        if a == 0 and b == 0:
            continue
        c = rng.randint(-r, r)
        l = (a, b, c)
        if any(same_line(l, k) for k in out):
            continue
        out.append(l)
    return out


def check(lines, rng=None, probes=0):
    arr = LineArrangement(lines)
    arr.check_invariant()
    assert arr.counts() == model_counts(lines)
    # Each face of the box has its own sign vector, and no face is missing.
    seen = set()
    for f in range(1, len(arr.cycles)):
        pts = arr.face_boundary(f)
        c = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
        assert arr.locate(c) == f
        sv = sign_vector(lines, c)
        assert 0 not in sv and sv not in seen
        seen.add(sv)
    assert len(seen) == arr.counts()[2]
    if rng is not None:
        by_sign = {}
        for _ in range(probes):
            m = arr.m
            p = (Fraction(rng.randint(-2 * m + 1, 2 * m - 1), 2),
                 Fraction(rng.randint(-2 * m + 1, 2 * m - 1), 2))
            f = arr.locate(p)
            sv = sign_vector(lines, p)
            if f is None:
                assert 0 in sv
                continue
            assert by_sign.setdefault(sv, f) == f
    return arr


def test_example():
    # y = 0, x = 0, y = x, x + y = 2 and y = 2.
    lines = [(0, 1, 0), (1, 0, 0), (-1, 1, 0), (1, 1, 2), (0, 1, 2)]
    arr = check(lines)
    assert arr.counts() == (5, 17, 13)
    assert arr.m == 3
    p0 = (Fraction(0), Fraction(0))
    deg = len(arr.rotation[arr.points.index(p0)])
    assert deg == 6  # three lines through the origin
    tri = arr.locate((Fraction(1, 2), Fraction(1, 4)))
    assert sorted(arr.face_boundary(tri)) == [(0, 0), (1, 1), (2, 0)]


def test_degenerate():
    check([])
    check([(1, 0, 3)])
    check([(1, 0, 0), (1, 0, 1), (1, 0, -5)])  # all parallel
    check([(1, 1, 0), (1, -1, 0), (1, 0, 0), (0, 1, 0)])  # all through one point
    check([(1, 0, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1)])  # a grid
    check([(1, 1, 0), (1, 1, 4), (1, -1, 0)])
    with pytest.raises(ValueError):
        LineArrangement([(1, 2, 3), (2, 4, 6)])
    with pytest.raises(ValueError):
        LineArrangement([(0, 0, 1)])


def test_random():
    rng = random.Random(20261109)
    for case in range(700):
        n = rng.randint(0, 7)
        r = 1 if case % 3 == 0 else (2 if case % 3 == 1 else 5)
        check(random_lines(rng, n, r), rng, probes=15)
