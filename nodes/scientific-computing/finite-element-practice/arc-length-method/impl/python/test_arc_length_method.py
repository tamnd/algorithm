# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-length-method/. The authors are listed in prov/J4J4WD.jsonl.

import math

import scimat
from arc_length_method import (
    arc_length,
    load_control,
    truss_with_spring,
    von_mises_limit_point,
    von_mises_truss,
)


def residual(fint, P, u, lam):
    return scimat.norm2(scimat.sub(fint(u), scimat.scale(lam, P)))


def increments(path):
    return [(scimat.sub(b[0], a[0]), b[1] - a[1]) for a, b in zip(path, path[1:])]


def test_linear_problem_is_a_straight_line():
    K = [[4.0, -1.0], [-1.0, 3.0]]
    P = [1.0, 2.0]
    path = arc_length(lambda u: scimat.matvec(K, u), lambda u: K, P, [0.0, 0.0], 0.5, 6, psi=0.5)
    x = scimat.solve(K, P)
    for u, lam, it in path:
        assert it == 0
        assert all(abs(ui - lam * xi) < 1e-12 for ui, xi in zip(u, x))
    for du, dlam in increments(path):
        assert abs(scimat.dot(du, du) + 0.25 * dlam * dlam * scimat.dot(P, P) - 0.25) < 1e-12


def test_truss_path_through_the_limit_points():
    fint, tangent = von_mises_truss()
    path = arc_length(fint, tangent, [1.0], [0.0], 0.02, 70)
    ws = [p[0][0] for p in path]
    lams = [p[1] for p in path]
    for u, lam, _ in path:
        assert residual(fint, [1.0], u, lam) < 1e-9
    # the apex moves down all the time, past the flat position w = H and the inverted one w = 2H
    assert all(b > a for a, b in zip(ws, ws[1:]))
    assert ws[-1] > 1.0
    # the load rises, falls through zero and below, and rises again
    i_max = max(range(len(lams)), key=lambda i: lams[i] if ws[i] < 0.5 else -1)
    i_min = min(range(len(lams)), key=lambda i: lams[i])
    assert 0 < i_max < i_min < len(lams) - 1
    assert lams[i_min] < -0.03
    assert lams[-1] > 0


def test_arc_length_constraint_holds_for_each_step():
    fint, tangent = von_mises_truss()
    for psi in (1.0, 0.0):
        path = arc_length(fint, tangent, [1.0], [0.0], 0.03, 30, psi=psi)
        for du, dlam in increments(path):
            assert abs(scimat.dot(du, du) + psi * psi * dlam * dlam - 0.03 ** 2) < 1e-12


def test_limit_load_against_closed_form():
    fint, tangent = von_mises_truss()
    w_lim, p_lim = von_mises_limit_point()
    # the closed form is a stationary point of fint
    h = 1e-6
    assert abs(fint([w_lim + h])[0] - fint([w_lim - h])[0]) < 1e-12
    errs = []
    for dl in (0.04, 0.02, 0.01):
        path = arc_length(fint, tangent, [1.0], [0.0], dl, int(0.6 / dl))
        best = max(p[1] for p in path if p[0][0] < 0.5)
        assert best <= p_lim + 1e-12
        errs.append(p_lim - best)
    # the largest sampled load misses the peak by O(dl^2)
    assert errs[-1] < 1e-5
    assert all(q > 1.5 for q in scimat.observed_order(errs))


def test_load_control_cannot_pass_the_limit_point():
    fint, tangent = von_mises_truss()
    w_lim, p_lim = von_mises_limit_point()
    below = load_control(fint, tangent, [1.0], [0.0], [p_lim * s for s in (0.25, 0.5, 0.75, 0.95)])
    assert below[-1][0][0] < w_lim
    # just above the limit load there is no equilibrium near the start branch:
    # Newton either fails or jumps through to the far branch beyond w = 2H.
    try:
        out = load_control(fint, tangent, [1.0], below[-1][0], [1.05 * p_lim])
    except RuntimeError:
        return
    assert out[-1][0][0] > 1.0


def test_snap_back_with_a_soft_spring():
    # Load on the free end of a spring of stiffness 0.1 on top of the apex.
    # The truss softens faster than the spring is stiff, so the loaded point moves back.
    k = 0.1
    fint, tangent = truss_with_spring(k)
    P = [0.0, 1.0]
    path = arc_length(fint, tangent, P, [0.0, 0.0], 0.05, 80)
    zs = [p[0][1] for p in path]
    for u, lam, _ in path:
        assert residual(fint, P, u, lam) < 1e-9
        assert abs(k * (u[1] - u[0]) - lam) < 1e-9
    backs = sum(1 for a, b in zip(zs, zs[1:]) if b < a)
    assert backs >= 3
    assert path[-1][0][0] > 1.0
    # successive increments never point backwards along the path
    inc = increments(path)
    for (a, la), (b, lb) in zip(inc, inc[1:]):
        assert scimat.dot(a, b) + la * lb > 0


def test_iterations_are_few():
    fint, tangent = truss_with_spring(0.1)
    path = arc_length(fint, tangent, [0.0, 1.0], [0.0, 0.0], 0.05, 80)
    assert max(p[2] for p in path) <= 6
