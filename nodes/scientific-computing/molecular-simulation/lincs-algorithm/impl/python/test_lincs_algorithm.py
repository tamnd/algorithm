# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lincs-algorithm/. The authors are listed in prov/F7HF6T.jsonl.

import math
import random

from lincs_algorithm import coupling, lincs, series_solve, spectral_radius


def bond_error(x, bonds):
    return max(abs(math.dist(x[i], x[j]) - d) / d for i, j, d in bonds)


def shake_reference(x_old, x_unc, w, bonds):
    """SHAKE iterated to rounding: the exact solution with corrections along the old bonds."""
    x = [list(p) for p in x_unc]
    for _ in range(2000):
        for i, j, d in bonds:
            s = [x[i][a] - x[j][a] for a in range(3)]
            r = [x_old[i][a] - x_old[j][a] for a in range(3)]
            g = (d * d - sum(c * c for c in s)) / (2 * (w[i] + w[j]) * sum(p * q for p, q in zip(s, r)))
            for a in range(3):
                x[i][a] += w[i] * g * r[a]
                x[j][a] -= w[j] * g * r[a]
    return x


def zigzag_chain(seed):
    rng = random.Random(seed)
    x_old = [[0.8 * k, 0.6 * (k % 2), 0.1 * k] for k in range(6)]
    bonds = [(k, k + 1, math.dist(x_old[k], x_old[k + 1])) for k in range(5)]
    w = [1 / 12, 1 / 14, 1 / 12, 1 / 16, 1 / 12, 1.0]
    x_unc = [[c + rng.uniform(-0.03, 0.03) for c in p] for p in x_old]
    return x_old, x_unc, w, bonds


def triangle(angle_deg, seed):
    t = math.radians(angle_deg)
    x_old = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [math.cos(t), math.sin(t), 0.0]]
    bonds = [(0, 1, 1.0), (0, 2, 1.0), (1, 2, math.dist(x_old[1], x_old[2]))]
    rng = random.Random(seed)
    x_unc = [[c + rng.uniform(-0.01, 0.01) for c in p] for p in x_old]
    return x_old, x_unc, [1.0, 1.0, 1.0], bonds


def test_series_solve_matches_a_direct_inverse() -> None:
    x_old, _, w, bonds = zigzag_chain(1)
    _, _, coup = coupling(x_old, w, bonds)
    rhs = [0.3, -0.1, 0.7, 0.2, -0.4]
    sol = series_solve(coup, rhs, 60)
    back = [s - sum(a * sol[d] for d, a in row) for s, row in zip(sol, coup)]  # (I - A) sol
    assert max(abs(p - q) for p, q in zip(back, rhs)) < 1e-14


def test_high_order_with_corrections_reaches_the_shake_solution() -> None:
    x_old, x_unc, w, bonds = zigzag_chain(2)
    x = lincs(x_old, x_unc, w, bonds, order=16, n_iter=4)
    ref = shake_reference(x_old, x_unc, w, bonds)
    assert bond_error(ref, bonds) < 1e-14
    assert bond_error(x, bonds) < 1e-11
    assert max(math.dist(p, q) for p, q in zip(x, ref)) < 1e-11


def test_error_falls_with_order_and_corrections() -> None:
    x_old, x_unc, w, bonds = zigzag_chain(2)
    by_order = [bond_error(lincs(x_old, x_unc, w, bonds, order, 2), bonds) for order in (0, 1, 2)]
    assert by_order[0] > by_order[1] > by_order[2]
    by_iter = [bond_error(lincs(x_old, x_unc, w, bonds, 4, n), bonds) for n in (0, 1, 2, 4)]
    assert by_iter[0] > by_iter[1] > by_iter[2] > by_iter[3]
    assert by_iter[0] > 1e-4  # without the rotation correction the bonds come out too long


def test_centre_of_mass_does_not_move() -> None:
    x_old, x_unc, w, bonds = zigzag_chain(3)
    x = lincs(x_old, x_unc, w, bonds, 4, 1)
    for a in range(3):
        before = sum(p[a] / wi for p, wi in zip(x_unc, w))
        after = sum(p[a] / wi for p, wi in zip(x, w))
        assert abs(before - after) < 1e-12


def test_flat_triangle_makes_the_series_converge_slowly() -> None:
    radii = []
    errors = []
    for angle in (60, 120, 150, 170):
        x_old, x_unc, w, bonds = triangle(angle, 5)
        radii.append(spectral_radius(coupling(x_old, w, bonds)[2]))
        errors.append(bond_error(lincs(x_old, x_unc, w, bonds, 8, 2), bonds))
    assert abs(radii[0] - 0.5) < 1e-9 and abs(radii[1] - 0.75) < 1e-9
    assert radii[1] < radii[2] < radii[3] < 1.0
    assert errors[0] < 1e-9 < 1e-5 < errors[3]
    # the chain without rings stays well inside the unit disc
    x_old, _, w, bonds = zigzag_chain(1)
    assert spectral_radius(coupling(x_old, w, bonds)[2]) < 0.3
