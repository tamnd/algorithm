# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/artificial-compressibility-method/. The authors are listed in prov/FZZC89.jsonl.

import math
from fractions import Fraction as Fr

from artificial_compressibility_method import (
    Grid,
    artificial_compressibility,
    divergence,
    residual,
    stable_step,
    taylor_green_steady,
)

NU = 0.5  # viscosity of the forced steady Taylor-Green tests


def _solve(n, c, tol=1e-11):
    g = Grid(n, n)
    u, v, p, fu, fv = taylor_green_steady(g, NU)
    zero = [0.0] * (n * n)
    uu, vv, pp, it = artificial_compressibility(g, zero, zero, zero, stable_step(g, NU, c, 1.0), c, NU, fu, fv, tol)
    return g, (u, v, p, fu, fv), (uu, vv, pp), it


def test_one_step_by_hand():
    # 4 by 1 periodic cells, dx = dy = 1, nu = 0, force (1, 0, 0, 0) on the u faces, dtau = 1/2, c = 1
    g = Grid(4, 1, Fr(4), Fr(1))
    z = [Fr(0)] * 4
    u, v, p, it = artificial_compressibility(g, z, z, z, Fr(1, 2), 1, 0, [Fr(1), 0, 0, 0], z, 0, maxit=1)
    assert it == 1
    assert u == [Fr(1, 2), 0, 0, 0] and v == z
    assert divergence(g, u, v) == [Fr(-1, 2), 0, 0, Fr(1, 2)]
    assert p == [Fr(1, 4), 0, 0, Fr(-1, 4)]


def test_converged_state_is_divergence_free_and_steady():
    g, (u, v, p, fu, fv), (uu, vv, pp), it = _solve(8, 1.0)
    assert it < 1000  # measured: 151 iterations
    assert max(abs(x) for x in divergence(g, uu, vv)) < 1e-10
    ru, rv = residual(g, uu, vv, pp, NU, fu, fv)
    assert max(abs(x) for x in ru + rv) < 1e-10


def test_steady_state_does_not_depend_on_the_sound_speed():
    _, _, (u1, v1, p1), it1 = _solve(8, 1.0)
    _, _, (u2, v2, p2), it2 = _solve(8, 0.5)
    assert it2 > it1  # measured: 313 against 151 iterations
    m1, m2 = sum(p1) / 64, sum(p2) / 64
    assert max(abs(u1[k] - u2[k]) + abs(v1[k] - v2[k]) + abs(p1[k] - m1 - p2[k] + m2) for k in range(64)) < 1e-9


def test_stability_limit_on_the_checkerboard_mode():
    # the checkerboard pressure is the eigenvector of -D G with the largest eigenvalue;
    # with a tiny amplitude the advection term is negligible and the Stokes analysis applies
    g = Grid(8, 8)
    lim = stable_step(g, NU, 1.0, 0, safety=1.0)
    z = [0.0] * 64
    out = []
    for f in (0.98, 1.02):
        p = [1e-6 * (-1) ** (k % 8 + k // 8) for k in range(64)]
        _, _, pp, _ = artificial_compressibility(g, z, z, p, f * lim, 1.0, NU, z, z, -1, maxit=300)
        out.append(max(abs(x) for x in pp))
    assert out[0] < 1e-12 and out[1] > 1e-3


def test_space_order_on_the_forced_taylor_green_vortex():
    errs, hs = [], []
    for n in (8, 12, 16):
        g, (u, v, p, _, _), (uu, vv, pp), _ = _solve(n, 1.0, tol=1e-10)
        errs.append(max(max(abs(uu[k] - u[k]) for k in range(n * n)), max(abs(vv[k] - v[k]) for k in range(n * n))))
        hs.append(g.dx)
    orders = [math.log(errs[i] / errs[i + 1]) / math.log(hs[i] / hs[i + 1]) for i in range(2)]
    assert all(abs(q - 2) < 0.2 for q in orders), orders
    assert abs(errs[0] - 0.048993) < 1e-5
