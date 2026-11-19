# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rhie-chow-interpolation/. The authors are listed in prov/SYEY5V.jsonl.

import math
from fractions import Fraction

from rhie_chow_interpolation import (avg, cell_gradient, face_difference, linear_continuity_operator, momentum_residual,
                                     rhie_chow_continuity_operator, simple)


def _rank(rows):
    rows = [list(r) for r in rows]
    rank, col, m = 0, 0, len(rows[0])
    while rank < len(rows) and col < m:
        piv = next((r for r in range(rank, len(rows)) if rows[r][col] != 0), None)
        if piv is None:
            col += 1
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                f = rows[r][col] / rows[rank][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
        col += 1
    return rank


def _matrix(op, n, h, a):
    cols = [op([Fraction(int(i == k)) for i in range(n)], h, a) for k in range(n)]
    return [[cols[k][i] for k in range(n)] for i in range(n)]


def test_checkerboard_is_invisible_to_linear_interpolation_only():
    n, h, a = 8, Fraction(1, 8), Fraction(3)
    chk = [Fraction((-1) ** i) for i in range(n)]
    assert all(x == 0 for x in cell_gradient(chk, h))
    assert all(x == 0 for x in linear_continuity_operator(chk, h, a))
    assert rhie_chow_continuity_operator(chk, h, a) == [4 * (-1) ** i / (a * h * h) for i in range(n)]
    # null spaces: constants and the checkerboard for linear interpolation, constants only for Rhie-Chow
    assert _rank(_matrix(linear_continuity_operator, n, h, a)) == n - 2
    assert _rank(_matrix(rhie_chow_continuity_operator, n, h, a)) == n - 1


def test_the_added_term_is_minus_h2_over_4_times_the_third_derivative():
    errs = []
    for n in (32, 64):
        h = 1.0 / n
        x = [(i + 0.5) * h for i in range(n)]
        p = [math.sin(2 * math.pi * t) for t in x]
        diff = [a - b for a, b in zip(face_difference(p, h), avg(cell_gradient(p, h)))]
        third = [-(2 * math.pi) ** 3 * math.cos(2 * math.pi * (t + h / 2)) for t in x]
        # dp/h - avg(G p) = -(h^2 / 4) p''' at the face + O(h^4)
        assert max(abs(d + h * h / 4 * q) for d, q in zip(diff, third)) < h**4 * (2 * math.pi) ** 5 / 4
        errs.append(max(map(abs, diff)))
    assert 3.9 < errs[0] / errs[1] < 4.1


def _source(n):
    return [1 + math.sin(2 * math.pi * (i + 0.5) / n) + 0.5 * math.sin(6 * math.pi * (i + 0.5) / n) for i in range(n)]


def test_simple_fixed_point_solves_the_discrete_equations():
    s = _source(16)
    u, uf, p, _ = simple(s, 1.0, 0.01, alpha=0.7, alpha_p=0.3)
    assert max(uf) - min(uf) < 1e-12  # continuity
    assert momentum_residual(u, p, s, 1.0, 0.01) < 1e-9
    assert abs(uf[0] - 1) < 1e-9  # the mean of s divided by c


def test_converged_pressure_depends_on_relaxation_unless_majumdar():
    s = _source(16)
    _, _, p1, _ = simple(s, 1.0, 0.01, alpha=1.0, alpha_p=1.0)
    for alpha, lo in ((0.7, 2.0e-3), (0.3, 5.1e-3)):  # measured 2.046e-3 and 5.197e-3
        _, _, pa, _ = simple(s, 1.0, 0.01, alpha=alpha, alpha_p=0.3)
        _, _, pm, _ = simple(s, 1.0, 0.01, alpha=alpha, alpha_p=0.3, majumdar=True)
        assert max(abs(a - b) for a, b in zip(pa, p1)) > lo
        assert max(abs(a - b) for a, b in zip(pm, p1)) < 1e-12
