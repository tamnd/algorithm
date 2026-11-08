# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adi-method/. The authors are listed in prov/G6HHDK.jsonl.

import math
import random

import pytest

from adi_method import adi, thomas

mode = lambda k, l: (lambda x, y: math.sin(k * math.pi * x) * math.sin(l * math.pi * y))


def norm(u, dx, dy):
    return math.sqrt(dx * dy * sum(v * v for row in u for v in row))


def test_thomas() -> None:
    x = thomas([0.0, -1.0, -1.0], [2.0, 2.0, 2.0], [-1.0, -1.0, 0.0], [1.0, 0.0, 1.0])
    assert all(abs(v - 1.0) < 1e-15 for v in x)


def test_mode_amplification_exact() -> None:
    mx, my, k, l = 8, 6, 3, 2
    dt = 0.01
    rx, ry = dt * mx ** 2, dt * my ** 2
    sx, sy = math.sin(k * math.pi / (2 * mx)) ** 2, math.sin(l * math.pi / (2 * my)) ** 2
    g = (1 - 2 * rx * sx) * (1 - 2 * ry * sy) / ((1 + 2 * rx * sx) * (1 + 2 * ry * sy))
    u, _ = adi(mode(k, l), 1.0, 1.0, 1.0, 3 * dt, mx, my, dt)
    for i in range(mx + 1):
        for j in range(my + 1):
            assert abs(u[i][j] - g ** 3 * mode(k, l)(i / mx, j / my)) < 1e-13


def test_hand_example() -> None:
    u, info = adi(mode(1, 1), 1.0, 1.0, 1.0, 1 / 16, 4, 4, 1 / 16)
    assert info["rx"] == 1.0
    s = math.sin(math.pi / 8) ** 2
    assert abs(u[2][2] - ((1 - 2 * s) / (1 + 2 * s)) ** 2) < 1e-15
    assert abs(u[2][2] - 0.2991195) < 1e-7


def test_second_order() -> None:
    def err(m):
        u, _ = adi(mode(1, 1), 1.0, 1.0, 1.0, 0.1, m, m, 1.0 / (5 * m))
        ex = math.exp(-2 * math.pi ** 2 * 0.1)
        return max(abs(u[i][j] - ex * mode(1, 1)(i / m, j / m)) for i in range(m + 1) for j in range(m + 1))

    e = [err(m) for m in (8, 16, 32)]
    assert all(abs(math.log2(e[i] / e[i + 1]) - 2) < 0.05 for i in range(2))


def test_unconditional_l2_stability() -> None:
    rnd = random.Random(2)
    m = 12
    u = [[0.0 if i in (0, m) or j in (0, m) else rnd.uniform(-1, 1) for j in range(m + 1)] for i in range(m + 1)]
    dt = 50.0 / m ** 2  # r = 50
    norms = [norm(u, 1 / m, 1 / m)]
    for _ in range(10):
        u, _ = adi(u, 1.0, 1.0, 1.0, dt, m, m, dt)
        norms.append(norm(u, 1 / m, 1 / m))
    assert all(norms[i + 1] <= norms[i] * (1 + 1e-14) for i in range(10))


def test_explicit_scheme_needs_small_steps() -> None:
    # Forward Euler in 2D needs r <= 1/4; ADI is stable at the same step.
    m, r = 10, 0.3
    dt = r / m ** 2
    u = [[mode(1, 1)(i / m, j / m) + (1e-6 * (-1) ** (i + j) if 0 < i < m and 0 < j < m else 0.0)
          for j in range(m + 1)] for i in range(m + 1)]
    v = [row[:] for row in u]
    for _ in range(300):
        v = [[0.0 if i in (0, m) or j in (0, m) else
              v[i][j] + r * (v[i - 1][j] + v[i + 1][j] + v[i][j - 1] + v[i][j + 1] - 4 * v[i][j])
              for j in range(m + 1)] for i in range(m + 1)]
    assert max(abs(x) for row in v for x in row) > 1e3
    w, _ = adi(u, 1.0, 1.0, 1.0, 300 * dt, m, m, dt)
    assert max(abs(x) for row in w for x in row) < 1


def test_neumann_conserves_total_heat() -> None:
    m = 10
    u0 = [[1.0 if 3 <= i <= 5 and 2 <= j <= 4 else 0.0 for j in range(m + 1)] for i in range(m + 1)]
    wt = lambda i: 0.5 if i in (0, m) else 1.0
    heat = lambda u: sum(wt(i) * wt(j) * u[i][j] for i in range(m + 1) for j in range(m + 1))
    spread = []
    for dt in (0.01, 0.05):  # r = 1 and r = 5
        u, _ = adi(u0, 1.0, 1.0, 1.0, 0.5, m, m, dt, bc="neumann")
        assert abs(heat(u) - heat(u0)) < 1e-13
        spread.append(max(map(max, u)) - min(map(min, u)))
    # the temperature levels out; with r = 5 the checkerboard modes are damped only slowly
    assert spread[0] < 0.003 and spread[1] > 0.02


def test_edges() -> None:
    u, info = adi(mode(1, 1), 1.0, 1.0, 1.0, 0.0, 4, 4, 0.1)
    assert info["steps"] == 0 and abs(u[2][2] - 1.0) < 1e-15
    _, info = adi(mode(1, 1), 1.0, 1.0, 1.0, 0.05, 4, 4, 1.0)
    assert info["steps"] == 1 and info["dt"] == 0.05
    _, info = adi(mode(1, 1), 1.0, 1.0, 2.0, 0.1, 4, 8, 0.03)
    assert info["steps"] == 4 and info["rx"] == pytest.approx(0.4) and info["ry"] == pytest.approx(0.4)
    with pytest.raises(ValueError):
        adi(mode(1, 1), 1.0, 1.0, 1.0, 0.1, 1, 4, 0.1)
