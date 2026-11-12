# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/digital-differential-analyzer/. The authors are listed in prov/QJ39WT.jsonl.

import math
import random
from fractions import Fraction

from digital_differential_analyzer import dda_line


def exact_points(x0: int, y0: int, x1: int, y1: int) -> list[tuple[Fraction, Fraction]]:
    """The exact sample points of the DDA: the start plus i times the exact increment."""
    n = max(abs(x1 - x0), abs(y1 - y0))
    if n == 0:
        return [(Fraction(x0), Fraction(y0))]
    return [(x0 + Fraction((x1 - x0) * i, n), y0 + Fraction((y1 - y0) * i, n)) for i in range(n + 1)]


def is_tie(v: Fraction) -> bool:
    return v - math.floor(v) == Fraction(1, 2)


def check_against_exact(x0: int, y0: int, x1: int, y1: int, single: bool = False) -> bool:
    """True if each pixel is the exact point rounded half up, and at a tie one of the two pixels.

    The exact coordinate c0 + (c1 - c0) i / n is handled as the integer fraction (c0 n + (c1 - c0) i) / n."""
    got = dda_line(x0, y0, x1, y1, single)
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    if len(got) != max(abs(x1 - x0), abs(y1 - y0)) + 1:
        return False
    for i, (gx, gy) in enumerate(got):
        for g, c0, c1 in ((gx, x0, x1), (gy, y0, y1)):
            num = c0 * n + (c1 - c0) * i
            up = (2 * num + n) // (2 * n)
            if (2 * num + n) % (2 * n) == 0:
                if g not in (up - 1, up):
                    return False
            elif g != up:
                return False
    return True


def test_exact_check_agrees_with_fraction() -> None:
    rng = random.Random(3)
    for _ in range(300):
        x0, y0, x1, y1 = (rng.randint(-20, 20) for _ in range(4))
        ref = exact_points(x0, y0, x1, y1)
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i, (ex, ey) in enumerate(ref):
            for e, c0, c1 in ((ex, x0, x1), (ey, y0, y1)):
                num = c0 * n + (c1 - c0) * i
                assert is_tie(e) == ((2 * num + n) % (2 * n) == 0)
                assert math.floor(e + Fraction(1, 2)) == (2 * num + n) // (2 * n)


def test_example() -> None:
    assert dda_line(0, 0, 8, 3) == [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2), (6, 2), (7, 3), (8, 3)]


def test_edges() -> None:
    assert dda_line(4, -7, 4, -7) == [(4, -7)]
    assert dda_line(0, 0, 0, 3) == [(0, 0), (0, 1), (0, 2), (0, 3)]
    assert dda_line(0, 0, -3, -3) == [(0, 0), (-1, -1), (-2, -2), (-3, -3)]
    assert dda_line(2, 5, -2, 3) == [(2, 5), (1, 5), (0, 4), (-1, 4), (-2, 3)]


def test_float64_matches_exact_rounding_off_ties() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        x0, y0, x1, y1 = (rng.randint(-3000, 3000) for _ in range(4))
        assert check_against_exact(x0, y0, x1, y1)
    for x1 in range(-15, 16):
        for y1 in range(-15, 16):
            assert check_against_exact(0, 0, x1, y1)


def test_endpoints_are_exact() -> None:
    rng = random.Random(7)
    for _ in range(500):
        x0, y0, x1, y1 = (rng.randint(-10**6, 10**6) for _ in range(4))
        n = max(abs(x1 - x0), abs(y1 - y0))
        if n > 4000:
            x1, y1 = x0 + (x1 - x0) % 4000, y0 - (y1 - y0) % 4000
        pts = dda_line(x0, y0, x1, y1)
        assert pts[0] == (x0, y0) and pts[-1] == (x1, y1)


def test_float64_tie_goes_down() -> None:
    # The exact point (7, 1/2) is a tie. Seven additions of fl(1/14) give a value below 1/2.
    assert dda_line(0, 0, 14, 1)[7] == (7, 0)


def test_float32_drift_changes_a_pixel() -> None:
    pts = dda_line(0, 0, 353, 337, single=True)
    exact = Fraction(337 * 342, 353)
    assert not is_tie(exact) and math.floor(exact + Fraction(1, 2)) == 326
    assert pts[342] == (342, 327)
    assert dda_line(0, 0, 353, 337)[342] == (342, 326)


def test_python_round_is_not_half_up() -> None:
    assert [round(v) for v in (0.5, 1.5, 2.5)] == [0, 2, 2]
    assert [math.floor(v + 0.5) for v in (0.5, 1.5, 2.5)] == [1, 2, 3]
