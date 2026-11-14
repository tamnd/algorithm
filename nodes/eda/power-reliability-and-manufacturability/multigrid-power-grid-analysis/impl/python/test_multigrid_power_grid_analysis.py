# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multigrid-power-grid-analysis/. The authors are listed in prov/C6B46K.jsonl.

import random
from fractions import Fraction

from multigrid_power_grid_analysis import (
    energy_error,
    kept_lines,
    knn_solve,
    knn_solve_with_basis,
    prolongation,
    two_grid_iterate,
)
from pgrid import matmul, matvec, mesh, random_mesh, solve, transpose


def test_kept_lines():
    assert kept_lines(5) == [0, 2, 4]
    assert kept_lines(4) == [0, 2, 3]
    assert kept_lines(1) == [0]


def test_rows_of_p_sum_to_one_and_are_nonnegative():
    rng = random.Random(1)
    for nx, ny in [(5, 5), (4, 6), (7, 3)]:
        g = random_mesh(nx, ny, rng)
        p, cshape = prolongation(g.matrix(), (nx, ny))
        assert len(p[0]) == cshape[0] * cshape[1]
        for row in p:
            assert sum(row) == 1
            assert all(w >= 0 for w in row)


def test_h_node_weights_are_conductance_ratios():
    # 3 by 1 line: node 1 sits between the kept nodes 0 and 2.
    g = mesh(3, 1, lambda r, c: Fraction([2, 6][c]), lambda r, c: Fraction(1), {0: Fraction(5)}, [0, 0, 0])
    p, _ = prolongation(g.matrix(), (3, 1))
    assert p[1] == [Fraction(2, 8), Fraction(6, 8)]


def test_galerkin_orthogonality_exact():
    # P^T A (x - P x_c) = 0 exactly, for one level and for several levels.
    rng = random.Random(2)
    for nx, ny, levels in [(5, 5, 1), (5, 5, 2), (7, 5, 2), (4, 4, 1)]:
        g = random_mesh(nx, ny, rng)
        a, b = g.matrix(), g.cur
        x = solve(a, b)
        y, p = knn_solve_with_basis(a, b, (nx, ny), levels)
        e = [u - v for u, v in zip(x, y)]
        assert matvec(transpose(p), matvec(a, e)) == [0] * len(p[0])


def test_one_pass_is_the_best_coarse_answer_in_energy_norm():
    rng = random.Random(3)
    for _ in range(6):
        g = random_mesh(5, 5, rng)
        a, b = g.matrix(), g.cur
        x = solve(a, b)
        y, p = knn_solve_with_basis(a, b, (5, 5), 1)
        best = energy_error(a, x, y)
        for _ in range(20):
            z = [Fraction(rng.randint(-20, 20), 4) for _ in range(len(p[0]))]
            pz = matvec(p, z)
            assert energy_error(a, x, pz) >= best
        # The coarse nodes are only part of the fine nodes, so the answer is not exact in general.
        assert energy_error(a, x, y) >= 0


def test_exact_when_the_solution_is_in_the_range_of_p():
    # A uniform line with a pad at node 0 and a load only at the far end:
    # the drop is linear in the distance, and linear interpolation is exact.
    n = 9
    cur = [Fraction(0)] * n
    cur[-1] = Fraction(3)
    g = mesh(n, 1, lambda r, c: Fraction(2), lambda r, c: Fraction(1), {0: Fraction(4)}, cur)
    a = g.matrix()
    assert knn_solve(a, cur, (n, 1), 3) == solve(a, cur)


def test_float_mesh_close_to_direct():
    rng = random.Random(4)
    g = random_mesh(9, 9, rng, exact=False, n_pads=4)
    a, b = g.matrix(), g.cur
    x = solve(a, b)
    y = knn_solve(a, b, (9, 9), 2)
    assert max(abs(u - v) for u, v in zip(x, y)) < max(x)


def test_variant_converges_to_the_direct_solution():
    rng = random.Random(5)
    g = random_mesh(9, 9, rng, exact=False, n_pads=3)
    a, b = g.matrix(), g.cur
    x = solve(a, b)
    y, hist = two_grid_iterate(a, b, (9, 9), cycles=20, sweeps=1)
    assert max(abs(u - v) for u, v in zip(x, y)) < 1e-8
    assert all(h2 <= h1 * 1.0000001 for h1, h2 in zip(hist, hist[1:]))


def test_variant_energy_error_never_grows():
    rng = random.Random(6)
    g = random_mesh(7, 7, rng)
    a, b = g.matrix(), g.cur
    x = solve(a, b)
    y = knn_solve(a, b, (7, 7), 1)
    prev = energy_error(a, x, y)
    for _ in range(3):
        y, _ = two_grid_iterate(a, b, (7, 7), cycles=1, sweeps=1, x0=y)
        cur = energy_error(a, x, y)
        assert cur <= prev
        prev = cur
