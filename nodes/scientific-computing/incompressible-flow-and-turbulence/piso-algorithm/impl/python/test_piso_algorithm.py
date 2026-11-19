# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piso-algorithm/. The authors are listed in prov/8SFP8G.jsonl.

import math
import random

from piso_algorithm import Grid, coupled_step, divergence, momentum_residual, piso_step, taylor_green

NU = 0.1


def _gap(a, b):
    return max(max(abs(a[0][k] - b[0][k]) for k in range(len(a[0]))), max(abs(a[1][k] - b[1][k]) for k in range(len(a[0]))))


def _gap2(a, b):
    return math.sqrt(sum((a[0][k] - b[0][k]) ** 2 + (a[1][k] - b[1][k]) ** 2 for k in range(len(a[0]))))


def _start(n):
    g = Grid(n, n)
    return g, [0.0] * g.n, taylor_green(g, NU, 0.0)


def test_every_corrector_ends_divergence_free():
    g, z, (u, v, p) = _start(8)
    rng = random.Random(4)
    u = [x + 0.05 * rng.uniform(-1, 1) for x in u]  # not divergence free at the start
    seen = []

    def check(m, us, vs):
        seen.append((m, max(abs(x) for x in divergence(g, us, vs))))

    piso_step(g, u, v, p, NU, 0.1, z, z, correctors=3, check=check)
    assert [m for m, _ in seen] == [1, 2, 3]
    assert all(d < 1e-10 for _, d in seen)


def test_many_correctors_solve_the_coupled_implicit_step():
    g, z, (u, v, p) = _start(8)
    dt = 0.1
    un, vn, pn = coupled_step(g, u, v, p, NU, dt, z, z)
    ru, rv = momentum_residual(g, u, v, un, vn, pn, NU, dt, z, z)
    assert max(max(map(abs, ru)), max(map(abs, rv))) < 1e-11
    assert max(abs(x) for x in divergence(g, un, vn)) < 1e-11


def test_corrector_error_contracts_by_the_proved_factor():
    # ||u^(m+1) - u|| <= q ||u^(m) - u|| with q = S / a_P, S = 2 nu/dx^2 + 2 nu/dy^2 + U/dx + V/dy.
    g, z, (u, v, p) = _start(8)
    dt = 0.2
    U, V = max(map(abs, u)), max(map(abs, v))
    ap = 1 / dt + 2 * NU / g.dx**2 + 2 * NU / g.dy**2
    q = (2 * NU / g.dx**2 + 2 * NU / g.dy**2 + U / g.dx + V / g.dy) / ap
    assert q < 1
    ref = coupled_step(g, u, v, p, NU, dt, z, z)
    errs = [_gap2(piso_step(g, u, v, p, NU, dt, z, z, correctors=m), ref) for m in (1, 2, 3, 4)]
    for a, b in zip(errs, errs[1:]):
        assert b <= q * a


def test_splitting_error_of_one_step_is_order_m_plus_2():
    # Start from a pressure consistent with the scheme (one coupled step first). Measured
    # orders on 8 x 8: about 3 for one corrector and 4 for two.
    g, z, (u, v, p) = _start(8)
    errs = {1: [], 2: []}
    for dt in (0.1, 0.05, 0.025):
        s1 = coupled_step(g, u, v, p, NU, dt, z, z)
        ref = coupled_step(g, *s1, NU, dt, z, z)
        for m in (1, 2):
            errs[m].append(_gap(piso_step(g, *s1, NU, dt, z, z, correctors=m), ref))
    for m, lo in ((1, 2.6), (2, 3.5)):
        e = errs[m]
        orders = [math.log2(e[i] / e[i + 1]) for i in range(2)]
        assert all(o > lo for o in orders), (m, orders)


def test_two_correctors_are_first_order_in_time_like_backward_euler():
    g, z, (u, v, p) = _start(8)
    T = 0.4
    sols = []
    for dt in (0.1, 0.05, 0.025, 0.0125):
        s = (u, v, p)
        for _ in range(round(T / dt)):
            s = piso_step(g, *s, NU, dt, z, z, correctors=2)
        sols.append(s)
    d = [_gap(sols[i], sols[i + 1]) for i in range(3)]
    orders = [math.log2(d[i] / d[i + 1]) for i in range(2)]
    assert all(0.9 < o < 1.15 for o in orders), orders
    eu, ev, _ = taylor_green(g, NU, T)
    assert _gap(sols[-1], (eu, ev)) < 0.05  # the 8 x 8 grid error dominates
