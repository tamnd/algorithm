# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bresenham-line-algorithm/. The authors are listed in prov/VSRX7E.jsonl.

import random
from fractions import Fraction

from bresenham_line_algorithm import bresenham_line


def nearest_pixels(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Brute force: in each step of the major axis, try every minor value and keep the nearest
    to the exact line, computed with Fraction. A tie goes to the value nearer to the start."""
    dx, dy = x1 - x0, y1 - y0
    m = max(abs(dx), abs(dy))
    if m == 0:
        return [(x0, y0)]
    out = []
    for i in range(m + 1):
        if abs(dx) >= abs(dy):
            x = x0 + (i if dx >= 0 else -i)
            exact = y0 + Fraction(dy * (x - x0), dx)
            lo, hi = min(y0, y1), max(y0, y1)
            y = min(range(lo, hi + 1), key=lambda v: (abs(v - exact), abs(v - y0)))
        else:
            y = y0 + (i if dy >= 0 else -i)
            exact = x0 + Fraction(dx * (y - y0), dy)
            lo, hi = min(x0, x1), max(x0, x1)
            x = min(range(lo, hi + 1), key=lambda v: (abs(v - exact), abs(v - x0)))
        out.append((x, y))
    return out


def test_example() -> None:
    assert bresenham_line(0, 0, 8, 3) == [(0, 0), (1, 0), (2, 1), (3, 1), (4, 1), (5, 2), (6, 2), (7, 3), (8, 3)]


def test_reversal_differs_at_a_tie() -> None:
    assert bresenham_line(0, 0, 4, 1) == [(0, 0), (1, 0), (2, 0), (3, 1), (4, 1)]
    assert bresenham_line(4, 1, 0, 0) == [(4, 1), (3, 1), (2, 1), (1, 0), (0, 0)]


def test_edges() -> None:
    assert bresenham_line(3, -2, 3, -2) == [(3, -2)]
    assert bresenham_line(0, 0, 5, 0) == [(i, 0) for i in range(6)]
    assert bresenham_line(0, 0, 0, -4) == [(0, -i) for i in range(5)]
    assert bresenham_line(0, 0, 4, 4) == [(i, i) for i in range(5)]
    assert bresenham_line(0, 0, -3, 3) == [(-i, i) for i in range(4)]
    big = 2**62
    assert bresenham_line(big, big, big + 3, big + 1) == [(big, big), (big + 1, big), (big + 2, big + 1), (big + 3, big + 1)]


def test_all_octants_against_brute_force() -> None:
    for x1 in range(-9, 10):
        for y1 in range(-9, 10):
            assert bresenham_line(0, 0, x1, y1) == nearest_pixels(0, 0, x1, y1)


def test_random_against_brute_force() -> None:
    rng = random.Random(1965)
    for _ in range(600):
        x0, y0, x1, y1 = (rng.randint(-25, 25) for _ in range(4))
        pts = bresenham_line(x0, y0, x1, y1)
        assert pts == nearest_pixels(x0, y0, x1, y1)
        assert pts[0] == (x0, y0) and pts[-1] == (x1, y1)
        for (a, b), (c, d) in zip(pts, pts[1:]):
            assert max(abs(a - c), abs(b - d)) == 1


def test_run_lengths() -> None:
    for dx in range(1, 70):
        for dy in range(1, dx + 1):
            pts = bresenham_line(0, 0, dx, dy)
            runs, length = [], 1
            for (_, a), (_, b) in zip(pts, pts[1:]):
                if a == b:
                    length += 1
                else:
                    runs.append(length)
                    length = 1
            runs.append(length)
            lo, hi = dx // dy, -(-dx // dy)
            assert all(r <= hi for r in runs)
            assert all(lo <= r for r in runs[1:-1])
