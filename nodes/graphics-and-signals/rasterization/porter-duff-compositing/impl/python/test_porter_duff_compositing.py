# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/porter-duff-compositing/. The authors are listed in prov/BSR165.jsonl.

import random
from fractions import Fraction as F

from porter_duff_compositing import (
    OPERATORS,
    composite_pixel,
    darken,
    dissolve,
    opaque,
    over,
    plus,
    porter_duff_compositing,
    premultiply,
    unpremultiply,
)

# The quadruple of Porter and Duff: which picture shows in the regions
# (neither, A only, B only, both). 0 means nothing.
QUADRUPLE = {
    "clear": ("0", "0", "0", "0"),
    "A": ("0", "A", "0", "A"),
    "B": ("0", "0", "B", "B"),
    "A over B": ("0", "A", "B", "A"),
    "B over A": ("0", "A", "B", "B"),
    "A in B": ("0", "0", "0", "A"),
    "B in A": ("0", "0", "0", "B"),
    "A out B": ("0", "A", "0", "0"),
    "B out A": ("0", "0", "B", "0"),
    "A atop B": ("0", "0", "B", "A"),
    "B atop A": ("0", "A", "0", "B"),
    "A xor B": ("0", "A", "B", "0"),
}


def region_oracle(op, color_a, alpha_a, color_b, alpha_b):
    """Exact area algebra: B splits each region of A in the ratio alpha_b to 1 - alpha_b."""
    areas = (
        (1 - alpha_a) * (1 - alpha_b),
        alpha_a * (1 - alpha_b),
        (1 - alpha_a) * alpha_b,
        alpha_a * alpha_b,
    )
    color = [F(0)] * len(color_a)
    alpha = F(0)
    for area, who in zip(areas, QUADRUPLE[op]):
        if who == "0":
            continue
        src = color_a if who == "A" else color_b
        color = [c + area * s for c, s in zip(color, src)]
        alpha += area
    return tuple(color) + (alpha,)


def grid_oracle(op, color_a, p, color_b, q, m):
    """Brute force on an m by m subpixel grid: A covers the first p columns, B the first q rows."""
    color = [F(0)] * len(color_a)
    alpha = F(0)
    for row in range(m):
        for col in range(m):
            in_a, in_b = col < p, row < q
            region = (1 if in_a else 0) + (2 if in_b else 0)
            who = QUADRUPLE[op][region]
            if who == "0":
                continue
            src = color_a if who == "A" else color_b
            color = [c + s for c, s in zip(color, src)]
            alpha += 1
    n = m * m
    return tuple(c / n for c in color) + (alpha / n,)


def test_example() -> None:
    a = (F(1, 2), F(0), F(0), F(1, 2))
    b = (F(0), F(0), F(3, 4), F(3, 4))
    want = {
        "A over B": (F(1, 2), 0, F(3, 8), F(7, 8)),
        "B over A": (F(1, 8), 0, F(3, 4), F(7, 8)),
        "A in B": (F(3, 8), 0, 0, F(3, 8)),
        "A out B": (F(1, 8), 0, 0, F(1, 8)),
        "A atop B": (F(3, 8), 0, F(3, 8), F(3, 4)),
        "A xor B": (F(1, 8), 0, F(3, 8), F(1, 2)),
    }
    for op, w in want.items():
        assert composite_pixel(op, a, b) == w


def test_edges() -> None:
    clear = (F(0),) * 4
    red = (F(1), F(0), F(0), F(1))
    for op in OPERATORS:
        assert composite_pixel(op, clear, clear) == clear
    assert over(red, (F(0), F(1), F(0), F(1))) == red
    assert over(clear, red) == red
    assert over(red, clear) == red
    assert porter_duff_compositing("A over B", [], []) == []
    try:
        porter_duff_compositing("A over B", [[red]], [[red, red]])
    except ValueError:
        pass
    else:
        raise AssertionError("size mismatch not caught")


