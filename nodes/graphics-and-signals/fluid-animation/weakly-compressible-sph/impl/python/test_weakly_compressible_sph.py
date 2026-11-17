# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weakly-compressible-sph/. The authors are listed in prov/XB7CYE.jsonl.

import math
import random

import sph
import weakly_compressible_sph as wc

# ---------------------------------------------------------------- the shared helper sph.py


def brute_pairs(pos, radius):
    out = []
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            if (pos[i][0] - pos[j][0]) ** 2 + (pos[i][1] - pos[j][1]) ** 2 < radius * radius:
                out.append((i, j))
    return out


def test_kernel_check_value() -> None:
    assert abs(sph.SIGMA_2D - 0.454728) < 1e-6
    assert abs(sph.w_cubic(0.0, 1.0) - 0.454728) < 1e-6
    assert abs(sph.w_cubic(0.0, 0.5) - 0.454728 / 0.25) < 1e-5
    assert sph.w_cubic(2.0, 1.0) == 0.0
    assert sph.w_cubic(3.0, 1.0) == 0.0


def test_kernel_integrates_to_one() -> None:
    for h in (1.0, 0.05, 0.3):
        # Simpson's rule on [0, h] and [h, 2h] of W(r) 2 pi r dr.
        total = 0.0
        n = 200
        for a in (0.0, h):
            step = h / n
            s = 0.0
            for k in range(n + 1):
                r = a + k * step
                f = sph.w_cubic(r, h) * 2.0 * math.pi * r
                wgt = 1 if k in (0, n) else (4 if k % 2 else 2)
                s += wgt * f
            total += s * step / 3.0
        assert abs(total - 1.0) < 1e-3


def test_kernel_is_continuous_and_derivative_matches() -> None:
    h = 0.7
    for q in (1.0, 2.0):
        r = q * h
        assert abs(sph.w_cubic(r - 1e-9, h) - sph.w_cubic(r + 1e-9, h)) < 1e-7
    for q in (0.1, 0.5, 0.9, 1.1, 1.5, 1.9):
        r = q * h
        e = 1e-6
        num = (sph.w_cubic(r + e, h) - sph.w_cubic(r - e, h)) / (2 * e)
        assert abs(num - sph.dw_cubic(r, h)) < 1e-6 * max(1.0, abs(num))


def test_gradient_is_antisymmetric_and_numeric() -> None:
    rng = random.Random(7)
    h = 0.2
    assert sph.grad_w((0.0, 0.0), h) == (0.0, 0.0)
    for _ in range(200):
        d = (rng.uniform(-0.45, 0.45), rng.uniform(-0.45, 0.45))
        g = sph.grad_w(d, h)
        gm = sph.grad_w((-d[0], -d[1]), h)
        assert abs(g[0] + gm[0]) < 1e-12 and abs(g[1] + gm[1]) < 1e-12
        e = 1e-7
        for c in range(2):
            dp = list(d)
            dm = list(d)
            dp[c] += e
            dm[c] -= e
            num = (sph.w_cubic(math.hypot(*dp), h) - sph.w_cubic(math.hypot(*dm), h)) / (2 * e)
            assert abs(num - g[c]) < 1e-5 * max(1.0, abs(num))


def test_neighbor_pairs_equal_brute_force() -> None:
    rng = random.Random(2024)
    for radius in (0.05, 0.1, 0.25):
        pos = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)) for _ in range(200)]
        assert sph.neighbor_pairs(pos, radius) == brute_pairs(pos, radius)
    # Points on cell borders and at exactly the radius.
    pos = [(0.0, 0.0), (0.1, 0.0), (0.2, 0.0), (0.1, 0.1), (-0.1, -0.1), (0.05, 0.05)]
    assert sph.neighbor_pairs(pos, 0.1) == brute_pairs(pos, 0.1)
    assert sph.neighbor_pairs([], 0.1) == []
    assert sph.neighbor_pairs([(0.3, 0.3)], 0.1) == []
    lists = sph.neighbor_lists(pos, 0.1)
    for i, nb in enumerate(lists):
        assert nb == [j for j in range(len(pos)) if j != i and ((pos[i][0] - pos[j][0]) ** 2 + (pos[i][1] - pos[j][1]) ** 2) < 0.01]


