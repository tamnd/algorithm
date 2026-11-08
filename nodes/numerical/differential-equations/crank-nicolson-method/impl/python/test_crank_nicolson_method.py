# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crank-nicolson-method/. The authors are listed in prov/NNF3BE.jsonl.

import math
import random

import pytest

from crank_nicolson_method import crank_nicolson, thomas


def l2(u, dx):
    return math.sqrt(dx * sum(v * v for v in u))


def test_thomas_against_dense() -> None:
    a, b, c, d = [0, 1, 2, 1], [4, 5, 6, 4], [1, 2, 1, 0], [1, 2, 3, 4]
    x = thomas(a, b, c, d)
    for i in range(4):
        lhs = b[i] * x[i] + (a[i] * x[i - 1] if i else 0) + (c[i] * x[i + 1] if i < 3 else 0)
        assert abs(lhs - d[i]) < 1e-14


def test_quadratic_solution_is_reproduced() -> None:
    # u = x^2 + 2 kappa t solves u_t = kappa u_xx; the scheme is exact for it.
    k = 0.7
    xs, u, info = crank_nicolson(lambda x: x * x, k, 1.0, 0.5, 8, 0.1, left=lambda t: 2 * k * t,
                                 right=lambda t: 1 + 2 * k * t)
    assert max(abs(u[j] - xs[j] ** 2 - 2 * k * 0.5) for j in range(9)) < 1e-12


@pytest.mark.parametrize("theta", [0.0, 0.5, 1.0])
def test_fourier_mode_amplification(theta) -> None:
    m, kk, r = 16, 3, 0.4
    dx = 1 / m
    dt = r * dx * dx
    s = math.sin(kk * math.pi * dx / 2) ** 2
    g = (1 - 4 * (1 - theta) * r * s) / (1 + 4 * theta * r * s)
    xs, u, _ = crank_nicolson(lambda x: math.sin(kk * math.pi * x), 1.0, 1.0, 5 * dt, m, dt, theta=theta)
    assert max(abs(u[j] - g ** 5 * math.sin(kk * math.pi * xs[j])) for j in range(m + 1)) < 1e-13


def _err(m, theta):
    xs, u, _ = crank_nicolson(lambda x: math.sin(math.pi * x), 1.0, 1.0, 0.1, m, 1.0 / (10 * m), theta=theta)
    return max(abs(u[j] - math.sin(math.pi * xs[j]) * math.exp(-math.pi ** 2 * 0.1)) for j in range(m + 1))


def test_second_order_in_space_and_time() -> None:
    e = [_err(m, 0.5) for m in (20, 40, 80)]  # dt = dx / 10, so r grows like 1/dx
    assert all(abs(math.log2(e[i] / e[i + 1]) - 2) < 0.05 for i in range(2))
    eb = [_err(m, 1.0) for m in (20, 40, 80)]  # backward Euler: first order in dt
    assert all(abs(math.log2(eb[i] / eb[i + 1]) - 1) < 0.1 for i in range(2))


def test_unconditionally_stable_in_l2() -> None:
    rnd = random.Random(1)
    m = 40
    u = [0.0] + [rnd.uniform(-1, 1) for _ in range(m - 1)] + [0.0]
    dt = 100 / m ** 2  # r = 100
    norms = [l2(u, 1 / m)]
    for _ in range(20):
        _, u, info = crank_nicolson(u, 1.0, 1.0, dt, m, dt)
        norms.append(l2(u, 1 / m))
    assert info["r"] == pytest.approx(100)
    assert all(norms[i + 1] <= norms[i] * (1 + 1e-14) for i in range(20))


def test_maximum_principle_and_oscillation() -> None:
    m = 50
    u0 = [0.0] * (m + 1)
    u0[25] = 1.0
    _, u, _ = crank_nicolson(u0, 1.0, 1.0, 0.0004 * 5, m, 0.0004)  # r = 1
    assert min(u) >= 0 and max(u) <= 1
    centre = [crank_nicolson(u0, 1.0, 1.0, n * 0.01, m, 0.01)[1][25] for n in (1, 2, 3, 4)]  # r = 25
    assert centre[0] < -0.7 and centre[1] > 0.7 and centre[2] < -0.5 and centre[3] > 0.5
    _, ub, _ = crank_nicolson(u0, 1.0, 1.0, 0.01, m, 0.01, theta=1.0)  # backward Euler stays positive
    assert min(ub) >= 0


def test_explicit_scheme_fails_beyond_r_half() -> None:
    m = 20
    u0 = [math.sin(math.pi * j / m) + 1e-3 * (-1) ** j for j in range(m + 1)]
    u0[0] = u0[-1] = 0.0
    _, ok, _ = crank_nicolson(u0, 1.0, 1.0, 400 * 0.5 / m ** 2, m, 0.5 / m ** 2, theta=0.0)
    _, bad, _ = crank_nicolson(u0, 1.0, 1.0, 400 * 0.6 / m ** 2, m, 0.6 / m ** 2, theta=0.0)
    assert max(map(abs, ok)) < 1 and max(map(abs, bad)) > 1e6
    _, cn, _ = crank_nicolson(u0, 1.0, 1.0, 400 * 0.6 / m ** 2, m, 0.6 / m ** 2)
    assert max(map(abs, cn)) < 1


def test_neumann_conserves_total_heat() -> None:
    m = 30
    u0 = [1.0 if 10 <= j <= 14 else 0.0 for j in range(m + 1)]
    heat = lambda u: (u[0] / 2 + sum(u[1:-1]) + u[-1] / 2) / m
    _, u, _ = crank_nicolson(u0, 1.0, 1.0, 0.3, m, 0.01, bc="neumann")
    assert abs(heat(u) - heat(u0)) < 1e-14
    assert max(u) - min(u) < 0.05  # the temperature levels out at the mean
    _, c, _ = crank_nicolson([2.0] * (m + 1), 1.0, 1.0, 0.3, m, 0.1, bc="neumann")
    assert max(abs(v - 2) for v in c) < 1e-14


def test_edges() -> None:
    f0 = lambda x: math.sin(math.pi * x)
    xs, u, info = crank_nicolson(f0, 1.0, 1.0, 0.0, 10, 0.1)
    assert info["steps"] == 0 and u[1:-1] == [f0(x) for x in xs[1:-1]] and u[0] == u[-1] == 0.0
    _, _, info = crank_nicolson(f0, 1.0, 1.0, 0.05, 10, 1.0)  # dt larger than the interval
    assert info["steps"] == 1 and info["dt"] == 0.05
    _, _, info = crank_nicolson(f0, 1.0, 1.0, 0.1, 10, 0.03)  # 0.1 is not a multiple of 0.03
    assert info["steps"] == 4 and abs(info["dt"] * 4 - 0.1) < 1e-15
    for bad in (dict(m=1), dict(dt=0.0), dict(bc="periodic")):
        args = dict(m=10, dt=0.1, bc="dirichlet") | bad
        with pytest.raises(ValueError):
            crank_nicolson(f0, 1.0, 1.0, 0.1, args["m"], args["dt"], bc=args["bc"])
