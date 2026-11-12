# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radiosity/. The authors are listed in prov/E000CC.jsonl.

import math
from fractions import Fraction as Fr

import pytest

from radiosity import (
    cube_room,
    exact_solve,
    form_factor,
    form_factor_matrix,
    gauss_seidel,
    jacobi,
    point_to_polygon,
    progressive_refinement,
    radiosity,
    sphere_zone_form_factors,
)

CUTS = [Fr(-1), Fr(0), Fr(1, 2), Fr(1)]
E_SPH = [Fr(1), Fr(0), Fr(0)]
RHO_SPH = [Fr(1, 2), Fr(1, 2), Fr(1, 4)]


def test_sphere_zones_reciprocity_and_row_sums_are_exact():
    areas, F = sphere_zone_form_factors(CUTS)
    for i in range(3):
        assert sum(F[i]) == 1
        for j in range(3):
            assert areas[i] * F[i][j] == areas[j] * F[j][i]


def test_sphere_zones_exact_solution():
    areas, F = sphere_zone_form_factors(CUTS)
    B = exact_solve(E_SPH, RHO_SPH, F)
    assert B == [Fr(13, 9), Fr(4, 9), Fr(2, 9)]
    for i in range(3):
        assert B[i] == E_SPH[i] + RHO_SPH[i] * sum(F[i][j] * B[j] for j in range(3))


@pytest.mark.parametrize("method", ["jacobi", "gauss_seidel", "progressive"])
def test_iterations_match_the_exact_solve(method):
    areas, F = sphere_zone_form_factors(CUTS)
    exact = [float(b) for b in exact_solve(E_SPH, RHO_SPH, F)]
    e = [float(x) for x in E_SPH]
    r = [float(x) for x in RHO_SPH]
    f = [[float(x) for x in row] for row in F]
    if method == "jacobi":
        B, _ = jacobi(e, r, f)
    elif method == "gauss_seidel":
        B, _ = gauss_seidel(e, r, f)
    else:
        B, _ = progressive_refinement(e, r, f, [float(a) for a in areas])
    assert max(abs(B[i] - exact[i]) for i in range(3)) < 1e-11


def test_jacobi_contracts_by_the_largest_reflectance():
    areas, F = sphere_zone_form_factors(CUTS)
    exact = exact_solve(E_SPH, RHO_SPH, F)
    B = list(E_SPH)
    e0 = max(abs(B[i] - exact[i]) for i in range(3))
    for k in range(1, 12):
        B = [E_SPH[i] + RHO_SPH[i] * sum(F[i][j] * B[j] for j in range(3)) for i in range(3)]
        assert max(abs(B[i] - exact[i]) for i in range(3)) <= Fr(1, 2) ** k * e0


def test_exact_solve_with_fractions_on_jacobi_values():
    # Gauss-Seidel in exact arithmetic gets closer than Jacobi after the same number of sweeps here.
    areas, F = sphere_zone_form_factors(CUTS)
    exact = exact_solve(E_SPH, RHO_SPH, F)
    bj = list(E_SPH)
    bg = list(E_SPH)
    for _ in range(3):
        bj = [E_SPH[i] + RHO_SPH[i] * sum(F[i][j] * bj[j] for j in range(3)) for i in range(3)]
        for i in range(3):
            bg[i] = E_SPH[i] + RHO_SPH[i] * sum(F[i][j] * bg[j] for j in range(3))
    assert max(abs(bg[i] - exact[i]) for i in range(3)) < max(abs(bj[i] - exact[i]) for i in range(3))


def test_unit_square_form_factors_match_the_closed_forms():
    # Two parallel unit squares at distance 1, and two unit squares that share an edge at 90 degrees.
    P = cube_room(1)
    F = form_factor_matrix(P, 16)
    x = math.sqrt(2.0)
    parallel = (2 / math.pi) * (math.log(math.sqrt(4 / 3)) + x * math.atan(1 / x) * 2 - 2 * math.atan(1.0))
    perpendicular = (1 / math.pi) * (2 * math.atan(1.0) - x * math.atan(1 / x) + 0.25 * math.log(3 / 4))
    assert math.isclose(F[0][1], parallel, rel_tol=1e-9)
    assert math.isclose(F[0][2], perpendicular, rel_tol=1e-9)
    assert F[0][0] == 0.0


def test_point_to_polygon_of_a_whole_face_and_of_a_hemisphere():
    # From the center of the floor of the unit cube, the four walls and the ceiling cover the hemisphere.
    p, n = (0.5, 0.5, 0.0), (0.0, 0.0, 1.0)
    room = cube_room(1)
    total = sum(point_to_polygon(p, n, q.vertices) for q in room if q.normal != n)
    assert math.isclose(total, 1.0, rel_tol=1e-14)


@pytest.fixture(scope="module")
def room():
    P = cube_room(2)
    return P, form_factor_matrix(P, 8)


def test_cube_room_row_sums_and_reciprocity(room):
    P, F = room
    for i in range(len(P)):
        assert abs(sum(F[i]) - 1.0) < 1e-12  # the room is closed
        for j in range(len(P)):
            assert abs(P[i].area * F[i][j] - P[j].area * F[j][i]) < 1e-9 * P[i].area


def test_cube_room_furnace(room):
    P, F = room
    n = len(P)
    B, _ = gauss_seidel([1.0] * n, [0.6] * n, F)
    for b in B:
        assert math.isclose(b, 1 / (1 - 0.6), rel_tol=1e-10)


def test_cube_room_solvers_agree_with_elimination(room):
    P, F = room
    n = len(P)
    E = [1.0 if p.normal == (0.0, 0.0, -1.0) else 0.0 for p in P]  # the ceiling z = 1 emits
    rho = [0.3 if p.normal[2] != 0.0 else 0.7 for p in P]
    exact = exact_solve(E, rho, F)
    Bj, nj = jacobi(E, rho, F)
    Bg, ng = gauss_seidel(E, rho, F)
    Bp, _ = progressive_refinement(E, rho, F, [p.area for p in P])
    for B in (Bj, Bg, Bp):
        assert max(abs(B[i] - exact[i]) for i in range(n)) < 1e-10
    assert ng < nj
    B, _, _ = radiosity(P, E, rho)
    assert max(abs(B[i] - exact[i]) for i in range(n)) < 1e-10


def test_form_factor_is_zero_for_coplanar_patches():
    P = cube_room(2)
    assert form_factor(P[0], P[1]) == 0.0
