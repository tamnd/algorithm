# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucas-kanade-method/. The authors are listed in prov/VEDYF0.jsonl.

import math
import random
from fractions import Fraction as F

from lucas_kanade_method import (
    lucas_kanade,
    lucas_kanade_step,
    min_eigenvalue,
    normal_equations,
    sample,
    solve_2x2,
    window,
)

N = 24


def blob(x, y):
    return 100 * math.exp(-((x - 11.5) ** 2 + (y - 11.5) ** 2) / 18)


def shifted_frames(dx, dy):
    """Frame 2 is frame 1 moved by the integer shift (dx, dy): E2(x + dx, y + dy) = E1(x, y)."""
    e1 = [[blob(x, y) for x in range(N)] for y in range(N)]
    e2 = [[blob(x - dx, y - dy) for x in range(N)] for y in range(N)]
    return e1, e2


def eliminate(rows, rhs):
    """Least squares by Gaussian elimination on the normal equations, built from the raw rows."""
    m = [[sum(r[i] * r[j] for r in rows) for j in range(2)] + [sum(r[i] * t for r, t in zip(rows, rhs))] for i in range(2)]
    if m[0][0] == 0:
        m[0], m[1] = m[1], m[0]
    k = m[1][0] / m[0][0]
    m[1] = [x - k * y for x, y in zip(m[1], m[0])]
    v = m[1][2] / m[1][1]
    u = (m[0][2] - m[0][1] * v) / m[0][0]
    return u, v


def test_closed_form_matches_direct_least_squares() -> None:
    rng = random.Random(8)
    for _ in range(200):
        n = rng.randrange(2, 30)
        ix = [F(rng.randrange(-50, 51), rng.randrange(1, 9)) for _ in range(n)]
        iy = [F(rng.randrange(-50, 51), rng.randrange(1, 9)) for _ in range(n)]
        it = [F(rng.randrange(-50, 51), rng.randrange(1, 9)) for _ in range(n)]
        a, b, c, p, q = normal_equations(ix, iy, it)
        d = solve_2x2(a, b, c, p, q)
        if a * c - b * b == 0:
            assert d is None
            continue
        assert d == eliminate(list(zip(ix, iy)), [-t for t in it])
        # the residual is orthogonal to both columns, so d is the least-squares minimum
        res = [x * d[0] + y * d[1] + t for x, y, t in zip(ix, iy, it)]
        assert sum(r * x for r, x in zip(res, ix)) == 0 and sum(r * y for r, y in zip(res, iy)) == 0


def test_example_numbers() -> None:
    a, b, c, p, q = normal_equations([1, 0, 1], [0, 1, 1], [-2, 1, -1])
    assert (a, b, c, p, q) == (2, 1, 2, 3, 0)
    assert solve_2x2(F(a), F(b), F(c), F(p), F(q)) == (F(2), F(-1))


def test_straight_edge_is_singular() -> None:
    e1 = [[3 * x + 5 * y for x in range(8)] for y in range(8)]
    e2 = [[3 * (x - 1) + 5 * y for x in range(8)] for y in range(8)]
    assert lucas_kanade_step(e1, e2, window(4, 4, 2)) is None


def test_bilinear_sample_is_exact_at_integers() -> None:
    img = [[F(x * x + 3 * y) for x in range(5)] for y in range(4)]
    assert sample(img, 2, 3) == 13
    assert sample(img, F(5, 2), 1) == (img[1][2] + img[1][3]) / 2


def test_iteration_recovers_an_integer_translation() -> None:
    e1, e2 = shifted_frames(2, -1)
    (u, v), steps = lucas_kanade(e1, e2, window(11, 11, 6), 50, 1e-12)
    assert abs(u - 2) < 1e-12 and abs(v + 1) < 1e-12
    assert steps <= 8
    first = lucas_kanade_step(e1, e2, window(11, 11, 6))
    assert abs(first[0] - 1.8826) < 1e-4 and abs(first[1] + 0.9148) < 1e-4


def test_true_shift_is_a_fixed_point() -> None:
    e1, e2 = shifted_frames(2, -1)
    step = lucas_kanade_step(e1, e2, window(11, 11, 6), (2, -1))
    assert math.hypot(*step) < 1e-12


def test_texture_measure() -> None:
    assert min_eigenvalue(2, 1, 2) == 1
    assert min_eigenvalue(9, 0, 0) == 0