def test_density_equals_brute_force_sum() -> None:
    rng = random.Random(11)
    h = 0.06
    pos = [(rng.uniform(0, 0.6), rng.uniform(0, 0.6)) for _ in range(200)]
    ms = [rng.uniform(0.5, 1.5) for _ in pos]
    rho = sph.density(pos, ms, h)
    for i in range(len(pos)):
        ref = sum(ms[j] * sph.w_cubic(math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]), h) for j in range(len(pos)))
        assert abs(rho[i] - ref) < 1e-9 * ref


def test_density_on_a_lattice_is_near_rest_density() -> None:
    dx = 0.02
    rho0 = 1000.0
    h = 1.3 * dx
    n = 15
    pos = [(i * dx, j * dx) for i in range(n) for j in range(n)]
    ms = [rho0 * dx * dx] * len(pos)
    rho = sph.density(pos, ms, h)
    for k, p in enumerate(pos):
        i, j = round(p[0] / dx), round(p[1] / dx)
        if 3 <= i < n - 3 and 3 <= j < n - 3:
            assert abs(rho[k] - rho0) < 0.01 * rho0


# ---------------------------------------------------------------- WCSPH


def random_blob(rng, n, dx, rho0):
    side = int(math.ceil(math.sqrt(n)))
    pos = []
    for k in range(n):
        i, j = k % side, k // side
        pos.append((i * dx + rng.uniform(-0.2, 0.2) * dx, j * dx + rng.uniform(-0.2, 0.2) * dx))
    vel = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    ms = [rho0 * dx * dx * rng.uniform(0.8, 1.2) for _ in range(n)]
    return pos, vel, ms


