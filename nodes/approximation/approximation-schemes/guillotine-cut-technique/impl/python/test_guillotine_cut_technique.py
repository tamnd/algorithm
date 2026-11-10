# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guillotine-cut-technique/. The authors are listed in prov/Z1DTDF.jsonl.

import random
from fractions import Fraction
from math import comb

from guillotine_cut_technique import (areas, guillotine_partition, has_perfect_cut, is_m_guillotine,
                                      make_m_guillotine, total_length)

# Three horizontal and three vertical lines across the box [0, 8] x [0, 8], each with one gap of length 1.
GAPPED = [("h", 2, 0, 4), ("h", 2, 5, 8), ("h", 4, 0, 5), ("h", 4, 6, 8), ("h", 6, 0, 2), ("h", 6, 3, 8),
          ("v", 2, 0, 1), ("v", 2, 2, 8), ("v", 4, 0, 5), ("v", 4, 6, 8), ("v", 6, 0, 2), ("v", 6, 3, 8)]
BOX = (0, 8, 0, 8)


def unit_edges(rng, size, count):
    edges = set()
    while len(edges) < count:
        c, t = rng.randrange(1, size), rng.randrange(size)
        edges.add(("h", c, t, t + 1) if rng.random() < 0.5 else ("v", c, t, t + 1))
    return sorted(edges)


def gapped(rng, size, lines):
    segs = []
    for axis in ("h", "v"):
        for c in lines:
            g = rng.randrange(size)
            segs += [(axis, c, 0, g)] if g > 0 else []
            segs += [(axis, c, g + 1, size)] if g + 1 < size else []
    return segs


def contains(big, small):
    """Every segment of small lies on the union of big."""
    return total_length(list(big) + list(small)) == total_length(big)


def test_example() -> None:
    assert total_length(GAPPED) == 42
    assert has_perfect_cut(GAPPED, BOX, 1) == []
    assert not is_m_guillotine(GAPPED, BOX, 1)
    assert is_m_guillotine(GAPPED, BOX, 2) and is_m_guillotine(GAPPED, BOX, 3)
    stats = {}
    out = make_m_guillotine(GAPPED, BOX, 1, stats)
    paid = [(w, axis, c, f, h) for w, axis, c, f, h in stats["cuts"] if f > 0]
    assert paid == [(BOX, "x", Fraction(5, 2), 2, 7)]
    assert total_length(out) == 44 and out[-1] == ("v", Fraction(5, 2), 2, 4)
    assert is_m_guillotine(out, BOX, 1)
    assert areas(GAPPED, BOX, "x", 1) == (28, 28) and areas(GAPPED, BOX, "y", 1) == (28, 28)
    assert total_length(make_m_guillotine(GAPPED, BOX, 2)) == 42


def test_length_bound_for_several_m() -> None:
    rng = random.Random(1999)
    for trial in range(24):
        if trial % 2:
            size = 6
            segs = unit_edges(rng, size, rng.randint(3, 16))
        else:
            size = 8
            segs = gapped(rng, size, (2, 4, 6))
        box = (0, size, 0, size)
        length = total_length(segs)
        for m in (1, 2, 3):
            stats = {}
            out = make_m_guillotine(segs, box, m, stats)
            assert contains(out, segs)
            assert total_length(out) - length <= Fraction(length, m)
            assert all(f <= h for _, _, _, f, h in stats["cuts"])
            assert is_m_guillotine(out, box, m)


def test_two_ways_to_measure_the_dark_region() -> None:
    rng = random.Random(1996)
    for _ in range(40):
        size = rng.choice([4, 6])
        segs = unit_edges(rng, size, rng.randint(2, 14))
        box = (0, size, 0, size)
        for m in (1, 2):
            fx, hx = areas(segs, box, "x", m)
            fy, hy = areas(segs, box, "y", m)
            assert fx == hy and fy == hx  # each area is measured once by columns and once by rows
            assert (hx - fx) + (hy - fy) == 0  # so one direction has h - f >= 0 in total


# A brute force over all partitions of the box into rectangles with edges on the grid of the point coordinates.

def grid(points, width, height):
    return sorted({0, width} | {p[0] for p in points}), sorted({0, height} | {p[1] for p in points})