def test_operators_against_region_algebra() -> None:
    rng = random.Random(1984)
    for _ in range(600):
        alpha_a = F(rng.randint(0, 12), 12)
        alpha_b = F(rng.randint(0, 12), 12)
        color_a = tuple(F(rng.randint(0, 9), 9) for _ in range(3))
        color_b = tuple(F(rng.randint(0, 9), 9) for _ in range(3))
        pa, pb = premultiply(color_a, alpha_a), premultiply(color_b, alpha_b)
        for op in OPERATORS:
            assert composite_pixel(op, pa, pb) == region_oracle(op, color_a, alpha_a, color_b, alpha_b)


def test_operators_against_subpixel_grid() -> None:
    rng = random.Random(253)
    for _ in range(500):
        m = rng.randint(1, 6)
        p, q = rng.randint(0, m), rng.randint(0, m)
        color_a = tuple(F(rng.randint(0, 5), 5) for _ in range(3))
        color_b = tuple(F(rng.randint(0, 5), 5) for _ in range(3))
        pa, pb = premultiply(color_a, F(p, m)), premultiply(color_b, F(q, m))
        op = rng.choice(list(OPERATORS))
        assert composite_pixel(op, pa, pb) == grid_oracle(op, color_a, p, color_b, q, m)


def test_images() -> None:
    rng = random.Random(7)
    for _ in range(50):
        h, w = rng.randint(1, 4), rng.randint(1, 4)

        def image():
            out = []
            for _ in range(h):
                out.append([premultiply((F(rng.randint(0, 4), 4),) * 3, F(rng.randint(0, 4), 4)) for _ in range(w)])
            return out

        ia, ib = image(), image()
        op = rng.choice(list(OPERATORS))
        res = porter_duff_compositing(op, ia, ib)
        for i in range(h):
            for j in range(w):
                assert res[i][j] == composite_pixel(op, ia[i][j], ib[i][j])


def test_over_is_associative() -> None:
    rng = random.Random(18)

    def pixel():
        alpha = F(rng.randint(0, 8), 8)
        return premultiply(tuple(F(rng.randint(0, 8), 8) for _ in range(3)), alpha)

    for _ in range(1000):
        a, b, c = pixel(), pixel(), pixel()
        assert over(over(a, b), c) == over(a, over(b, c))


def test_results_stay_premultiplied() -> None:
    rng = random.Random(3)
    for _ in range(500):
        a = premultiply(tuple(F(rng.randint(0, 6), 6) for _ in range(3)), F(rng.randint(0, 6), 6))
        b = premultiply(tuple(F(rng.randint(0, 6), 6) for _ in range(3)), F(rng.randint(0, 6), 6))
        for op in OPERATORS:
            r = composite_pixel(op, a, b)
            assert 0 <= r[-1] <= 1
            assert all(0 <= c <= r[-1] for c in r[:-1])


def test_straight_alpha_blend_is_not_associative() -> None:
    def naive(x, y):
        (cx, ax), (cy, ay) = x, y
        return (ax * cx + (1 - ax) * cy, ax + ay - ax * ay)

    a, b, c = (F(1), F(1, 2)), (F(0), F(1, 2)), (F(1), F(1, 2))
    assert naive(naive(a, b), c) == (F(5, 8), F(7, 8))
    assert naive(a, naive(b, c)) == (F(3, 4), F(7, 8))


def test_unary_and_plus() -> None:
    p = (F(1, 4), F(1, 8), F(0), F(1, 2))
    assert darken(p, F(1, 2)) == (F(1, 8), F(1, 16), 0, F(1, 2))
    assert dissolve(p, F(1, 2)) == (F(1, 8), F(1, 16), 0, F(1, 4))
    assert opaque(p, F(1, 2)) == (F(1, 4), F(1, 8), F(0), F(1, 4))
    assert plus(p, p) == (F(1, 2), F(1, 4), 0, 1)
    assert unpremultiply(p) == ((F(1, 2), F(1, 4), F(0)), F(1, 2))
    assert unpremultiply((F(0),) * 4) == ((0, 0, 0), 0)
