# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-phase-unwrapping/. The authors are listed in prov/FX5THR.jsonl.

import math
import random

from imgla import solve
from least_squares_phase_unwrapping import (dct2, divergence, idct2, least_squares_cost, neumann_laplacian, residues,
                                            unwrap_least_squares, wrap, wrapped_gradients)

TWO_PI = 2.0 * math.pi


def _wrap_image(phi):
    return [[wrap(v) for v in row] for row in phi]


def _minus_first(phi):
    c = phi[0][0]
    return [[v - c for v in row] for row in phi]


def test_wrap() -> None:
    assert abs(wrap(3 * math.pi / 2) + math.pi / 2) < 1e-15
    assert abs(wrap(math.pi) - math.pi) < 1e-15
    assert abs(wrap(-math.pi) - math.pi) < 1e-15
    assert abs(wrap(7.0) - (7.0 - TWO_PI)) < 1e-15


def test_dct_round_trip() -> None:
    rng = random.Random(7301)
    x = [[rng.uniform(-1, 1) for _ in range(5)] for _ in range(4)]
    y = idct2(dct2(x))
    assert max(abs(a - b) for ra, rb in zip(x, y) for a, b in zip(ra, rb)) < 1e-12


def test_matches_the_normal_equations_solved_directly() -> None:
    # Reference: build D^T D phi = D^T g with one pinned pixel and solve it by
    # Gaussian elimination (imgla.solve); compare up to the additive constant.
    rng = random.Random(7302)
    m, n = 5, 6
    psi = [[rng.uniform(-math.pi, math.pi) for _ in range(n)] for _ in range(m)]
    assert any(r != 0 for row in residues(psi) for r in row)
    dx, dy = wrapped_gradients(psi)
    size = m * n
    a = [[0.0] * size for _ in range(size)]
    b = [0.0] * size
    edges = [(i * n + j, i * n + j + 1, dx[i][j]) for i in range(m) for j in range(n - 1)]
    edges += [(i * n + j, (i + 1) * n + j, dy[i][j]) for i in range(m - 1) for j in range(n)]
    for p, q, g in edges:
        a[p][p] += 1.0
        a[q][q] += 1.0
        a[p][q] -= 1.0
        a[q][p] -= 1.0
        b[p] -= g
        b[q] += g
    a[0] = [1.0] + [0.0] * (size - 1)
    b[0] = 0.0
    ref = solve(a, b)
    got = _minus_first(unwrap_least_squares(psi))
    for i in range(m):
        for j in range(n):
            assert abs(got[i][j] - ref[i * n + j]) < 1e-9
    assert abs(least_squares_cost(got, psi) - least_squares_cost([ref[i * n:(i + 1) * n] for i in range(m)], psi)) < 1e-9


def test_solves_the_neumann_poisson_equation() -> None:
    rng = random.Random(7303)
    psi = [[rng.uniform(-math.pi, math.pi) for _ in range(7)] for _ in range(6)]
    dx, dy = wrapped_gradients(psi)
    rho = divergence(dx, dy, 6, 7)
    assert abs(sum(sum(row) for row in rho)) < 1e-12
    phi = unwrap_least_squares(psi)
    lap = neumann_laplacian(phi)
    assert max(abs(a - b) for ra, rb in zip(lap, rho) for a, b in zip(ra, rb)) < 1e-10
    assert abs(sum(sum(row) for row in phi)) < 1e-10


def test_exact_recovery_without_residues() -> None:
    m, n = 8, 9
    true = [[0.9 * j - 0.5 * i + 1.5 * math.sin(0.4 * i * j / 3.0) for j in range(n)] for i in range(m)]
    psi = _wrap_image(true)
    assert all(r == 0 for row in residues(psi) for r in row)
    got = _minus_first(unwrap_least_squares(psi))
    want = _minus_first(true)
    assert max(abs(a - b) for ra, rb in zip(got, want) for a, b in zip(ra, rb)) < 1e-9


def test_integer_wraps_of_the_input_do_not_change_the_output() -> None:
    rng = random.Random(7304)
    psi = [[rng.uniform(-math.pi, math.pi) for _ in range(5)] for _ in range(5)]
    shifted = [[v + TWO_PI * rng.randint(-3, 3) for v in row] for row in psi]
    a, b = unwrap_least_squares(psi), unwrap_least_squares(shifted)
    assert max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb)) < 1e-9


def test_two_by_two_with_one_residue_spreads_the_error() -> None:
    psi = [[0.0, 2.0], [-2.0, 2.5]]
    assert residues(psi) == [[1]]
    got = _minus_first(unwrap_least_squares(psi))
    q = math.pi / 2
    want = [[0.0, 2.0 - q], [-(2.0 - q), 2.0 - q + 0.5 - q]]
    assert max(abs(a - b) for ra, rb in zip(got, want) for a, b in zip(ra, rb)) < 1e-12
    # The result is not congruent to the data: phi - psi is not a multiple of 2 pi.
    assert abs(wrap(got[0][1] - psi[0][1])) > 1.5


def test_residues_bias_the_slope_low() -> None:
    # A steep ramp plus noise: some wrapped differences take the wrong branch,
    # and the least squares solution spreads those errors, so its mean slope is
    # lower than the true slope. Without noise it is exact.
    rng = random.Random(7305)
    m, n, slope = 10, 10, 2.6
    clean = [[slope * j for j in range(n)] for i in range(m)]
    noisy = [[slope * j + rng.gauss(0.0, 0.7) for j in range(n)] for i in range(m)]

    def mean_slope(phi):
        return sum(phi[i][n - 1] - phi[i][0] for i in range(m)) / (m * (n - 1))

    assert abs(mean_slope(unwrap_least_squares(_wrap_image(clean))) - slope) < 1e-9
    psi = _wrap_image(noisy)
    assert sum(abs(r) for row in residues(psi) for r in row) > 10
    assert mean_slope(unwrap_least_squares(psi)) < 0.9 * slope
