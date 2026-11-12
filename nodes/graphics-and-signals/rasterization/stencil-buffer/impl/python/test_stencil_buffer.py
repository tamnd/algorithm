# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stencil-buffer/. The authors are listed in prov/A59S6S.jsonl.

import random
from fractions import Fraction

import pytest

from stencil_buffer import FUNCS, OPS, StencilBuffer, fill_path, triangle_pixels

K = 10**6


def winding(rings, px, py):
    """Winding number by the crossing test of Sunday, in exact arithmetic."""
    w = 0
    for ring in rings:
        n = len(ring)
        for k in range(n):
            (ax, ay), (bx, by) = ring[k], ring[(k + 1) % n]
            side = (bx - ax) * (py - ay) - (px - ax) * (by - ay)
            if ay <= py:
                if by > py and side > 0:
                    w += 1
            elif by <= py and side < 0:
                w -= 1
    return w


def moved_center(i, j):
    return Fraction(2 * i + 1, 2) + Fraction(1, K), Fraction(2 * j + 1, 2) + Fraction(1, K * K)


STAR = [(5, 0), (8, 10), (0, 4), (10, 4), (2, 10)]


def test_ops_match_definitions():
    for bits in (1, 3, 8):
        top = (1 << bits) - 1
        for s in sorted({0, 1, top - 1, top} & set(range(top + 1))):
            for op in OPS:
                sb = StencilBuffer(1, 1, bits)
                sb.set_func("ALWAYS", 2, top)
                sb.values[0][0] = s
                sb.set_op("KEEP", "KEEP", op)
                sb.fragment(0, 0)
                expect = {
                    "KEEP": s, "ZERO": 0, "REPLACE": min(2, top),
                    "INCR": min(s + 1, top), "INCR_WRAP": (s + 1) % (top + 1),
                    "DECR": max(s - 1, 0), "DECR_WRAP": (s - 1) % (top + 1),
                    "INVERT": top - s,
                }[op]
                assert sb.values[0][0] == expect, (bits, s, op)


def test_funcs_and_masks():
    rng = random.Random(1990)
    for _ in range(2000):
        sb = StencilBuffer(1, 1, 8)
        func = rng.choice(list(FUNCS))
        ref, mask, s = rng.randint(-5, 300), rng.randint(0, 255), rng.randint(0, 255)
        sb.values[0][0] = s
        sb.set_func(func, ref, mask)
        r = min(max(ref, 0), 255) & mask
        assert sb.test(0, 0) == FUNCS[func](r, s & mask)
    sb = StencilBuffer(1, 1, 8)
    sb.set_func("LESS", 3, 255)
    sb.values[0][0] = 5
    assert sb.test(0, 0)  # LESS passes when ref < stored
    sb.values[0][0] = 3
    assert not sb.test(0, 0)


def test_which_op_runs_and_write_mask():
    sb = StencilBuffer(1, 1, 8)
    sb.set_op("REPLACE", "INCR", "DECR_WRAP")
    sb.set_func("NEVER", 7, 255)
    assert not sb.fragment(0, 0)
    assert sb.values[0][0] == 7  # sfail
    sb.set_func("ALWAYS", 7, 255)
    assert not sb.fragment(0, 0, depth_pass=False)
    assert sb.values[0][0] == 8  # dpfail
    assert sb.fragment(0, 0)
    assert sb.values[0][0] == 7  # dppass
    sb.write_mask = 0b11110000
    sb.set_op("KEEP", "KEEP", "INVERT")
    sb.fragment(0, 0)
    assert sb.values[0][0] == 0b11110111  # only the high four bits flip
    sb.set_op("KEEP", "KEEP", "ZERO", "BACK")
    sb.write_mask = 255
    sb.fragment(0, 0, front=False)
    assert sb.values[0][0] == 0


def test_bad_arguments():
    with pytest.raises(ValueError):
        StencilBuffer(1, 1, 0)
    with pytest.raises(ValueError):
        StencilBuffer(1, 1).set_op("KEEP", "KEEP", "ADD")
    with pytest.raises(ValueError):
        StencilBuffer(1, 1).set_func("SOMETIMES", 0, 1)
    with pytest.raises(ValueError):
        fill_path([STAR], 4, 4, "positive")


def test_shared_edge_covered_once():
    a, b, c, d = (1, 1), (7, 2), (6, 7), (0, 5)
    t1 = set(triangle_pixels(a, b, c, 8, 8))
    t2 = set(triangle_pixels(a, c, d, 8, 8))
    assert not (t1 & t2)
    assert triangle_pixels((0, 0), (4, 4), (8, 8), 8, 8) == []


def test_star_page_example():
    covered, sb = fill_path([STAR], 11, 11, "nonzero")
    assert sb.values[5][5] == 2  # the center pentagon is covered twice by front-facing fan triangles
    assert (5, 5) in covered
    odd, _ = fill_path([STAR], 11, 11, "evenodd")
    assert (5, 5) not in odd
    assert odd < covered


def test_random_against_winding_numbers():
    rng = random.Random(2012)
    for _ in range(60):
        width, height = rng.randint(1, 10), rng.randint(1, 10)
        rings = [[(Fraction(rng.randint(-8, 48), 4), Fraction(rng.randint(-8, 48), 4)) for _ in range(rng.randint(3, 7))]
                 for _ in range(rng.randint(1, 2))]
        nonzero, sb = fill_path(rings, width, height, "nonzero")
        odd, _ = fill_path(rings, width, height, "evenodd")
        for j in range(height):
            for i in range(width):
                w = winding(rings, *moved_center(i, j))
                assert sb.values[j][i] == w % 256
                assert ((i, j) in nonzero) == (w != 0)
                assert ((i, j) in odd) == (w % 2 == 1)


def test_saturating_ops_give_wrong_counts():
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    back_then_front = [square[::-1], square]  # winding number 0 everywhere
    good, _ = fill_path(back_then_front, 4, 4, "nonzero")
    bad, _ = fill_path(back_then_front, 4, 4, "nonzero", saturate=True)
    assert good == set()
    assert len(bad) == 16  # DECR stayed at 0, then INCR made 1


def test_too_few_bits():
    # One bit: the count is kept mod 2, so the nonzero rule turns into the even-odd rule.
    one_bit, _ = fill_path([STAR], 11, 11, "nonzero", bits=1)
    odd, _ = fill_path([STAR], 11, 11, "evenodd")
    assert one_bit == odd
    # Two bits: four copies of a square give winding 4, which wraps to 0.
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    covered, _ = fill_path([square] * 4, 4, 4, "nonzero", bits=2)
    assert covered == set()
