# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simple-algorithm/. The authors are listed in prov/61PTZG.jsonl.

import math
import random
from fractions import Fraction as Fr

import scisparse as sp
from simple_algorithm import Grid, correction_matrix, divergence, pressure_gradient, simple, steady_residual

NU = 0.5


def _manufactured(nx=8, ny=8, amp=0.5):
    """Channel, periodic in x, no-slip walls at y = 0 and y = 1. The velocity comes from a
    discrete streamfunction at the cell corners, so D u = 0 exactly. The force is chosen so
    that this sampled field and p are an exact solution of the discrete steady equations."""
    g = Grid(nx, ny, 2.0, 1.0, walls=True)
    psi = lambda x, y: amp * math.sin(math.pi * x) * 16 * (y * (1 - y)) ** 2
    u = [(psi(i * g.dx, (j + 1) * g.dy) - psi(i * g.dx, j * g.dy)) / g.dy for j in range(ny) for i in range(nx)]
    v = [0.0 if g.wall_v(k) else -(psi((k % nx + 1) * g.dx, (k // nx) * g.dy) - psi((k % nx) * g.dx, (k // nx) * g.dy)) / g.dx
         for k in range(g.nv)]
    p = g.sample_p(lambda x, y: 0.2 * math.cos(math.pi * x) * (y - 0.5))
    n = nx * ny
    r = steady_residual(g, u, v, p, NU, [0.0] * n, [0.0] * g.nv)
    fu = [-x for x in r[:n]]
    fv, pos = [], n
    for k in range(g.nv):
        if g.wall_v(k):
            fv.append(0.0)
        else:
            fv.append(-r[pos])
            pos += 1
    return g, u, v, p, fu, fv


def _gap(g, u, v, p, ue, ve, pe):
    n = len(u)
    eu = max(max(abs(u[k] - ue[k]) for k in range(n)), max(abs(v[k] - ve[k]) for k in range(g.nv)))
    pm, qm = sum(p) / n, sum(pe) / n
    return eu, max(abs(p[k] - pm - pe[k] + qm) for k in range(n))


def test_correction_matrix_is_minus_div_d_grad_exactly():
    rng = random.Random(3)
    g = Grid(3, 3, Fr(3), Fr(3, 2), walls=True)
    du = [Fr(rng.randint(1, 9), 10) for _ in range(9)]
    dv = [0 if g.wall_v(k) else Fr(rng.randint(1, 9), 10) for k in range(g.nv)]
    B = correction_matrix(g, du, dv)
    for m in range(9):
        e = [Fr(int(k == m)) for k in range(9)]
        gx, gy = pressure_gradient(g, e)
        col = [-x for x in divergence(g, [du[k] * gx[k] for k in range(9)], [dv[k] * gy[k] for k in range(g.nv)])]
        assert col == [B[k].get(m, 0) for k in range(9)]
    assert all(B[k].get(m, 0) == B[m].get(k, 0) for k in range(9) for m in range(9))
    assert all(sum(row.values()) == 0 for row in B)  # constants are in the null space


def test_poiseuille_error_is_exactly_g_dy2_over_8_nu():
    # The discrete solution is the exact parabola plus G dy^2 / (8 nu): second order.
    G = 1.0
    for ny in (4, 8):
        g = Grid(2, ny, 1.0, 1.0, walls=True)
        n = 2 * ny
        u, v, p, it = simple(g, [0.0] * n, [0.0] * g.nv, [0.0] * n, NU, [G] * n, [0.0] * g.nv, tol=1e-11)
        exact, _ = g.sample(lambda x, y: G / (2 * NU) * y * (1 - y), lambda x, y: 0.0)
        shift = G * g.dy**2 / (8 * NU)
        assert it < 20000
        assert max(abs(u[k] - exact[k] - shift) for k in range(n)) < 1e-9
        assert max(abs(x) for x in v) < 1e-12


def test_converges_to_the_discrete_solution_and_conserves_mass_every_iteration():
    g, ue, ve, pe, fu, fv = _manufactured()
    n = len(ue)
    worst = [0.0]

    def check(u, v):
        worst[0] = max(worst[0], max(abs(x) for x in divergence(g, u, v)))

    u, v, p, it = simple(g, [0.0] * n, [0.0] * g.nv, [0.0] * n, NU, fu, fv, tol=1e-10, check=check)
    eu, ep = _gap(g, u, v, p, ue, ve, pe)
    assert it < 400  # measured: 153
    assert eu < 1e-9 and ep < 1e-9
    assert worst[0] < 1e-10  # D u = 0 after every correction, not only at the end


def test_fixed_point_does_not_depend_on_under_relaxation():
    g, ue, ve, pe, fu, fv = _manufactured()
    n = len(ue)
    u, v, p, it = simple(g, [0.0] * n, [0.0] * g.nv, [0.0] * n, NU, fu, fv, alpha_u=0.8, alpha_p=0.2, sweeps=2, tol=1e-10)
    eu, ep = _gap(g, u, v, p, ue, ve, pe)
    assert it < 400
    assert eu < 1e-9 and ep < 1e-9


def test_full_pressure_correction_diverges_here():
    # Measured on this problem: alpha_u = 0.7 with alpha_p = 1 blows up (rule of thumb:
    # alpha_p near 1 - alpha_u), alpha_p = 0.3 converges.
    g, ue, ve, pe, fu, fv = _manufactured()
    n = len(ue)
    for alpha_p, grows in ((1.0, True), (0.3, False)):
        u, v, p, _ = simple(g, [0.0] * n, [0.0] * g.nv, [0.0] * n, NU, fu, fv, alpha_p=alpha_p, maxit=15)
        r = max(abs(x) for x in steady_residual(g, u, v, p, NU, fu, fv))
        assert (r > 10) == grows


def test_periodic_box_leaves_the_mean_velocity_free():
    # Fully periodic: the steady equations do not fix the mean velocity. Two starts give two
    # different converged states, both with a residual below 1e-10.
    n = 8
    L = 2 * math.pi
    g = Grid(n, n, L, L)
    U = lambda x, y: math.sin(x) * math.cos(y)
    V = lambda x, y: -math.cos(x) * math.sin(y)
    fu, fv = g.sample(lambda x, y: 2 * NU * U(x, y), lambda x, y: 2 * NU * V(x, y))
    eu, ev = g.sample(U, V)
    ep = g.sample_p(lambda x, y: 0.25 * (math.cos(2 * x) + math.cos(2 * y)))
    means = []
    for shift in (0.0, 0.1):
        u, v, p, it = simple(g, [x + shift for x in eu], list(ev), list(ep), NU, fu, fv, tol=1e-10, maxit=1000)
        assert it < 1000
        assert max(abs(x) for x in steady_residual(g, u, v, p, NU, fu, fv)) < 1e-10
        means.append(sum(u) / len(u))
    assert abs(means[1] - means[0]) > 0.05