def best_grid_partition(points, width, height):
    xs, ys = grid(points, width, height)
    nx, ny = len(xs), len(ys)
    need = {(xs.index(p[0]), ys.index(p[1])) for p in points}
    verts = [(i, j) for j in range(1, ny - 1) for i in range(1, nx - 1)]
    best = [float("inf"), None]
    chosen: dict = {}

    def ok(i, j):
        left, right = chosen[("h", j, i - 1)], chosen[("h", j, i)]
        down, up = chosen[("v", i, j - 1)], chosen[("v", i, j)]
        deg = left + right + down + up
        if deg == 1 or (deg == 2 and not (left and right) and not (down and up)):
            return False
        return deg > 0 or (i, j) not in need

    def length(e):
        return xs[e[2] + 1] - xs[e[2]] if e[0] == "h" else ys[e[2] + 1] - ys[e[2]]

    def go(k, cost):
        if cost >= best[0]:
            return
        if k == len(verts):
            best[0], best[1] = cost, [e for e, b in chosen.items() if b]
            return
        i, j = verts[k]
        free = [("h", j, i), ("v", i, j)] + ([("h", j, 0)] if i == 1 else []) + ([("v", i, 0)] if j == 1 else [])
        for mask in range(1 << len(free)):
            add = 0
            for t, e in enumerate(free):
                chosen[e] = (mask >> t) & 1
                add += length(e) * chosen[e]
            if ok(i, j):
                go(k + 1, cost + add)
        for e in free:
            del chosen[e]

    go(0, 0)
    segs = [("h", ys[e[1]], xs[e[2]], xs[e[2] + 1]) if e[0] == "h" else ("v", xs[e[1]], ys[e[2]], ys[e[2] + 1])
            for e in best[1]]
    return best[0], segs


def all_guillotine_lengths(points, width, height):
    """The lengths of all guillotine partitions with cuts on the grid, by recursion without a table."""
    xs, ys = grid(points, width, height)

    def rec(i0, i1, j0, j1):
        if not any(xs[i0] < p[0] < xs[i1] and ys[j0] < p[1] < ys[j1] for p in points):
            return {0}
        out = set()
        for i in range(i0 + 1, i1):
            out |= {ys[j1] - ys[j0] + a + b for a in rec(i0, i, j0, j1) for b in rec(i, i1, j0, j1)}
        for j in range(j0 + 1, j1):
            out |= {xs[i1] - xs[i0] + a + b for a in rec(i0, i1, j0, j) for b in rec(i0, i1, j, j1)}
        return out

    return rec(0, len(xs) - 1, 0, len(ys) - 1)


def test_partition_dynamic_program() -> None:
    rng = random.Random(1986)
    for _ in range(30):
        width, height = rng.randint(4, 9), rng.randint(4, 9)
        n = rng.randint(1, 4)
        points = sorted({(rng.randint(1, width - 1), rng.randint(1, height - 1)) for _ in range(n)})
        stats = {}
        value, segs = guillotine_partition(points, width, height, stats)
        assert value == min(all_guillotine_lengths(points, width, height)) == total_length(segs)
        opt, opt_segs = best_grid_partition(points, width, height)
        assert opt <= value
        box = (0, width, 0, height)
        assert is_m_guillotine(segs, box, 1)
        one = make_m_guillotine(opt_segs, box, 1)
        assert is_m_guillotine(one, box, 1) and total_length(one) <= 2 * opt
        xs, ys = len({0, width} | {p[0] for p in points}), len({0, height} | {p[1] for p in points})
        assert stats["windows"] == comb(xs, 2) * comb(ys, 2) <= comb(len(points) + 2, 2) ** 2
        assert stats["transitions"] <= stats["windows"] * (xs + ys - 4)


def test_partition_example() -> None:
    points = [(1, 2), (2, 4), (3, 1), (4, 3)]
    stats = {}
    value, segs = guillotine_partition(points, 5, 5, stats)
    opt, opt_segs = best_grid_partition(points, 5, 5)
    assert (value, opt) == (13, 12)
    assert sorted(segs) == [("h", 1, 2, 5), ("h", 2, 0, 2), ("h", 3, 2, 5), ("v", 2, 0, 5)]
    assert stats == {"windows": 225, "transitions": 320}
    # the optimum is a pinwheel: not a guillotine partition, but 1-guillotine as it is
    assert is_m_guillotine(opt_segs, (0, 5, 0, 5), 1)
    assert total_length(make_m_guillotine(opt_segs, (0, 5, 0, 5), 1)) == 12