def brute_accelerations(pos, vel, ms, h, rho0, c, gravity, alpha):
    n = len(pos)
    rho = [sum(ms[j] * sph.w_cubic(math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]), h) for j in range(n)) for i in range(n)]
    b = rho0 * c * c / 7.0
    p = [b * ((r / rho0) ** 7 - 1.0) for r in rho]
    acc = []
    for i in range(n):
        ax, ay = gravity
        for j in range(n):
            if j == i:
                continue
            d = (pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
            g = sph.grad_w(d, h)
            s = p[i] / rho[i] ** 2 + p[j] / rho[j] ** 2
            vr = (vel[i][0] - vel[j][0]) * d[0] + (vel[i][1] - vel[j][1]) * d[1]
            if alpha > 0 and vr < 0:
                mu = h * vr / (d[0] ** 2 + d[1] ** 2 + 0.01 * h * h)
                s += -alpha * c * mu / (0.5 * (rho[i] + rho[j]))
            ax -= ms[j] * s * g[0]
            ay -= ms[j] * s * g[1]
        acc.append((ax, ay))
    return acc


def test_tait_check_values() -> None:
    assert abs(wc.tait_b(1000.0, 10.0) - 14285.714285714286) < 1e-9
    assert wc.tait_pressure(1000.0, 1000.0, 10.0) == 0.0
    p = wc.tait_pressure(1010.0, 1000.0, 10.0)
    assert abs(p - 14285.714285714286 * (1.01 ** 7 - 1.0)) < 1e-9
    assert abs(p - 1030.505030) < 1e-5
    # For a small compression e, p is close to c^2 rho0 e.
    assert abs(wc.tait_pressure(1000.1, 1000.0, 10.0) - 100.0 * 0.1) < 0.01
    assert wc.tait_pressure(990.0, 1000.0, 10.0) < 0.0
    assert wc.tait_pressure(990.0, 1000.0, 10.0, clamp=True) == 0.0
    assert abs(wc.time_step_limit(0.026, 18.0, 2.0) - 0.4 * 0.026 / 20.0) < 1e-15


def test_accelerations_equal_brute_force() -> None:
    rng = random.Random(5)
    dx = 0.02
    pos, vel, ms = random_blob(rng, 49, dx, 1000.0)
    h = 1.3 * dx
    for alpha in (0.0, 0.2):
        acc, _, _ = wc.accelerations(pos, vel, ms, h, 1000.0, 15.0, (0.0, -9.81), alpha)
        ref = brute_accelerations(pos, vel, ms, h, 1000.0, 15.0, (0.0, -9.81), alpha)
        for a, r in zip(acc, ref):
            scale = max(1.0, abs(r[0]), abs(r[1]))
            assert abs(a[0] - r[0]) < 1e-9 * scale and abs(a[1] - r[1]) < 1e-9 * scale


def test_momentum_is_conserved_without_walls_and_gravity() -> None:
    rng = random.Random(9)
    dx = 0.02
    pos, vel, ms = random_blob(rng, 64, dx, 1000.0)
    h = 1.3 * dx
    c = 15.0
    dt = wc.time_step_limit(h, c, 2.0)
    p0 = wc.momentum(vel, ms)
    l0 = wc.angular_momentum(pos, vel, ms)
    scale = sum(m * math.hypot(*v) for m, v in zip(ms, vel))
    lscale = sum(m * math.hypot(*x) * math.hypot(*v) for m, x, v in zip(ms, pos, vel))
    for _ in range(60):
        pos, vel, _ = wc.step(pos, vel, ms, dt, h, 1000.0, c, (0.0, 0.0), alpha=0.1)
    p1 = wc.momentum(vel, ms)
    l1 = wc.angular_momentum(pos, vel, ms)
    assert abs(p1[0] - p0[0]) < 1e-10 * scale and abs(p1[1] - p0[1]) < 1e-10 * scale
    assert abs(l1 - l0) < 1e-10 * lscale


def test_gravity_alone_gives_free_fall() -> None:
    pos = [(0.0, 0.0), (1.0, 0.0)]
    vel = [(0.0, 0.0), (0.0, 0.0)]
    ms = [1.0, 1.0]
    dt = 0.01
    for _ in range(10):
        pos, vel, _ = wc.step(pos, vel, ms, dt, 0.1, 1000.0, 10.0)
    # Symplectic Euler: v_n = n g dt and y_n = g dt^2 n (n + 1) / 2.
    assert abs(vel[0][1] + 9.81 * 0.1) < 1e-12
    assert abs(pos[1][1] + 9.81 * dt * dt * 55) < 1e-12


def test_small_dam_break_keeps_the_density_error_near_one_percent() -> None:
    dx = 0.02
    rho0 = 1000.0
    h = 1.3 * dx
    n_side = 8
    v_max = math.sqrt(2 * 9.81 * n_side * dx)
    c = 10.0 * v_max
    pos = [((i + 0.5) * dx, (j + 0.5) * dx) for i in range(n_side) for j in range(n_side)]
    vel = [(0.0, 0.0)] * len(pos)
    ms = [rho0 * dx * dx] * len(pos)
    dt = wc.time_step_limit(h, c, v_max)
    box = (0.0, 0.0, 0.4, 0.4)
    worst_mean = 0.0
    for _ in range(280):
        pos, vel, rho = wc.step(pos, vel, ms, dt, h, rho0, c, alpha=0.1, clamp=True, box=box)
        worst_mean = max(worst_mean, sum(max(r - rho0, 0.0) for r in rho) / (rho0 * len(rho)))
    assert worst_mean < 0.01
    assert wc.max_speed(vel) < 1.2 * v_max
    # The column has collapsed: the front moved to the right.
    assert max(x for x, _ in pos) > n_side * dx + 0.05
    for x, y in pos:
        assert 0.0 <= x <= 0.4 and 0.0 <= y <= 0.4
