# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-element-method/. The authors are listed in prov/03WMHA.jsonl.

import math

import scimat
from boundary_element_method import (
    assemble,
    bem_solve,
    dirichlet,
    interior_value,
    midpoint,
    outward_normal,
    polygon_elements,
    segment_integrals,
)

SQUARE = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]


def u_exp(x, y):
    return math.exp(x) * math.sin(y)


def q_exp(e):
    (x, y), (nx, ny) = midpoint(e), outward_normal(e)
    return math.exp(x) * (math.sin(y) * nx + math.cos(y) * ny)


def brute_force(x, a, b, n=20000):
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    nx, ny = outward_normal((a, b))
    g = h = 0.0
    for k in range(n):
        s = (k + 0.5) / n
        rx, ry = a[0] + s * (b[0] - a[0]) - x[0], a[1] + s * (b[1] - a[1]) - x[1]
        r2 = rx * rx + ry * ry
        g += -math.log(r2) / (4 * math.pi) * length / n
        h += -(rx * nx + ry * ny) / r2 / (2 * math.pi) * length / n
    return g, h


def test_segment_integrals_against_quadrature():
    a, b = (0.2, 0.1), (0.9, 0.5)
    for x in [(0.4, 0.6), (0.6, 0.2), (-1.0, 3.0), (2.0, 0.0)]:
        g, h = segment_integrals(x, a, b)
        g2, h2 = brute_force(x, a, b)
        assert abs(g - g2) < 1e-8 and abs(h - h2) < 1e-8


def test_self_integral_closed_form():
    # x at the midpoint of its own element: int ln r ds = L ln(L / 2) - L, and the double layer is 0
    a, b = (0.0, 0.0), (0.3, 0.4)
    g, h = segment_integrals(midpoint((a, b)), a, b)
    assert abs(g + (0.5 * math.log(0.25) - 0.5) / (2 * math.pi)) < 1e-15
    assert h == 0.0


def test_gauss_law_for_the_double_layer():
    elems = polygon_elements(SQUARE, 5)
    _, h = assemble(elems)
    # with the 1/2 on the diagonal, every row of H sums to zero: constants are in its kernel
    assert max(abs(sum(row)) for row in h) < 1e-14
    # at an interior point the double layer of the constant 1 is -1
    total = sum(segment_integrals((0.3, 0.6), e[0], e[1])[1] for e in elems)
    assert abs(total + 1) < 1e-14


def test_constant_solution_has_zero_flux():
    elems = polygon_elements(SQUARE, 8)
    u, q, _ = bem_solve(elems, ["u"] * len(elems), [1.0] * len(elems))
    assert max(abs(v) for v in q) < 1e-12
    assert abs(interior_value((0.4, 0.7), elems, u, q) - 1) < 1e-13


def test_dirichlet_interior_values_converge_at_second_order():
    errs = []
    for per_side in (4, 8, 16, 32):
        _, vals = dirichlet(SQUARE, per_side, u_exp, [(0.5, 0.5)])
        errs.append(abs(vals[0] - u_exp(0.5, 0.5)))
    assert errs[-1] < 2e-6
    assert all(r > 1.9 for r in scimat.observed_order(errs))


def test_flux_away_from_corners_and_at_corners():
    per_side = 32
    elems = polygon_elements(SQUARE, per_side)
    u, q, _ = bem_solve(elems, ["u"] * len(elems), [u_exp(*midpoint(e)) for e in elems])
    err = [abs(qq - q_exp(e)) for e, qq in zip(elems, q)]
    # elements in the middle third of each side
    middle = [err[k * per_side + j] for k in range(4) for j in range(per_side // 3, 2 * per_side // 3)]
    assert max(middle) < 2e-3
    # the element next to the corner (1, 0) keeps an error of order one with constant elements
    assert err[per_side - 1] > 0.1


def test_mixed_problem():
    errs = []
    for per_side in (4, 8, 16):
        elems = polygon_elements(SQUARE, per_side)
        kinds, values = [], []
        for e in elems:
            (x, y), (nx, ny) = midpoint(e), outward_normal(e)
            if abs(ny) > 0.5:  # bottom and top: u given
                kinds.append("u")
                values.append(u_exp(x, y))
            else:  # left and right: q given
                kinds.append("q")
                values.append(q_exp(e))
        u, q, _ = bem_solve(elems, kinds, values)
        errs.append(abs(interior_value((0.5, 0.5), elems, u, q) - u_exp(0.5, 0.5)))
    assert errs[-1] < 2e-4
    assert all(r > 1.5 for r in scimat.observed_order(errs))


def test_unit_circle_makes_the_single_layer_nearly_singular():
    # On a circle of radius R, int ln |x - y| ds_y = 2 pi R ln R for x on the circle,
    # so for R = 1 the constant density is (almost) in the kernel of G.
    results = {}
    for radius in (1.0, 0.5):
        n = 64
        verts = [(radius * math.cos(2 * math.pi * k / n), radius * math.sin(2 * math.pi * k / n)) for k in range(n)]
        g, _ = assemble(polygon_elements(verts, 1))
        results[radius] = max(abs(sum(row)) for row in g)
    assert results[1.0] < 2e-3
    assert abs(results[0.5] - (-0.5 * math.log(0.5))) < 1e-3
